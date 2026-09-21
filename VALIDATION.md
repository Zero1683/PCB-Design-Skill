# Validation record: 1.2.0

Date: 2026-09-21. Local platform: Windows; Node.js 22.23.2. These results describe the skill package and helper behavior, not a certified PCB design.

| Area | Result | Evidence/method | Limit |
|---|---|---|---|
| Skill structure | PASS | System skill validator | Frontmatter/structure only |
| Existing helpers | PASS, 11 tests | `python -X utf8 scripts/test_helpers.py --workdir <temp-root>` | Initialization and release integrity |
| Workflow helpers | PASS, 16 tests | `python -X utf8 scripts/test_workflow.py --workdir <temp-root>` | Known arithmetic, record rejection, normalized exports, envelope screening, localization and fake-bridge probe |
| Actual bridge server with simulated clients | PASS | `node scripts/test_bridge.mjs --workdir <temp-root>` | Window switching, nonexistent-window isolation and explicit-window request routing; no EDA client |
| Local live connection | BLOCKED | Existing bridge reports `WAITING_FOR_EDA`, zero windows | No client connection; old running bridge also reports upgrade recommended |
| Live project creation/edit/routing/export/reopen | NOT_RUN | Procedure in reference 11 | Must be tested in a disposable connected project |
| macOS end-to-end | NOT_RUN | Cross-platform commands documented | Windows execution and a Mac scenario review do not establish macOS execution |

## Independent scenario review

An independent agent was given the skill and two realistic requests without the acceptance notes or prior conclusions. It read the needed files without modifying files or accessing EDA:

1. A MacBook beginner has installed EasyEDA and Gateway and wants a 30 × 40 mm USB-powered temperature/humidity board, manufacturing files only, self-purchased parts.
2. An existing board has reviewed power/USB routes and needs ordinary GPIO/I²C routing plus supply review, with only a multimeter available.

The proposed actions loaded the bundled API, separated setup from project creation, kept the G5 stopping point, avoided purchasing, preserved existing critical routes, and selected explicit ordinary nets for native autorouting. Electrical reasoning separated known trace drop from missing via/contact resistance. Under the stated example assumptions, the 100 mm total copper path gives 98.514 mΩ and 29.554 mV at 0.3 A, without declaring the full path passed.

The review identified and the package addresses:

- An undefined variable in the bridge window-selection success response. Fixed and covered by the simulated-client regression.
- Two stale `openProject(projectPath)` instructions. Corrected to UUID and documented in third-party patch notes.
- No documented router completion-status API. Instructions now require verified installed-version semantics or native UI completion observation before further mutation; actual lifecycle verification remains pending.

This is a dry-run behavioral assessment, not measured design quality, hardware performance, or token savings. The additional scenarios in reference 11 remain a test plan until independently executed.

## Reproducing package checks

Run from the package root; choose a writable temporary directory on your working drive:

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/temp-root
python -X utf8 scripts/test_workflow.py --workdir /path/to/temp-root
node scripts/test_bridge.mjs --workdir /path/to/temp-root
```

The bridge regression starts and stops only its own isolated temporary server. It uses simulated clients and does not select or modify an actual EDA project. The workflow probe test briefly uses an unoccupied local bridge-range port; it skips that test if all ports are occupied.
