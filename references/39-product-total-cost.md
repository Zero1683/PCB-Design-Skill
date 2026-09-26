# Product total cost and what payment buys

Use this when proposing a new device, comparing bare PCB and PCBA quotes, or handing a beginner an ordering plan. A component price is only one part of the cash needed to make the object usable. Record both `delivery` (what the selected PCB or PCBA quote supplies) and `target_delivery` (what the user is trying to make): `bare_pcb`, `assembled_pcb`, or `usable_device`. A bare-board quote can be combined with separately bought parts and self or outsourced soldering to reach a working object. Say plainly what each payment supplies. A fitted board is not evidence that firmware and functions work.

Build one bill for the chosen quantity and design revision. Include each applicable charge: component purchase, PCB fabrication, assembly, stencil, shipping, battery, enclosure, tools, and software/API usage. In `required_costs`, name the optional categories the actual product needs. In `not_required_costs`, give a reason for each absent optional category; an unconsidered category keeps the total unresolved. Distinguish an existing tool or part from a free new purchase. If a price is missing, show a known subtotal and missing items; do not call that subtotal the total or turn unknown into zero. Use explicit zero only when a quote or other source establishes no charge.

For a PCBA bundle, list exactly which of `pcb_fabrication`, `assembly`, and `components` the price covers. If it includes components, do not add the separate component purchase estimate. If components are bought separately, use the [component cost calculator](26-component-cost-planning.md) report and exclude components from every bundle. The calculator rejects overlapping core coverage. A `bare_pcb` quote cannot bundle fabrication with fitted parts or assembly in the same line, but separate parts and soldering charges belong in the whole-product plan. An `assembled_pcb` or `usable_device` quote must include fabrication and assembly together; otherwise call the quote `bare_pcb` and list assembly separately. Multiple shipping or tool charges may be separate line items when they are genuinely separate purchases. Amounts must be for the **entire chosen build lot**, in one currency and one tax basis, with quote source and contents stated.

`scripts/product_total_cost.py` combines a declared cost plan with the JSON output of `scripts/component_cost.py`. It does not fetch prices or prove that a vendor will deliver a working object. Exit 0 means every *declared required* category has a known price; exit 1 means missing price or coverage; exit 2 means invalid or conflicting input. A complete declared estimate still needs an Agent review for costs the plan forgot.

```sh
python3 scripts/component_cost.py --input /project/component-quotes.json > /project/component-cost.json
python3 scripts/product_total_cost.py --input /project/product-cost.json --component-report /project/component-cost.json > /project/product-total.json
```

Omit `--component-report` only when the target is bare boards without purchased components or when a bundle includes them. For bare boards that will later be assembled from separately bought components, supply the component report. The input is a JSON object:

```json
{
  "schema": 1,
  "baseline_id": "RevA",
  "board_quantity": 2,
  "currency": "CNY",
  "tax_basis": "included",
  "delivery": "bare_pcb",
  "target_delivery": "usable_device",
  "components": "separate_purchase",
  "required_costs": ["battery", "enclosure", "tools", "software_api"],
  "not_required_costs": {"stencil": "hand soldering; no paste printing"},
  "line_items": [
    {"id": "pcb-order", "covers": ["pcb_fabrication"], "amount": null, "timing": "batch", "description": "Two bare PCBs; no parts or assembly", "source": "quote link or local screenshot/date", "currency": "CNY", "tax_basis": "included"},
    {"id": "assembly-order", "covers": ["assembly"], "amount": null, "timing": "batch", "description": "Fit components on two boards; parts bought separately", "source": "quote link or local screenshot/date", "currency": "CNY", "tax_basis": "included"}
  ]
}
```

Add a line for shipping and each required item before calling it complete. `amount` is a nonnegative decimal string for the whole lot or `null` when unknown. `timing: batch` is charged again for an identical future lot; `one_time` applies to the first purchase, such as a reusable tool. `components` is `separate_purchase`, `included_in_bundle`, or `not_in_delivery` (bare PCB **target** only). For `included_in_bundle`, a line must cover `components`; a turnkey PCBA line may cover all three core categories. `required_costs` adds actual product-specific needs to the **target** level's minimum categories. Each of `stencil`, `battery`, `enclosure`, `tools`, and `software_api` must be covered by a line, required, or explained in `not_required_costs`. That object may be `{}` while decisions are pending; the full total then remains unknown. Keep mutually exclusive quotes in separate plans.

The report distinguishes `first_cash_outlay_total` from `repeat_batch_total_at_quantity`, and divides each by the stated board quantity for comparison. The repeat figure only removes declared one-time charges; it is not a future price prediction. It does not amortize tooling over an invented production volume. If any required charge is unknown, these four full totals are `null`; use the known subtotals and the `issues` list instead. Record any already-owned material/tool and any unpriced firmware, test or labor work next to the estimate. At handoff, report what can actually be ordered now, what will arrive, and what is still needed for the user's intended product.
