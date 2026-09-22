# Idea, functional requirements and component cost

For a new product, follow [beginner decisions](30-beginner-experience.md) before fixing the outline or assembly method. Collect ordinary product preferences, research specialist parameters, then show a concrete plan and component-only cost. After acceptance or explicit delegation, routine sourcing and design proceed without repeated approval requests. For stackup or impedance-related cost choices, use [calculation automation](31-calculation-automation.md); a nominal calculation cannot replace a required fabrication tolerance.

Use for new hardware ideas before detailed schematic drawing, and when a user requests a lower-cost BOM. Resume existing designs without repeating accepted intake. This workflow covers components only and does not authorize ordering.

## From an idea to an initial BOM

1. Translate the idea into a short functional brief: intended use, inputs/outputs, communication, power, controls, firmware behavior and mechanical/assembly needs. Separate confirmed functions, proposed defaults and unresolved choices. Ask only about choices that materially affect function or architecture. Do not add optional features to the required baseline or quietly remove requested features.
2. Map each function to hardware blocks and candidate parts. Include support components: decoupling, bias/pull resistors, clocks, programming/recovery, protection, connectors, switches and indicators where required. Distinguish a bare IC from a module and count required external parts. State assumptions instead of claiming the preliminary BOM is final.
3. Establish build quantity, explicit budget if provided and spare quantities. If no build quantity is given, state an initial estimate for one board and zero added spares; these are quotation assumptions, not fixed product requirements. Do not ask for a budget merely to begin. If costs depend heavily on unresolved options, show alternatives separately rather than adding mutually exclusive architectures together.
4. Query **立创商城** for exact selectable parts and present a component-only estimate before beginning detailed schematic work. Show the estimate during the conversation so the user can steer it. Do not invent a mandatory approval pause for an otherwise authorized design. A stated hard budget that cannot be met or a material functional tradeoff does require a decision before committing to that choice; continue independent work meanwhile.

Maintain the functional requirements in the project baseline and reference 25's requirement mapping. A price target supplements functional requirements; it does not replace them.

## Obtain current quotes

Use a currently available read-only distributor search/API or the official product pages. A browser is a fallback if a usable API is unavailable; never invent private endpoints or switch to purchasing actions. In this workflow, use the user's requested 立创商城 market first. A different regional LCSC listing can have different stock, tax, currency and MOQ; label it separately and do not silently substitute it for a domestic quote.

For every selected SKU record the full manufacturer part number, supplier code, package, important specifications, exact product URL, query timestamp with timezone, observed stock, MOQ, order increment and price tiers. Capture the price for the actual order quantity, not a search result's advertised lowest tier. Normalize packaging: a reel/pack price is not a per-piece price. Confirm whether the order increment is counted from zero or uses another supplier rule; the helper below supports zero-based multiples only.

Use one currency and one explicit tax basis per table. Do not mix currency/tax assumptions to create a lower total. Preserve raw observation or a local query note with its source. Read electrical compatibility from exact-part manufacturer sources; the shop's specification summary alone cannot approve a replacement.

If a login, regional restriction or missing field prevents a quote, mark the item unpriced or its stock/MOQ unknown, retain what was observed and explain the gap. Do not invent a price or use zero. Display a known subtotal and missing rows; never label it the full total. Stock is a point-in-time observation, not a reservation. Refresh quotes at final BOM freeze and before the user orders; do not claim an arbitrary cache lifetime guarantees availability.

## User-facing table and arithmetic

Use the user's language. A Chinese table can use:

| 功能/元件 | 型号 · 立创编号 | 关键规格/封装 | 单板用量 | 起订量/倍数 | 实购数量 | 对应单价 | 采购小计 | 库存/来源 |
|---|---|---|---|---|---|---|---|---|

List only electronic/electromechanical parts needed by the device, including required switches, connectors or batteries if in scope. Keep PCB fabrication, assembly, stencil, shipping, tools, enclosure production and software fees out of this table and these totals. State the scope in one sentence. Mark any user-supplied/existing parts separately rather than pretending their replacement value or purchase price is zero.

Give two clearly labeled totals, both based on the same queried price tier:

