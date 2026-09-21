# `notify/` — make a long job's silence mean something

One script. It watches a log and a milestone directory and speaks through **a command
template you supply**.

No transport is built in. No credential is read, stored or logged. If your transport
needs a token, it lives in that transport's own config or environment — outside this
script and outside your repository.

---

## Why

A routing run was once left alone for **10 hours 53 minutes**. The process was alive, the
log was growing, and it had stopped making progress hours earlier. Nothing said anything,
and "no news" was indistinguishable from "wedged".

The fix is not more messages. It is a **guaranteed heartbeat**: a message that says
*"still running, 214 minutes in, no new log lines"* converts silence into information.
That is rule 3 below, and it is the one people leave out.

---

## The four rules

1. **Speak only on change** — new log lines, or a new file matching `--milestone-glob`.
2. **Never more often than `--min-gap`** — a chatty job must not be able to spam a phone.
3. **Always speak at least every `--heartbeat`** while the job is alive.
   **Silence must never be ambiguous.**
4. **Stop on completion** — when `--done-file` appears, when `--pid` exits, or at
   `--max-seconds` — and say *which*.

Exit codes: `0` done-file · `1` process exited · `2` wall-clock cap · `3` relay error.

---

## Usage

```sh
python3 progress_relay.py \
    --log route.log \
    --milestone-dir out --milestone-glob '*.ses' \
    --done-file report.md \
    --pid 12345 \
    --command 'notify-send {title} {body}' \
    --poll 60 --min-gap 600 --heartbeat 2700 --max-seconds 50400 \
    --title 'board route'

python3 progress_relay.py --selftest
```

With **no `--command`** messages go to stdout — a perfectly good way to test the relay
before pointing it at anything.

### The command template

These placeholders are substituted, each shell-quoted for you:

| token | meaning |
|---|---|
| `{title}` | short subject line |
| `{body}` | message body |
| `{kind}` | `start` \| `progress` \| `heartbeat` \| `done` \| `timeout` \| `error` |
| `{file}` | path to a temp file holding the body — use this for long messages |

```sh
--command 'notify-send {title} {body}'
--command 'mail -s {title} me@example.org < {file}'
--command 'curl -s -X POST -d @{file} "$MY_WEBHOOK"'      # token from the environment
--command 'osascript -e "display notification {body} with title {title}"'
```

The command runs through the shell with a 120 s timeout. **A transport failure is
reported to stdout and the relay keeps going** — a broken notifier must never take the
job down with it. If delivery matters, check the other end; this script cannot.

---

## What it cannot see

* **Whether the job is doing anything useful.** It relays what the log says. For a
  router, pair it with `../routing/route_supervise.py`, which judges the *rate* —
  connections per minute, with a floor — and distinguishes four failure states.
* **Whether a message arrived.**
* **Anything about the content.** Log lines are passed through as text. If your log
  contains secrets, so will your notifications.

---

## Testing

`--selftest` runs the entire loop against a synthetic log with an **injected clock** and a
recording transport, so it finishes in milliseconds and asserts the exact message
sequence: hello first, a `progress` on a real change, a `heartbeat` when nothing changes,
the minimum gap respected, `done` on the done-file, exit 1 on a vanished pid, exit 2 at
the cap, and a failing transport reported rather than fatal. It also greps its own source
to confirm no transport name or credential is hard-coded.
