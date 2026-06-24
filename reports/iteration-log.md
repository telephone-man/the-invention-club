# Iteration Log

## Iteration 1 - Supporting Families

- Weakest evidence: realistic level containment was exactly 64/80 and several leaky examples were caused by cross-family dependencies rather than unclear primary objectives.
- Smallest amendment: add optional `supporting_families` and `classification_rationale`; allow cross-family dependencies when the I can statement, success condition and debug prompts remain inside the primary family.
- Generated examples changed: `r_dbg_04`, `r_des_06`, `r_pow_04`, and `r_pow_08`.
- Validation command: `python3 tools/validate_curriculum.py --curriculum-dir curriculum/generated --output reports/validation-results.json`.
- Result: mechanical validation still passed; realistic clear primary-family rate improved from 67/80 to 69/80; inside-family level rate improved from 64/80 to 68/80.
- What got worse: schema complexity increased slightly because cards can now carry supporting-family metadata.
- Judgement: essential amendment. It preserves one primary family while making cross-family dependencies auditable.

## Iteration 2 - Improve Level Tie-Breaker

- Weakest evidence: Improve-level cards were making Debugging/Testing overlap with Movement, Structures, Power, Sensing, Control/Input and Logic/Sequencing.
- Smallest amendment: define Improve inside a family as improving that family's own object of study; reserve Debugging/Testing as primary when the transferable diagnostic method is the main learning objective.
- Generated examples changed: `r_mov_07`, `r_ctl_08`, `r_sen_08`, `r_str_07`, `r_pow_07`, `r_log_07`; red-team cases `debugging a broken circuit` and `improving a weak chassis`.
- Validation command: `python3 tools/validate_curriculum.py --curriculum-dir curriculum/generated --output reports/validation-results.json`.
- Result: mechanical validation still passed; realistic clear primary-family rate improved from 69/80 to 74/80; inside-family level rate improved from 68/80 to 74/80; arbitrary red-team cases fell from 4/14 to 2/14.
- What got worse: the schema now has a specific Improve rule that facilitators must learn.
- Judgement: essential amendment. Without it, level 6 collapses too easily into Debugging/Testing.

## Iteration 3 - Mechanism and Openness Tie-Breakers

- Weakest evidence: remaining arbitrary red-team cases were `robotic arm` and `structure with moving hinge`; remaining borderline cards involved passive mechanisms, control interfaces, remote command meaning, subsystem testing, and invention scoping.
- Smallest amendment: add tie-breakers for passive Structures versus active Movement, human-facing Control/Input, Communication message meaning, and fixed Integration versus open Invention.
- Generated examples changed: `r_ctl_04`, `r_ctl_07`, `r_str_04`, `r_com_05`, `r_dbg_06`, `r_des_08`; red-team cases `robotic arm` and `structure with moving hinge`.
- Validation command: `python3 tools/validate_curriculum.py --curriculum-dir curriculum/generated --output reports/validation-results.json`.
- Result: mechanical validation still passed; realistic clear primary-family rate improved from 74/80 to 80/80; inside-family level rate improved from 74/80 to 80/80; arbitrary red-team cases fell from 2/14 to 0/14.
- What got worse: the schema now depends on explicit tie-breaker rules, so it is no longer as minimal as the original.
- Judgement: essential amendment. It materially strengthens facilitator classification without changing the core skill/integration/invention model.

## Stop Condition

Stopped after iteration 3 because the target evidence threshold was met: clear primary-family rate is at least 90%, inside-family level rate is above 85%, and arbitrary red-team classifications are no more than 1/14.