- **Single-board component consumption cost:** sum of per-board fitted quantities times the applicable unit prices. It is not the checkout amount.
- **Actual component purchase amount for N boards:** sum of rounded purchase quantities times their applicable unit prices, including explicitly selected spares and MOQ surplus.

For an aggregated SKU, `need = boards * per_board + spares`; `buy = ceil(max(need, MOQ) / order_multiple) * order_multiple`. Choose the highest observed tier threshold no greater than `buy`. Check stock against `buy`, not the smaller fitted quantity. Combine identical SKUs before selecting price tiers. Keep mutually exclusive alternatives and DNP parts out of the selected total. Preserve exact decimal arithmetic; display totals with the currency's normal precision and note that checkout rounding or later prices may differ.

The minimal-quantity estimate does not search every larger tier. When investigating costs, a larger order can sometimes cost less in total; compare it as an explicit extra-purchase option and show the surplus. Do not increase build quantity, add unrequested spares or change the currency to make an estimate appear cheaper.

## Cost reduction without functional loss

When the user asks for lower cost or lower MOQ:

1. Preserve the confirmed feature/performance baseline and quantify both per-board consumption cost and actual purchase amount. If they conflict, show the tradeoff; for a one-board prototype, small-order cash outlay is usually the useful default objective.
2. Search equivalent-specification alternatives, lower-MOQ SKUs and packaging. Combine genuinely interchangeable values/packages where their electrical roles allow it. Compare total supporting BOM costs when changing a module, regulator or MCU; a cheaper chip can require extra flash, RF, clocks or protection.
3. Verify replacements against exact-part sources and the actual circuit. Present old/new part numbers, compatibility conclusions, quantity/MOQ, unit price, total savings and necessary design changes. Prefer verified drop-in equivalents when savings are similar.
4. Apply verified substitutions within the authorized optimization scope and re-run affected selection, pin, footprint, electrical, layout and firmware compatibility checks. Distinguish an electrically suitable alternative that needs board changes from a pin-compatible substitute. Do not call it a drop-in replacement without verification.
5. If preserving requirements cannot meet the requested budget, report the lowest verified estimate and its limits. Present any feature reduction or performance downgrade as a separate proposal with explicit impact and savings; apply it only after the user explicitly accepts it. A generic request to reduce cost does not authorize it.

Relevant comparison fields include:

| Family | Preserve and verify as applicable |
|---|---|
| Capacitor | Capacitance, tolerance, rated voltage/derating, dielectric, effective capacitance under bias, ESR/ripple, temperature, package |
| Resistor | Resistance, tolerance, power/voltage rating, temperature coefficient, pulse duty, package |
| MCU/module | Required interfaces and usable pins, RAM/flash and real software needs, USB/radio features, throughput/timing, boot/recovery, power/logic levels, pinout/package, toolchain and library support |
| Power/protection/connector | Operating ranges, load/transients, losses/thermal limits, protection behavior, polarity/pinout, mechanical mating and assembly needs |

A lower maximum datasheet rating may still satisfy a documented design requirement with its margins. Record that comparison instead of demanding identical catalog numbers. Unproven equivalence remains a candidate, not an accepted replacement. Do not remove decoupling, protection, test access or recovery circuitry simply to save their cost.

## Final reconciliation

At G5, regenerate the fitted BOM from the actual design. Compare every selected manufacturer part, supplier SKU, package, quantity and DNP decision against the estimate; resolve missing support parts or duplicate groups. Re-query price, stock, MOQ and order increments for the final build quantity. Label the estimate preliminary/revised/final and bind it to the current requirement/design baseline. Keep old/new totals and reasons for changes in the project record. A complete price table does not establish that the hardware design is complete.

## Reproducible calculator

`scripts/component_cost.py` takes observed quote data and emits JSON. It neither queries a shop nor verifies compatibility or performs checkout. Exit 0 means every declared row is quoted with sufficient declared stock; exit 1 means missing prices or unknown/insufficient stock; exit 2 indicates invalid input. With a missing price, full totals are null and only known subtotals are emitted. With known prices but insufficient stock, totals remain quoted arithmetic and status stays INCOMPLETE.

