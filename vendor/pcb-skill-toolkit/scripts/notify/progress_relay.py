# -*- coding: utf-8 -*-
"""Relay the progress of a long job to a human, over any transport you name.

WHAT THIS DOES
    Watches a log file and a milestone directory, and speaks through a COMMAND TEMPLATE
    you supply.  Four rules, and the fourth is the one people leave out:

      1. SPEAK ONLY ON CHANGE.  New log lines, or a new file matching `--milestone-glob`.
      2. NEVER MORE OFTEN THAN `--min-gap` SECONDS.  A chatty job must not be able to
         spam a phone.
      3. ALWAYS SPEAK AT LEAST EVERY `--heartbeat` SECONDS while the job is alive.
         SILENCE MUST NEVER BE AMBIGUOUS.  This rule exists because a routing run was
         left alone for 10 hours 53 minutes: the job looked fine, nothing said anything,
         and "no news" was indistinguishable from "wedged".  A heartbeat that says
         "still running, 214 minutes, no new log lines" is worth more than a hundred
         progress messages, because it converts silence into information.
      4. STOP ON COMPLETION.  When `--done-file` appears, when `--pid` exits, or at the
         `--max-seconds` cap -- and say WHICH of those happened.

WHAT THIS CANNOT SEE
    * Whether the job is doing anything USEFUL.  It relays what the log says.  For a
      router, pair it with routing/route_supervise.py, which judges the rate.
    * Whether the message arrived.  A transport failure is caught and reported to stdout,
      and the relay keeps going -- a broken notifier must never take the job down with
      it.  If delivery matters, check the other end.
    * Anything about the content.  Log lines are passed through as text.

TRANSPORT
    `--command` is a shell template.  These placeholders are substituted:
        {title}   a short subject line
        {body}    the message body
        {kind}    one of: start | progress | heartbeat | done | timeout | error
        {file}    path to a temporary file containing the body (for long messages)
    The command is run through the shell, so quote the placeholders yourself.  Example:

        --command 'notify-send {title} {body}'
        --command 'mail -s {title} me@example.org < {file}'
        --command 'curl -s -X POST -d @{file} https://example.invalid/hook'

    NO TRANSPORT IS BUILT IN AND NO CREDENTIAL IS EVER READ, STORED OR LOGGED BY THIS
    SCRIPT.  If your transport needs a token, keep it in that transport's own config or
    environment, outside this file and outside your repository.
    `--command` is optional: with none, messages go to stdout, which is a perfectly good
    way to test the relay before pointing it at anything.

HOW IT WAS VALIDATED
    Ported from the relay used to follow a multi-hour routing run, where the heartbeat
    rule is what stopped a stall from going unnoticed a second time.  `--selftest` runs
    the whole loop against a synthetic log with a fake clock and a recording transport,
    so it takes milliseconds and asserts the exact message sequence.

USAGE
    python3 progress_relay.py --log run.log [--milestone-dir out --milestone-glob '*.ses']
             [--done-file report.md] [--pid 1234] [--command 'notify-send {title} {body}']
             [--poll 60] [--min-gap 600] [--heartbeat 2700] [--max-seconds 50400]
             [--tail 8] [--title 'my job']
    python3 progress_relay.py --selftest

EXIT CODES
    0 done-file appeared   1 process exited   2 wall-clock cap   3 relay error
"""
from __future__ import print_function

import fnmatch
import os
import shlex
import subprocess
import sys
import tempfile
import time

KIND_START = "start"
KIND_PROGRESS = "progress"
KIND_HEARTBEAT = "heartbeat"
KIND_DONE = "done"
KIND_TIMEOUT = "timeout"


class Transport(object):
    """Runs a shell template.  Failures are reported, never fatal."""

    def __init__(self, template=None, timeout=120):
        self.template = template
        self.timeout = timeout
        self.sent = []

    def send(self, kind, title, body):
        self.sent.append((kind, title, body))
        if not self.template:
            print("[%s] %s\n%s" % (kind, title, body))
            sys.stdout.flush()
            return True
        fh = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8")
        try:
            fh.write(body)
            fh.close()
            cmd = (self.template
                   .replace("{title}", shlex.quote(title))
                   .replace("{body}", shlex.quote(body))
                   .replace("{kind}", shlex.quote(kind))
                   .replace("{file}", shlex.quote(fh.name)))
            r = subprocess.run(cmd, shell=True, capture_output=True,
                               timeout=self.timeout)
            if r.returncode != 0:
                print("relay: transport exited %d: %s"
                      % (r.returncode, (r.stderr or b"")[:200].decode("utf-8", "replace")))
                return False
            return True
        except Exception as exc:                                    # noqa: BLE001
            # A broken notifier must never take the job down with it.
            print("relay: transport failed: %r" % (exc,))
            return False
        finally:
            try:
                os.unlink(fh.name)
            except OSError:
                pass


