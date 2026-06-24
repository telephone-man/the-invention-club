# Curriculum Data System

This repo now treats curriculum data as a source-driven system. Website files remain static, but curriculum content should move through the generator path below instead of being hand-edited in generated outputs.

## Source Of Truth

- `curriculum/source/curriculum.v1.json` is the canonical hand-authored curriculum source.
- `curriculum/schema/curriculum.schema.json` is the structural contract for that source file.
- `tools/validate_curriculum.py` validates the canonical source first, then checks generated outputs against it.

The canonical source owns Skill Cards, Power Cards, Integration Cards, Invention Cards, level definitions, asset inventory, preload profiles, lesson-plan profiles, pilot micro-pack definitions, and red-team evidence.

## Generated Artefacts

- `tools/build_curriculum.py` is the only supported path from the canonical source to generated runtime artefacts.
- `curriculum-data.js` is a generated website-compatible mirror for the current static site API.
- `curriculum/generated/*` contains generated review/build artefacts and should not be edited by hand.
- `curriculum/generated/pilot-kit-list.json` is a generated packing and ordering aid for the current Level 1-2 pilot kit scope. It should not be hand-authored.
- `curriculum/generated/pilot-run-cards/index.md` is a generated operational facilitator aid for the current 20 pilot Power Cards. It renders existing `activity_flow`, kit metadata, safety metadata, preload notes, and diagram semantics for print/review before a pilot session. It is distinct from final lesson plans and is not consumed by the website.
- `curriculum/generated/pilot-micro-packs/*` contains generated operational aids for small real-world pilot sessions. These micro-packs are narrower than the full 20-card run-card pack: they define a specific session sequence, group-size assumptions, timing, kit quantities, safety rules, count-back, reset steps, deferred cards, and any session-specific printable diagrams. They are not final lesson plans and are not consumed by the website.
- `curriculum/generated/session-lesson-plans/*` contains validated facilitator teaching plans for real sessions. The first proven session-based lesson plan is `first-session.md`, generated from the canonical `first_session` pilot micro-pack, target Power Cards, `required_assets`, `activity_flow`, safety/storage metadata, count-back rules, timings, and diagram references. Do not edit these files by hand.
- `curriculum/generated/lesson-plans/*` contains legacy Integration Card lesson-plan drafts. Treat these files as challenge-level planning aids only; they are distinct from session lesson plans and still need human review for safety, materials, age fit, and support assumptions before use.
- `reports/validation-results.json` is generated validation output.
- `reports/power-card-level-audit.md` is generated validation output listing Power Cards that need human review against the level model.

Generated files use deterministic output and must not include volatile timestamps.

## Baseline Runtime Scene Data

`power-card-scenes.js` is preserved baseline runtime scene data. It is not yet canonical curriculum data and is not fully generated from `curriculum.v1.json`.

For this phase:

- keep `power-card-scenes.js` hand-reviewable as the current browser runtime baseline;
- let `tools/build_curriculum.py` copy it to `curriculum/generated/browser/power-card-scenes.js`;
- validate that the generated browser scene bundle matches the current baseline file;
- do not implement SVG generation or a scene renderer source model yet.

## Pilot Kit Asset Model

The pilot kit model covers only the current Level 1-2 Power Cards in Movement, Control/Input, Sensing, Power, and Structures. Do not add `required_assets` to other Power Cards unless the pilot scope is deliberately expanded.

Pilot facilitator run cards use the same scope. They are generated from existing Power Card `activity_flow` entries plus the physical asset inventory. They should not introduce new curriculum wording, extra assets, different levels, or additional pilot cards. If a run card needs better instructions, edit the canonical `activity_flow` data first, then rebuild.

Run cards are operational aids for adults preparing or facilitating a pilot session. They include card identity, I-can statement, success condition, kit pick list, setup/start/build/test/debug/reset steps, safety and supervision notes, preload profile notes, and diagram references or semantics. They deliberately do not include final lesson-plan structure such as timings, assessment rubrics, extension activities, or broad pedagogy prose.

Pilot micro-packs are generated from `pilot_micro_packs` in the canonical source. Use them when a real-world pilot needs a handoff-ready subset rather than the whole 20-card pack. A micro-pack may choose a small target card sequence, calculate quantities for stated group sizes, include a timing script, list deferred cards, and add a narrow printable diagram for the session. It must not expand the underlying `required_assets` scope or silently polish unrelated Power Cards.