```sh
python scripts/component_cost.py --input /project/component-quotes.json
```

Input schema:

- Top level: `schema: 1`, `baseline_id`, positive integer `board_quantity`, `currency` (normally `CNY` for domestic quotes), `tax_basis` (`included` or `excluded`), nonempty `parts`.
- Each part: `id`, `function`, `mpn`, unique aggregated `supplier_code`, `package`, `spec`, positive integer `qty_per_board`, optional nonnegative integer `spares` (default 0), `quote` (null if unavailable).
- Quote: exactly `url` (HTTPS), `queried_at` (ISO timestamp with timezone), `stock` (nonnegative integer or null), positive integers `moq` and `multiple`, matching `currency` and `tax_basis`, `price_unit: "piece"`, and nonempty `tiers`.
- Tier: `min_qty` (positive integer) and `unit_price` (nonnegative decimal string, up to eight fractional digits, in currency per individual component).

Keep unresolved MOQ or pack conversion as `quote: null` until verified; the calculator cannot safely infer order quantities. Use separate estimates for different tax/currency markets. Existing inventory, coupons, shipping and checkout-specific discounts need separately documented accounting; this helper does not model them. Input completeness and source accuracy remain Agent review responsibilities.

## Structured substitution review

Before applying cost substitutions, run `review_substitutions.py` against a project-local `substitution-review.json`. This adds a reproducible completeness check; it does not infer electrical equivalence or replace the engineering comparison above.

```sh
python scripts/review_substitutions.py --root /project --requirements requirements.json --review substitution-review.json
```

Review schema: `schema: 1`, matching `project_id`/`baseline_id`, `requirements_digest` (canonical digest of requirements.json), `reviewer`, and `change_scope`. Include:

- `requirements`: one assessment per declared requirement, with `requirement_id`, `status`, `reason`, and nonempty hashed local `sources`. Unaffected requirements use UNCHANGED with a reason; do not omit them.
- `impacts`: the same assessment structure using `area` instead of requirement_id, covering `electrical`, `pinout`, `footprint`, `firmware`, `mechanical`, and `supporting_bom`.
- Assessment status is MEETS, UNCHANGED, UNKNOWN or DOES_NOT_MEET. Unknown/unmet/missing assessments block completion. For an accepted functional change, update the sourced requirement baseline explicitly and reassess; a request to save cost alone does not permit it.
- `before` and `after`: each has the selected `supplier_code`, a `quote_file: {path, sha256}` pointing to a complete estimate in the calculator schema, and `observations`, an array of hashed observation JSON files for every SKU in that estimate. Compare full supporting BOM totals using identical build quantity, currency and tax basis. Explain changed quantities, added and removed parts in supporting_bom; a cheaper bare IC may increase system cost.

Each observation JSON records `supplier_code`, exact `mpn`, the complete normalized `quote` object (including URL and timestamp), and `raw_source: {path, sha256}` pointing to the saved actual distributor response, page capture or source note. Keep original observations separate from derived quote fields. The checker requires exact correspondence between estimate and retained observation, including stock/MOQ/tiers. It cannot establish that a captured page is authentic or that prices remain current; refresh them before final release.

Also include `bom_changes`: one record for every changed SKU, containing `supplier_code`, exact `before` and `after` projections (or null when added/removed), `reason` and nonempty hashed `sources`. Each projection contains `mpn`, `package`, `spec`, `qty_per_board` and `spares` (default 0). The checker derives the delta independently and rejects contradictory or missing reviews. `supporting_bom: UNCHANGED` cannot cover a real BOM change. A lower total spare count requires a separate `spares_decision: {path, sha256}` referencing the user's explicit decision; it must not be hidden as a cheaper equivalent part. The output includes the actual BOM delta so quantity savings stay visible.

Exit 0 means REVIEW_RECORD_COMPLETE, 1 means BLOCKED, and 2 means invalid/stale input. The report gives before/after purchase totals and savings; a negative saving remains visible. A complete record does not automatically apply a replacement or assert drop-in compatibility. Inspect manufacturer sources, reasons and supporting-part changes, then re-run affected electrical, footprint, PCB and firmware checks after implementation.
