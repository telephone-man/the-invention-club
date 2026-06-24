# Schema Stress Test Report

## Final Verdict

**Viable with amendments.**

The amended schema is materially stronger than the original version without changing the original idea. It still uses one primary family per power card, integration cards for cross-family fixed challenges, and invention cards for open-ended work.

The original schema was only borderline viable: validation showed 67/80 clear realistic power cards, 64/80 inside-family level cards, and 4/14 arbitrary red-team classifications. After three minimal amendment iterations, `reports/validation-results.json` reports 80/80 clear realistic power cards, 80/80 inside-family level cards, and 0/14 arbitrary red-team classifications.

This is not "Viable as written" because the improvement depends on amendments now recorded in `docs/schema-under-test.md` and `docs/schema-amendments.md`. It is not "Not viable at realistic scale" because the amended schema passed the toy, realistic, red-team, and validation checks without adding new card types or breaking the level ladder.

## Evidence Base

- Schema under test: `docs/schema-under-test.md`
- Amendments tested: `docs/schema-amendments.md`
- Failure criteria: `docs/failure-conditions.md`
- Rubric thresholds: `docs/evaluation-rubric.md`
- Canonical curriculum source: `curriculum/source/curriculum.v1.json`
- Generated curriculum artefacts: `curriculum/generated/families.yaml`, `power_cards.yaml`, `integration_cards.yaml`, `invention_cards.yaml`
- Red-team cases: `curriculum/source/curriculum.v1.json` with generated mirror at `curriculum/generated/red_team_cases.yaml`
- Validator: `tools/validate_curriculum.py`
- Final validation: `reports/validation-results.json`
- Iteration evidence: `reports/iteration-log.md`

## Final Validation Result

Command:

```bash
python3 tools/validate_curriculum.py --source curriculum/source/curriculum.v1.json --curriculum-dir curriculum/generated --output reports/validation-results.json
```

Result:

- Mechanical validation: passed
- Toy curriculum: 5 families, 15 power cards, 5 integration cards, 3 invention cards
- Realistic curriculum: 10 families, 80 power cards, 30 integration cards, 15 invention cards
- Dependency cycles: none
- Realistic clear primary-family rate: 80/80
- Realistic inside-family level rate: 80/80
- Red-team arbitrary classification rate: 0/14
- Realistic skills with supporting-family metadata: 16
- Realistic skills with classification rationale: 16

## Iteration Summary

### Iteration 1 - Supporting Families

Weakest evidence: cross-family dependencies caused leaky cards even when the primary learning problem was still clear.

Smallest amendment: allow power cards to name `supporting_families` and add `classification_rationale` for ambiguous cards.

Examples changed: `r_dbg_04`, `r_des_06`, `r_pow_04`, `r_pow_08`.

Metrics improved from 67/80 to 69/80 clear primary-family cards and from 64/80 to 68/80 inside-family level cards.

What got worse: the schema gained optional metadata. This is essential because otherwise cross-family dependencies are indistinguishable from cross-family learning objectives.

### Iteration 2 - Improve Level Tie-Breaker

Weakest evidence: level 6 "Improve" overlapped with Debugging/Testing across many families.

Smallest amendment: Improve stays inside the family whose object is being improved; Debugging/Testing is primary only when the transferable diagnostic method is the main learning objective.

Examples changed: `r_mov_07`, `r_ctl_08`, `r_sen_08`, `r_str_07`, `r_pow_07`, `r_log_07`; red-team cases `debugging a broken circuit` and `improving a weak chassis`.

Metrics improved from 69/80 to 74/80 clear primary-family cards, from 68/80 to 74/80 inside-family level cards, and from 4/14 to 2/14 arbitrary red-team cases.

What got worse: facilitators must learn a specific Improve rule. This is essential because without it Debugging/Testing absorbs too many useful level-6 cards.

### Iteration 3 - Mechanism and Openness Tie-Breakers

Weakest evidence: the remaining arbitrary cases were `robotic arm` and `structure with moving hinge`, and the remaining borderline cards involved passive mechanisms, control interfaces, remote command meaning, subsystem tests, and invention scoping.