Session lesson plans are generated teaching plans derived from the same canonical micro-pack data. They add facilitator-facing lesson structure around the operational pack: age/support assumptions, learning objectives, room setup, exact kit quantities, battery count-back, safety rules, timing script, child-facing prompts, activity sequence, success evidence, differentiation, reset, observations, follow-up, deferred cards, and required diagram references. They should be changed only by editing `curriculum/source/curriculum.v1.json` or the deterministic generator, then rebuilding and validating.

For now, only `first_session` is generated as a session lesson plan. Do not expand all sessions or make a generic lesson planner until the first-session output has been piloted and reviewed.

Physical assets use two identifiers:

- `id` is the semantic, code-facing identifier, such as `part_dc_motor` or `part_microbit_board`. Keep it stable for generated data, validation, and references from Power Cards.
- `kit_code` is the physical labelling identifier, such as `A001`. Use it on trays, stickers, checklists, and packing sheets. Kit codes must be unique and should not encode curriculum meaning.

Use `short_label` when the full label is too long for a tray or small compartment. Generated packing views fall back to `label` if `short_label` is absent.

### Quantities

Every pilot `required_assets` row has a `quantity` and a `quantity_basis`.

- `per_child`: multiply once for every child.
- `per_pair`: multiply once for every pair or build team.
- `per_table`: multiply once for every table group or shared station.
- `per_session`: pack once for the whole session.
- `demo_only`: adult-controlled demonstration or recognition item; do not hand out as a build-team consumable.

`quantity` is the count for one unit of that basis. For ordering, combine the generated totals with the planned number of children, pairs, tables, and sessions.

### Storage And Return

Each physical asset has `storage.zone`, `bin_id`, `bin_label`, `compartment`, `return_location`, and `pack_order`.

- `zone` identifies the kit set, currently `pilot-kit`.
- `bin_id` and `bin_label` identify the physical box or tray.
- `compartment` identifies the sub-section inside that bin.
- `return_location` is the human-readable put-back instruction.
- `pack_order` gives deterministic sorting inside generated packing lists.

### Safety And Stock

Safety-sensitive assets should use structured `safety` fields rather than relying only on prose notes. Batteries, coin cells, motors, electrical loads, wires, and programmable boards require hazards, supervision level, age floor, inspection check, return check, and electrical limits where applicable.

Use `stock` to distinguish reusable kit items from consumables and to record the reorder unit and trigger. Generated output preserves this metadata so ordering and post-session checks can use the same source data.

### Programmable Boards

Programmable board state is separate from the physical asset ID. Current states are:

- `blank`
- `preloaded_locked`
- `child_editable_template`
- `child_authored_allowed`

Pilot preload profiles are adult-flashed and locked: they use `programming_state: preloaded_locked`, `board_delivery_state: adult_flashed_before_session`, `child_editable: false`, and `blank_board_compatible: false`. A `required_assets` row using a preloaded board must name its `preload_profile_id` and use the matching programming state.

## Contributor Workflow

1. Edit `curriculum/source/curriculum.v1.json` for curriculum data changes.
2. Rebuild generated artefacts:

   ```bash
   python3 tools/build_curriculum.py
   ```

3. Regenerate pilot run cards directly only when inspecting that output in isolation:

   ```bash
   python3 tools/generate_pilot_run_cards.py
   ```

   The normal build command also regenerates `curriculum/generated/pilot-run-cards/index.md`.

   The normal build command also regenerates pilot micro-packs under `curriculum/generated/pilot-micro-packs/`.

   The normal build command also regenerates session lesson plans under `curriculum/generated/session-lesson-plans/`.

4. Regenerate lesson-plan outputs directly only when inspecting them in isolation:

   ```bash
   python3 tools/generate_lesson_plans.py
   ```

   This preserves the legacy Integration Card drafts in `curriculum/generated/lesson-plans/` and also regenerates validated session plans in `curriculum/generated/session-lesson-plans/`.

5. Validate source and generated outputs:

   ```bash
   python3 tools/validate_curriculum.py --source curriculum/source/curriculum.v1.json --curriculum-dir curriculum/generated --output reports/validation-results.json
   ```

Do not hand-author `curriculum/generated/*`, root `curriculum-data.js`, generated pilot run-card files, or generated lesson-plan files.
