# -*- coding: utf-8 -*-
"""Supervise a long autoroute: a four-state watchdog plus a connections-per-minute floor.

WHY THIS EXISTS
    An autorouter can fail in four different ways and only one of them looks like a
    failure.  On the reference project a run was left alone for 10 hours 53 minutes
    because nothing said anything: the process was alive, the log was growing, and it
    had stopped making progress hours earlier.  A supervisor that only asks "is it
    still running?" cannot tell a working router from a wedged one.

THE FOUR STATES  (checked in this order, every --poll seconds)
    1. OUTPUT PRESENT   -- the result file exists and is non-empty and has stopped
                           growing.  This is SUCCESS and it is checked FIRST, because a
                           router that finishes and exits also trips states 3 and 4.
    2. CRASH SIGNATURE  -- a --crash-pattern regex matched in the log.  Stack overflow,
                           out-of-memory and null-pointer traces all look like ordinary
                           output to a size check.  Exit code alone is not enough: a JVM
                           that dies inside a worker thread can still exit 0.
    3. PROCESS GONE     -- the --pid is no longer alive and state 1 did not fire.  That
                           is a silent death, and it is a distinct failure from a crash
                           with a message.
    4. WALL CLOCK       -- --max-seconds elapsed.  A cap that is never reached costs
                           nothing; one that is missing costs a night.

    Plus the rate floor, which is the state that is easy to leave out:
    5. RATE FLOOR       -- connections gained per MINUTE, over the last --rate-window
                           passes, below --min-rate.  PER-PASS improvement is the WRONG
                           metric: a router's passes get longer as the board fills (2:59
                           to 9:56 on one measured run), so a fixed per-pass threshold
                           silently tightens and condemns a run that is still working.
                           Judge per unit of TIME.

WHAT THIS CANNOT SEE
    * Whether the route is any good.  A run that finishes fast can finish wrong.
      route_accept.py decides that, on the board read back from the EDA.
    * Progress a router makes without logging it.  The rate floor needs the log lines
      that --pass-regex matches; if it matches nothing, the rate check is REPORTED AS
      UNAVAILABLE rather than treated as a stall.  Silence must never be scored as zero.
    * Whether the process it is watching is the right one.  --pid is taken on trust.
    * Anything on another machine.  It reads local files and sends signals to nobody.

    This supervisor never kills anything.  It reports a verdict and exits with a code;
    what to do about a stalled router is a decision, and killing a job that is 95 %
    done because a threshold fired is a bad one to automate.

HOW IT WAS VALIDATED
    The rate parser is a port of the stall judge written for a released board's routing
    runs; re-run against those logs it reproduces the per-pass timings and the
    "still progressing" / "stalled" verdicts.  `--selftest` runs the whole state machine
    against synthetic logs and a temporary output file.

USAGE
    python3 route_supervise.py --log route.log --output route.ses
                               [--pid 12345] [--poll 30] [--max-seconds 50400]
                               [--min-rate 0.10] [--rate-window 2]
                               [--crash-pattern "StackOverflowError|OutOfMemoryError"]
                               [--pass-regex "..."] [--once] [--quiet]
    python3 route_supervise.py --rate-only route.log
    python3 route_supervise.py --selftest

EXIT CODES
    0 output present (success)   1 crash signature   2 process gone
    3 wall-clock cap             4 rate floor        5 supervisor error
"""
from __future__ import print_function

import os
import re
import sys
import time

DEFAULT_CRASH = (r"StackOverflowError|OutOfMemoryError|NullPointerException|"
                 r"\bSegmentation fault\b|\bException in thread\b|\bFATAL\b")

# Default pass-line parser.  Named groups: idx, time, unrouted.
DEFAULT_PASS_RE = (r"pass\s+#(?P<idx>\d+).*?completed in (?P<time>[^w]*?)"
                   r"with the score of [\d.]+ \((?P<unrouted>\d+) unrouted")

_MIN_RE = re.compile(r"(\d+)\s+minutes?")
_HOUR_RE = re.compile(r"(\d+)\s+hours?")
_SEC_RE = re.compile(r"([\d.]+)\s+seconds?")

STATE_OUTPUT, STATE_CRASH, STATE_GONE, STATE_CLOCK, STATE_RATE, STATE_ERROR = range(6)
STATE_NAME = {0: "OUTPUT PRESENT", 1: "CRASH SIGNATURE", 2: "PROCESS GONE",
              3: "WALL CLOCK", 4: "RATE FLOOR", 5: "SUPERVISOR ERROR"}