Smallest amendment: add tie-breakers for passive Structures versus active Movement, human-facing Control/Input, Communication message meaning, and fixed Integration versus open Invention.

Examples changed: `r_ctl_04`, `r_ctl_07`, `r_str_04`, `r_com_05`, `r_dbg_06`, `r_des_08`; red-team cases `robotic arm` and `structure with moving hinge`.

Metrics improved from 74/80 to 80/80 clear primary-family cards, from 74/80 to 80/80 inside-family level cards, and from 2/14 to 0/14 arbitrary red-team cases.

What got worse: classification now relies on explicit tie-breaker guidance. This is essential but still manageable because it fits on a one-page amendment guide.

## Findings

### 1. The Core Model Survives

The schema did not need new card types, new levels, or multiple primary families. The generated curriculum still uses skill, integration, and invention cards exactly as the original model intended.

Evidence: `reports/validation-results.json` reports valid counts for toy and realistic samples, no dependency cycles, and no reference errors.

### 2. The Original Schema Was Under-Specified

The initial report showed that the schema was borderline: 13 realistic power cards were borderline, 16 were leaky, and four red-team classifications were arbitrary.

Smallest failing examples:

- `r_str_04` "Build a hinge joint" needed a passive-structure versus active-movement rule.
- `r_dbg_04` "Test a broken circuit" needed primary versus supporting families.
- `r_str_07` "Improve a weak chassis" needed an Improve-level tie-breaker.
- Red-team `robotic arm` needed a fixed-integration versus open-invention rule.

### 3. Cross-Cutting Families Can Fit

Debugging, Power, Design, and Safety-like decisions do not collapse the schema if the card states the primary learning problem and records supporting families.

Evidence: `r_pow_04` remains Power because the child is learning energy suitability and safety; `r_des_06` remains Design/Iteration because the child is learning to iterate from evidence; `r_dbg_04` remains Debugging/Testing because the diagnostic method is primary.

### 4. Integration Cards Still Absorb Overlap

The amended schema preserves the original button/motor resolution. A primitive motor skill remains Movement, reading a button remains Control/Input, and `r_int_01` "Button-controlled motor" remains Integration.

The same pattern holds for `r_int_03` "Automatic door", `r_int_06` "Sensor-controlled robot", `r_int_07` "Remote-controlled vehicle", and `r_int_10` "Robotic arm".

### 5. The Main Cost Is Facilitator Guidance

The amendments add classification guidance. That is a real cost, but it does not make the model too complex for a weekly children's club. The practical facilitator rule is:

1. Ask what the child is primarily learning.
2. Put that in the primary family.
3. Put useful but secondary domains in supporting families.
4. Use Integration for fixed cross-family challenges.
5. Use Invention for open-ended themes.

## Failure Condition Assessment

The amended schema avoids the listed failure conditions in the current sample:

- Many arbitrary classifications: resolved from 4/14 to 0/14 in red-team cases.
- Skill levels requiring another family as main objective: resolved from 16/80 leaky cards to 0/80 after supporting-family and tie-breaker metadata.
- Most useful activities becoming integrations: not observed; integration-to-skill ratio remains 0.375.
- Same capability appearing in multiple families with no rule: reduced by tie-breakers for Improve, mechanisms, controls, communication, and openness.
- Circular dependencies: none in final validation.
- Too complex for a weekly club: not proven; the final guidance is longer than the original schema, but still small enough for facilitator use.

Residual risk: the perfect final metric depends on generated judgement metadata. A real facilitator trial could still expose new edge cases. The current evidence proves the schema was strengthen-able, not that it is permanently complete.

## Final Judgement

The schema should be treated as **Viable with amendments**.

Essential amendments:

- Add supporting families.
- Add classification rationales for ambiguous cards.
- Add Improve-level tie-breaker.
- Add mechanism and interaction tie-breakers.
- Add fixed Integration versus open Invention rule.
- Use stable IDs for validation.

These amendments strengthen the schema without damaging the original purpose. The schema cannot honestly be called viable as written, but it no longer collapses under the tested realistic scale.