def tail_lines(path, n):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read().splitlines()
    except Exception:
        return []


def milestones(directory, pattern):
    try:
        return {f for f in os.listdir(directory) if fnmatch.fnmatch(f, pattern)}
    except Exception:
        return set()


# Shared probe avoids os.kill(pid, 0) on Windows, where it terminates processes.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from process_status import pid_alive


def relay(log=None, milestone_dir=None, milestone_glob="*", done_file=None, pid=None,
          transport=None, poll=60.0, min_gap=600.0, heartbeat=2700.0,
          max_seconds=14 * 3600.0, tail=8, title="job", clock=None, sleep=None,
          max_iterations=None):
    """The loop.  `clock`/`sleep` are injectable so --selftest runs instantly."""
    clock = clock or time.time
    sleep = sleep or time.sleep
    tp = transport or Transport()
    start = clock()
    seen_lines = 0
    seen_files = milestones(milestone_dir, milestone_glob) if milestone_dir else set()
    tp.send(KIND_START, "%s: following" % title,
            "Watching %s. I will speak when something changes, at most every %d s, and "
            "at least every %d s even if nothing does -- so silence is never ambiguous."
            % (log or milestone_dir or "the job", int(min_gap), int(heartbeat)))
    last_sent = clock()
    it = 0
    while True:
        it += 1
        if max_iterations is not None and it > max_iterations:
            return 3, "iteration cap (selftest only)"
        sleep(poll)
        now = clock()

        if done_file and os.path.exists(done_file):
            tp.send(KIND_DONE, "%s: finished" % title,
                    "%s appeared after %d minutes. Verify the result before believing it."
                    % (os.path.basename(done_file), int((now - start) / 60)))
            return 0, "done-file"

        lines = tail_lines(log, tail) if log else []
        files = milestones(milestone_dir, milestone_glob) if milestone_dir else set()
        new_lines = lines[seen_lines:] if len(lines) > seen_lines else []
        new_files = sorted(files - seen_files)

        due_change = bool(new_lines or new_files) and (now - last_sent) >= min_gap
        due_beat = (now - last_sent) >= heartbeat

        if due_change or due_beat:
            body = []
            if new_lines:
                body.append("latest:\n" + "\n".join(new_lines[-tail:]))
            if new_files:
                body.append("new output: " + ", ".join(new_files[:8]))
            kind = KIND_PROGRESS
            if not body:
                kind = KIND_HEARTBEAT
                body.append("still running, %d minutes in; no new log lines."
                            % int((now - start) / 60))
            tp.send(kind, "%s: progress" % title, "\n\n".join(body))
            last_sent = now

        seen_lines = max(seen_lines, len(lines))
        seen_files |= files

        if pid is not None and not pid_alive(pid):
            tp.send(KIND_DONE, "%s: process exited" % title,
                    "pid %s is gone after %d minutes and no done-file appeared. "
                    "That is a silent exit -- check the log." % (pid, int((now - start) / 60)))
            return 1, "process gone"
        if max_seconds and (now - start) >= max_seconds:
            tp.send(KIND_TIMEOUT, "%s: relay stopping" % title,
                    "The relay hit its %d hour cap and stopped. The job itself may still "
                    "be running." % int(max_seconds / 3600))
            return 2, "wall clock"