def parse_duration(s):
    """'3 minutes 12.5 seconds' -> 192.5.  Unparseable -> 0.0, which the caller must
    treat as 'no timing information', not as 'instant'."""
    total = 0.0
    m = _HOUR_RE.search(s)
    if m:
        total += int(m.group(1)) * 3600
    m = _MIN_RE.search(s)
    if m:
        total += int(m.group(1)) * 60
    m = _SEC_RE.search(s)
    if m:
        total += float(m.group(1))
    return total


def parse_passes(text, pass_re=DEFAULT_PASS_RE):
    """-> [(index, seconds, unrouted)] in file order."""
    rx = re.compile(pass_re, re.S)
    out = []
    for m in rx.finditer(text):
        d = m.groupdict()
        out.append((int(d["idx"]), parse_duration(d["time"]), int(d["unrouted"])))
    return out


def rates(passes):
    """-> [(index, seconds, unrouted, gained, connections_per_minute)]"""
    out = []
    prev = None
    for idx, secs, unr in passes:
        if prev is None or secs <= 0:
            out.append((idx, secs, unr, None, None))
        else:
            gained = prev - unr
            out.append((idx, secs, unr, gained, gained / (secs / 60.0)))
        prev = unr
    return out


def rate_verdict(passes, min_rate=0.10, window=2):
    """-> (verdict, last_rates).  verdict is 'progressing' | 'stalled' | 'unknown'.

    'unknown' when there are not yet `window` timed passes.  That is deliberately NOT
    'stalled': a run that has not produced enough evidence has not failed.
    """
    rs = [r[4] for r in rates(passes) if r[4] is not None]
    if len(rs) < window:
        return "unknown", rs
    last = rs[-window:]
    return ("stalled" if all(x < min_rate for x in last) else "progressing"), last


# Shared probe avoids os.kill(pid, 0) on Windows, where it terminates processes.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from process_status import pid_alive


def _read(path, limit=4 * 1024 * 1024):
    try:
        size = os.path.getsize(path)
        with open(path, encoding="utf-8", errors="replace") as fh:
            if size > limit:
                fh.seek(size - limit)
            return fh.read()
    except Exception:
        return ""


def check_once(log=None, output=None, pid=None, started=None, max_seconds=None,
               crash_pattern=DEFAULT_CRASH, pass_re=DEFAULT_PASS_RE,
               min_rate=0.10, window=2, output_stable_for=5.0, _sizes=None):
    """One sweep of the state machine.  Returns (state or None, detail dict)."""
    detail = {}
    now = time.time()

    # Output readiness is bound to this run; it is not route acceptance.
    if output and os.path.isfile(output) and os.path.getsize(output) > 0:
        st = os.stat(output)
        detail["output_size"] = st.st_size
        detail["output_age"] = now - st.st_mtime
        growing = False
        if _sizes is not None:
            prev = _sizes.get(output)
            _sizes[output] = st.st_size
            growing = prev is not None and prev != st.st_size
        if started is None:
            detail["note"] = "output not bound to a run start"
        elif st.st_mtime < started:
            detail["note"] = "stale output predates this run"
        elif growing:
            detail["note"] = "output still growing"
        elif detail["output_age"] >= output_stable_for:
            detail["coverage"] = "fresh-stable-output-only"
            return STATE_OUTPUT, detail
        # Stale/growing files must not suppress crash/gone/timeout checks below.

    text = _read(log) if log else ""
    detail["log_bytes"] = len(text)

    # --- state 2: crash signature
    if crash_pattern:
        m = re.search(crash_pattern, text)
        if m:
            line = text[max(0, text.rfind("\n", 0, m.start()) + 1):
                        text.find("\n", m.end()) if text.find("\n", m.end()) > 0 else None]
            detail["crash"] = line.strip()[:200]
            return STATE_CRASH, detail

    # --- state 3: process gone
    if pid is not None and not pid_alive(pid):
        detail["pid"] = pid
        return STATE_GONE, detail

    # --- state 4: wall clock
    if max_seconds and started is not None and (now - started) >= max_seconds:
        detail["elapsed"] = now - started
        return STATE_CLOCK, detail

    # --- state 5: rate floor
    passes = parse_passes(text, pass_re)
    verdict, last = rate_verdict(passes, min_rate, window)
    detail["passes"] = len(passes)
    detail["rate_verdict"] = verdict
    detail["last_rates"] = [round(x, 3) for x in last]
    if verdict == "stalled":
        return STATE_RATE, detail
    return None, detail


