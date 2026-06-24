# Test brief

## Goal

Stress-test whether the schema can support a realistic invention-club curriculum.

Do not design the perfect curriculum first.
Instead, test whether the schema remains coherent as it grows.

## Required test passes

### Pass 1: Toy curriculum

Generate:
- 5 skill families
- 3 levels per family
- 15 power cards
- 5 integration cards
- 3 invention cards

Assess:
- Are families clear?
- Do levels stay within one primary family?
- Are integrations distinguishable from skills?

### Pass 2: Realistic club curriculum

Generate:
- 8 to 12 skill families
- 6 levels per family
- 60 to 100 power cards
- 20 to 40 integration cards
- 10 to 20 invention cards

Assess:
- Does overlap become unmanageable?
- Do dependencies form loops?
- Do some families become too broad or too narrow?
- Do cross-cutting skills like debugging, safety, power and design break the model?

### Pass 3: Red-team test

Try to break the schema with edge cases:
- button-controlled motor
- remote-controlled vehicle
- sensor-controlled robot
- robotic arm
- automatic door
- alarm system
- traffic lights
- tilt-controlled game
- servo-powered puppet
- structure with moving hinge
- debugging a broken circuit
- improving a weak chassis
- choosing a safe battery
- radio-controlled multiplayer game

For each edge case:
- classify it as skill, integration or invention
- list the families involved
- state whether classification feels principled or arbitrary
- identify schema weaknesses

## Final output

Create or update:
- `reports/schema-stress-test.md`
- `curriculum/source/curriculum.v1.json` as the canonical curriculum source
- generated artefacts via `python3 tools/build_curriculum.py`
- `tools/validate_curriculum.py` if validation rules need to change

Do not hand-author `curriculum/generated/*`; those files are generated from the canonical source.

The final report must conclude one of:
- Viable as written
- Viable with amendments
- Not viable at realistic scale

Failure is acceptable.
