# Curriculum Data System

This repo now treats curriculum data as a source-driven system. Website files remain static, but curriculum content should move through the generator path below instead of being hand-edited in generated outputs.

## Source Of Truth

- `curriculum/source/curriculum.v1.json` is the canonical hand-authored curriculum source.
- `curriculum/schema/curriculum.schema.json` is the structural contract for that source file.
- `tools/validate_curriculum.py` validates the canonical source first, then checks generated outputs against it.

The canonical source owns Skill Cards, Power Cards, Integration Cards, Invention Cards, level definitions, asset inventory, preload profiles, lesson-plan profiles, and red-team evidence.

## Generated Artefacts

- `tools/build_curriculum.py` is the only supported path from the canonical source to generated runtime artefacts.
- `curriculum-data.js` is a generated website-compatible mirror for the current static site API.
- `curriculum/generated/*` contains generated review/build artefacts and should not be edited by hand.
- `curriculum/generated/lesson-plans/*` is experimental generated facilitator output. Treat these files as planning aids only; review safety, materials, age fit, and support assumptions before use.
- `reports/validation-results.json` is generated validation output.

Generated files use deterministic output and must not include volatile timestamps.

## Baseline Runtime Scene Data

`power-card-scenes.js` is preserved baseline runtime scene data. It is not yet canonical curriculum data and is not fully generated from `curriculum.v1.json`.

For this phase:

- keep `power-card-scenes.js` hand-reviewable as the current browser runtime baseline;
- let `tools/build_curriculum.py` copy it to `curriculum/generated/browser/power-card-scenes.js`;
- validate that the generated browser scene bundle matches the current baseline file;
- do not implement SVG generation or a scene renderer source model yet.

## Contributor Workflow

1. Edit `curriculum/source/curriculum.v1.json` for curriculum data changes.
2. Rebuild generated artefacts:

   ```bash
   python3 tools/build_curriculum.py
   ```

3. Regenerate experimental lesson plans only when needed:

   ```bash
   python3 tools/generate_lesson_plans.py
   ```

4. Validate source and generated outputs:

   ```bash
   python3 tools/validate_curriculum.py --source curriculum/source/curriculum.v1.json --curriculum-dir curriculum/generated --output reports/validation-results.json
   ```

Do not hand-author `curriculum/generated/*`, root `curriculum-data.js`, or generated lesson-plan files.