def supervise(log=None, output=None, pid=None, poll=30, max_seconds=None,
              crash_pattern=DEFAULT_CRASH, pass_re=DEFAULT_PASS_RE,
              min_rate=0.10, window=2, once=False, quiet=False, clock=time,
              sleep=None, started=None):
    started = clock.time() if started is None else started
    if started > clock.time():
        raise ValueError("Run start must not be in the future")
    sizes = {}
    sleep = sleep or clock.sleep
    while True:
        state, detail = check_once(log, output, pid, started, max_seconds,
                                   crash_pattern, pass_re, min_rate, window,
                                   _sizes=sizes)
        if not quiet:
            print("[%6.0fs] %s %s"
                  % (clock.time() - started,
                     STATE_NAME.get(state, "running"),
                     " ".join("%s=%s" % kv for kv in sorted(detail.items()))))
            sys.stdout.flush()
        if state is not None:
            return state, detail
        if once:
            return None, detail
        sleep(poll)


def print_rate_table(text, pass_re=DEFAULT_PASS_RE, min_rate=0.10, window=2):
    passes = parse_passes(text, pass_re)
    if not passes:
        print("no pass lines matched --pass-regex.")
        print("The rate check is UNAVAILABLE, which is not the same as a stall.")
        return 5
    print("%-8s %9s %10s %9s %12s" % ("pass", "seconds", "unrouted", "gained", "conn/min"))
    for idx, secs, unr, gained, rate in rates(passes):
        print("%-8s %9.0f %10d %9s %12s"
              % ("#%d" % idx, secs, unr,
                 "" if gained is None else gained,
                 "" if rate is None else "%.2f" % rate))
    verdict, last = rate_verdict(passes, min_rate, window)
    print()
    print("last %d pass rate(s): %s  ->  %s (floor %.2f conn/min)"
          % (window, ", ".join("%.2f" % x for x in last) or "n/a", verdict, min_rate))
    return 4 if verdict == "stalled" else 0


# --------------------------------------------------------------------------- selftest

_GOOD_LOG = """
Starting autoroute
pass #1 completed in 2 minutes 59.0 seconds with the score of 12345.0 (410 unrouted
pass #2 completed in 4 minutes 10.0 seconds with the score of 11000.0 (300 unrouted
pass #3 completed in 9 minutes 56.0 seconds with the score of 10500.0 (250 unrouted
"""

_STALLED_LOG = """
pass #1 completed in 2 minutes 59.0 seconds with the score of 12345.0 (410 unrouted
pass #2 completed in 20 minutes 0.0 seconds with the score of 12000.0 (409 unrouted
pass #3 completed in 30 minutes 0.0 seconds with the score of 11990.0 (409 unrouted
"""

_CRASH_LOG = """
pass #1 completed in 2 minutes 59.0 seconds with the score of 12345.0 (410 unrouted
Exception in thread "main" java.lang.StackOverflowError
	at PolylineTrace.combine(PolylineTrace.java:1)
"""


