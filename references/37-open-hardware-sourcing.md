# Finding and adapting open hardware

Read this when an existing editable board could shorten a new PCB project. This is a project-time search procedure, not a library of approved circuits. A public repository, platform clone button, Gerber file, or license badge alone does not prove that a design is reusable for the intended purpose or that a physical board works.

## Search only after the product brief

1. Record the user's function, carrier or enclosure, approximate board envelope, supply, interfaces, assembly method, and intended output (private prototype, shared source, sold board). Reuse a compatible module if that satisfies the accepted goal; honor a request for a custom PCB.
2. Search the relevant MCU vendor's reference designs, GitHub, and [OSHWHub](https://oshwhub.com/) using the exact MCU/module or functional block plus `schematic`, `PCB`, `EasyEDA`, `KiCad`, and the desired license. Use a project-supplied source first when appropriate. Inspect a few plausible results, then choose by fit and evidence; do not trawl indefinitely or select by stars alone. Search again when the short list is unsuitable or outdated.
3. Seek editable native schematic **and** PCB source, matching symbol/footprint libraries, revision history, BOM and manufacturing files where available. A PDF, image, Gerber, firmware-only repo, or schematic-only repo can inform a circuit but cannot serve as an editable whole-board baseline. Native EDA formats may need conversion; confirm import, pin-net and footprint readback before editing.
4. Compare exact parts, operating range, physical dimensions, boot/programming path, antenna or RF constraints, power and thermal budget, assembly availability, reported test scope and open issues against the accepted requirements. A working photo is evidence of one build, not qualification of a derivative. State what will be retained and changed in one short explanation to the beginner.

### Leads checked on 2026-09-23

These links help discovery; recheck live files, licenses and revision before use. No project files below are shipped with this skill. None has been independently assembled or electrically qualified here.

| Lead | Editable source and license evidence | Use boundary |
|---|---|---|
| [CIRCUITSTATE/Mitayi-Pico-D1](https://github.com/CIRCUITSTATE/Mitayi-Pico-D1) | RP2040 KiCad `.kicad_sch`, `.kicad_pcb`, production files and [MIT LICENSE](https://github.com/CIRCUITSTATE/Mitayi-Pico-D1/blob/master/LICENSE); README identifies revision R0.6 | Candidate RP2040 starting board. It is not Raspberry Pi Pico pin-compatible; verify exact parts, PCB and intended modifications. |
| [atomic14/basic-esp32s3-dev-board](https://github.com/atomic14/basic-esp32s3-dev-board) | Basic ESP32-S3 KiCad `.kicad_sch`, `.kicad_pcb`, `.kicad_pro` and [MIT LICENSE](https://github.com/atomic14/basic-esp32s3-dev-board/blob/main/LICENSE) | Candidate ESP32-S3 starting board. README explicitly says it omits USB ESD protection and battery charge/power-path control; add and verify these if the product needs them. |
| [Fred98246/ESP-32-Dev-Board](https://github.com/Fred98246/ESP-32-Dev-Board) | ESP32-S3-MINI-1 KiCad schematic and PCB with repository [MIT LICENSE](https://github.com/Fred98246/ESP-32-Dev-Board/blob/main/LICENSE) | An extended-board alternative, not a bare minimum: it includes ENS210 and WS2812B. Repository description is not independent electrical or physical test evidence. |

An MIT label in GitHub's sidebar can describe software while board files have different terms. For example, [ESP32-Business-Card](https://github.com/kevinsun-dev/ESP32-Business-Card) distinguishes hardware CC BY-SA from firmware MIT; [dya-keyboard](https://github.com/cormoran/dya-keyboard) lists schematic/library files as MIT and PCB files as CC BY-NC. Do not promote either to an MIT board baseline based on the badge.

## Decide permissions per artifact and output

Read the root license, README, artifact directories, per-file notices, linked source projects, and platform-specific author terms. Record terms separately for schematic, PCB, footprints, firmware, artwork, documentation and manufacturing outputs. Record the exact URL and revision used. The project's own MIT license never relicenses copied third-party files.

| Observed terms for the files to be used | Action |
|---|---|
| Explicit MIT for relevant board source | Copy or adapt under the stated terms; retain copyright and license notice in distributed copies or substantial portions. Check separately licensed assets. |
| Attribution/share-alike/open-hardware license | Adapt only if the proposed private use, publication and manufacture fit the actual terms. Preserve attribution and required notices or source obligations in the applicable output; do not call the derivative wholly MIT. |
| Noncommercial, no-repost, author-approval condition, or apparently conflicting page statements | Separate the ability to view or make an authorized private working copy from the ability to publish derivative files, upload them elsewhere, or sell boards. Do not assume one permits the others. If the planned output depends on a right that is unclear or expressly restricted, use a clearer alternative or obtain author permission before that output. |
| Missing license, inaccessible source, or only a clone/download control | No implied reuse grant. Cite for study, consult manufacturer documentation, or choose a clearly licensed baseline. |

OSHWHub pages can contain a displayed open-source license alongside an author restriction such as `未经作者授权，禁止转载` or a platform notice limiting commercial use. The [ESP32 Nano page](https://oshwhub.com/umekoko/esp32-nano), for example, displays GPL 3.0 and a platform statement about learning/research and commercial use. Record the actual wording and do not silently resolve a conflict in favor of broader rights. The agent may use an available clone/export path for an authorized working copy, but must not bundle, publish, or sell copied/derived files on an unverified permission assumption. Reading a reference is distinct from copying its EDA files.

This check establishes a documented decision for the planned artifact; it is not a claim of legal certification. Do not let licensing replace electrical and manufacturing validation.

## Obtain and adapt a working copy

- Prefer `git` or a platform/API export of native files at a recorded commit or revision. If no supported API/CLI exists, use Computer Use for the official site UI's clone/export/download action. Stay within the project's authentication and normal access controls. Download only the selected project into the user's project workspace, not into this skill or a global cache. No purchasing or cart actions follow from source discovery.
- Save source URL, author, retrieved date, commit/revision, license evidence and paths, exported file inventory and archive hash. Keep an untouched source snapshot alongside a separate derivative working copy so every change can be compared. If only screenshots or PDFs are available, mark the source as reference-only.
- Convert formats only when needed. After import into the chosen EDA, compare symbols, pin numbers, nets, footprints, board outline and layer count with the source. Record import losses or unsupported objects. A successful parser or visual preview alone is insufficient.
- Add new features without assuming the base design's power, pin, RF, thermals, mechanical envelope or licensing still apply. Re-run the relevant staged checks in this skill: component and pin review; G2-A placement/format review before wiring; G2-B native net/ERC review; PCB geometry, DRC and sensitive routing; manufacturing outputs and assembly review. Tie the reports to the derivative revision. A cloned board's earlier tests do not prove the changed board.
- If no suitable source passes the fit, permission and editability checks, use exact-part manufacturer references for circuit blocks and continue with a new design. Explain the selected basis and remaining validation work without portraying a candidate as a production-proven board.

For a beginner, report the source choice in plain language: what circuit is reused, what changes, why the permission fits the intended output, and what still must be tested. Keep the full license and comparison evidence in project records.