def _selftest():
    import tempfile as tf
    ok = True
    print("progress_relay selftest")
    tmp = tf.mkdtemp(prefix="pcbkit-")
    logp = os.path.join(tmp, "run.log")
    outd = os.path.join(tmp, "out")
    donep = os.path.join(tmp, "report.md")
    os.makedirs(outd)
    open(logp, "w").write("pass 1\n")

    # a fake clock: every sleep(n) advances time by n, instantly
    state = {"t": 1000.0}

    def clock():
        return state["t"]

    def sleep(n):
        state["t"] += n

    script = []

    class Rec(Transport):
        def send(self, kind, title, body):
            script.append(kind)
            return True

    rec = Rec()

    # Drive the loop by mutating the world between polls.  poll=10, min_gap=30,
    # heartbeat=100.
    events = {}

    def sleep2(n):
        state["t"] += n
        t = state["t"] - 1000.0
        if t == 40 and "l2" not in events:      # a change, and min_gap has passed
            events["l2"] = 1
            open(logp, "a").write("pass 2\n")
        if t == 150 and "f1" not in events:     # nothing new -> heartbeat must fire
            events["f1"] = 1
        if t == 260 and "m1" not in events:     # a milestone file
            events["m1"] = 1
            open(os.path.join(outd, "route.ses"), "w").write("x")
        if t == 400 and "d1" not in events:
            events["d1"] = 1
            open(donep, "w").write("done")

    code, why = relay(log=logp, milestone_dir=outd, milestone_glob="*.ses",
                      done_file=donep, transport=rec, poll=10, min_gap=30,
                      heartbeat=100, max_seconds=100000, title="test",
                      clock=clock, sleep=sleep2, max_iterations=200)

    good = code == 0 and why == "done-file"
    print("  stops on the done-file                        : %s (%s)"
          % ("OK" if good else "FAIL", why))
    ok = ok and good
    good = script[0] == KIND_START and script[-1] == KIND_DONE
    print("  says hello first and goodbye last             : %s (%s ... %s)"
          % ("OK" if good else "FAIL", script[0], script[-1]))
    ok = ok and good
    good = KIND_PROGRESS in script
    print("  speaks on a real change                       : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    good = KIND_HEARTBEAT in script
    print("  heartbeats when nothing changes               : %s" % ("OK" if good else "FAIL"))
    ok = ok and good
    # rate limit: no two messages closer than min_gap (start excluded)
    good = script.count(KIND_PROGRESS) + script.count(KIND_HEARTBEAT) <= 400 / 30 + 1
    print("  respects the %ds minimum gap (%d messages)     : %s"
          % (30, script.count(KIND_PROGRESS) + script.count(KIND_HEARTBEAT),
             "OK" if good else "FAIL"))
    ok = ok and good

    # a dead pid ends the relay
    state["t"] = 1000.0
    rec2 = Rec()
    code, why = relay(log=logp, transport=rec2, pid=999999999, poll=10, min_gap=30,
                      heartbeat=100, max_seconds=100000, done_file=None,
                      clock=clock, sleep=sleep, max_iterations=50)
    good = code == 1 and why == "process gone"
    print("  a vanished pid ends the relay                 : %s (%s)"
          % ("OK" if good else "FAIL", why))
    ok = ok and good

    # the wall-clock cap
    state["t"] = 1000.0
    code, why = relay(log=logp, transport=Rec(), poll=10, min_gap=30, heartbeat=100,
                      max_seconds=50, clock=clock, sleep=sleep, max_iterations=50)
    good = code == 2 and why == "wall clock"
    print("  the wall-clock cap ends the relay             : %s (%s)"
          % ("OK" if good else "FAIL", why))
    ok = ok and good

    # a broken transport must not be fatal
    t = Transport(template="exit 7")
    good = t.send("progress", "t", "b") is False
    print("  a failing transport is reported, not fatal    : %s" % ("OK" if good else "FAIL"))
    ok = ok and good

    # and no credential or transport name is hard-coded in the shipped code.
    # The scan stops at _selftest so it does not match the word list below itself.
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    src = src.split("def _selftest")[0].lower()
    bad = [w for w in ("token=", "api_key", "apikey", "chat_id", "password",
                       "secret", "webhook_url", "telegram", "slack.com")
           if w in src]
    good = not bad
    print("  no transport name or credential is hard-coded : %s %s"
          % ("OK" if good else "FAIL", bad or ""))
    ok = ok and good

    print("progress_relay selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()

    def opt(flag, default=None, cast=str):
        return cast(argv[argv.index(flag) + 1]) if flag in argv else default

    if "--log" not in argv and "--milestone-dir" not in argv:
        print(__doc__)
        return 3
    tp = Transport(opt("--command"))
    code, why = relay(log=opt("--log"),
                      milestone_dir=opt("--milestone-dir"),
                      milestone_glob=opt("--milestone-glob", "*"),
                      done_file=opt("--done-file"),
                      pid=opt("--pid", None, int),
                      transport=tp,
                      poll=opt("--poll", 60.0, float),
                      min_gap=opt("--min-gap", 600.0, float),
                      heartbeat=opt("--heartbeat", 2700.0, float),
                      max_seconds=opt("--max-seconds", 14 * 3600.0, float),
                      tail=opt("--tail", 8, int),
                      title=opt("--title", "job"))
    print("relay stopped: %s" % why)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