def _selftest():
    import tempfile
    ok = True
    print("route_supervise selftest")

    p = parse_passes(_GOOD_LOG)
    good = len(p) == 3 and abs(p[2][1] - 596.0) < 1e-9 and p[2][2] == 250
    print("  pass lines parsed (3, last 596 s, 250 unrouted) : %s" % ("OK" if good else "FAIL"))
    ok &= good

    r = rates(p)
    # pass 2 gained 110 in 250 s -> 26.4/min ; pass 3 gained 50 in 596 s -> 5.03/min
    good = abs(r[1][4] - 110.0 / (250.0 / 60.0)) < 1e-6
    print("  conn/min uses TIME, not pass index              : %.2f  %s"
          % (r[1][4], "OK" if good else "FAIL"))
    ok &= good

    v, last = rate_verdict(p, 0.10, 2)
    good = v == "progressing"
    print("  a run whose passes get LONGER is not stalled    : %s (%s)  %s"
          % (v, [round(x, 2) for x in last], "OK" if good else "FAIL"))
    ok &= good

    v, last = rate_verdict(parse_passes(_STALLED_LOG), 0.10, 2)
    good = v == "stalled"
    print("  a genuinely stalled run IS caught               : %s (%s)  %s"
          % (v, [round(x, 3) for x in last], "OK" if good else "FAIL"))
    ok &= good

    v, _l = rate_verdict(parse_passes(_GOOD_LOG)[:1], 0.10, 2)
    good = v == "unknown"
    print("  too little evidence reports 'unknown', not stall: %s  %s"
          % (v, "OK" if good else "FAIL"))
    ok &= good

    tmp = tempfile.mkdtemp(prefix="pcbkit-")
    logp = os.path.join(tmp, "r.log")
    outp = os.path.join(tmp, "r.ses")

    open(logp, "w").write(_CRASH_LOG)
    st, d = check_once(log=logp, output=outp, started=time.time(), max_seconds=99999)
    good = st == STATE_CRASH
    print("  state 2 crash signature                         : %s  %s"
          % (STATE_NAME.get(st), "OK" if good else "FAIL"))
    ok &= good

    open(logp, "w").write(_GOOD_LOG)
    st, d = check_once(log=logp, output=outp, pid=999999999,
                       started=time.time(), max_seconds=99999)
    good = st == STATE_GONE
    print("  state 3 process gone                            : %s  %s"
          % (STATE_NAME.get(st), "OK" if good else "FAIL"))
    ok &= good

    st, d = check_once(log=logp, output=outp, started=time.time() - 100,
                       max_seconds=10)
    good = st == STATE_CLOCK
    print("  state 4 wall clock                              : %s  %s"
          % (STATE_NAME.get(st), "OK" if good else "FAIL"))
    ok &= good

    open(logp, "w").write(_STALLED_LOG)
    st, d = check_once(log=logp, output=outp, started=time.time(), max_seconds=99999)
    good = st == STATE_RATE
    print("  state 5 rate floor                              : %s  %s"
          % (STATE_NAME.get(st), "OK" if good else "FAIL"))
    ok &= good

    # output present must WIN over the stall and over a dead pid
    open(outp, "w").write("(session x)")
    os.utime(outp, (time.time() - 60, time.time() - 60))
    st, d = check_once(log=logp, output=outp, pid=999999999,
                       started=time.time() - 100000, max_seconds=10)
    good = st == STATE_OUTPUT
    print("  state 1 output wins over stall/gone/clock       : %s  %s"
          % (STATE_NAME.get(st), "OK" if good else "FAIL"))
    ok &= good

    # a growing output file is not yet 'present'
    sizes = {outp: 5}
    st, d = check_once(log=logp, output=outp, started=time.time(), _sizes=sizes)
    good = st != STATE_OUTPUT
    print("  a still-growing output is not called finished   : %s  %s"
          % (d.get("note", STATE_NAME.get(st)), "OK" if good else "FAIL"))
    ok &= good

    print("route_supervise selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()

    def opt(flag, default=None, cast=str):
        return cast(argv[argv.index(flag) + 1]) if flag in argv else default

    if "--rate-only" in argv:
        path = argv[argv.index("--rate-only") + 1]
        return print_rate_table(_read(path),
                                opt("--pass-regex", DEFAULT_PASS_RE),
                                opt("--min-rate", 0.10, float),
                                opt("--rate-window", 2, int))
    if "--log" not in argv and "--output" not in argv:
        print(__doc__)
        return 2
    state, detail = supervise(
        log=opt("--log"), output=opt("--output"), pid=opt("--pid", None, int),
        poll=opt("--poll", 30, float), max_seconds=opt("--max-seconds", None, float),
        crash_pattern=opt("--crash-pattern", DEFAULT_CRASH),
        pass_re=opt("--pass-regex", DEFAULT_PASS_RE),
        min_rate=opt("--min-rate", 0.10, float),
        window=opt("--rate-window", 2, int),
        once=("--once" in argv), quiet=("--quiet" in argv),
        started=opt("--started-at", None, float))
    print("VERDICT: %s  %s" % (STATE_NAME.get(state, "still running"),
                               " ".join("%s=%s" % kv for kv in sorted(detail.items()))))
    return 5 if state is None else state


if __name__ == "__main__":
    sys.exit(main(sys.argv))
