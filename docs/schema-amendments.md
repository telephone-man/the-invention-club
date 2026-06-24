# Schema Amendments Tested

## Verdict

The schema is materially stronger with amendments. The original idea remains intact: a curriculum is still a map of skill families, power cards still have one primary family, integrations still combine power cards from different families, and inventions still invite open-ended use of unlocked skills.

The amendments are not optional polish. They are needed to stop cross-cutting skills, mechanisms, and open-ended projects from being classified by facilitator preference alone.

## Essential Amendments

### 1. Supporting Families

Power cards keep one primary family, but may list `supporting_families` when another family supplies context, tools, materials, or prerequisite knowledge.

Rule tested: a skill remains inside its primary family when its I can statement, success condition, and main debug prompts are about that family's learning problem.

Evidence: after adding this rule, `r_dbg_04`, `r_des_06`, `r_pow_04`, and `r_pow_08` could be classified without pretending their cross-family dependencies were the main learning objective.

### 2. Classification Rationale

Ambiguous cards should include a short `classification_rationale`.

Rule tested: the rationale must say why the primary family was chosen, not merely repeat the family name.

Evidence: `tools/validate_curriculum.py` now checks optional rationale fields are non-empty, and `reports/validation-results.json` reports 16 realistic power cards with classification rationales.

### 3. Improve Level Tie-Breaker

Improve inside a family means improving that family's own object of study.

Debugging/Testing is primary only when the transferable diagnostic method is the main learning objective. It is supporting when the child is mainly improving motion, structure, power, sensing, input, communication, or sequencing.

Evidence: this resolved `r_mov_07`, `r_ctl_08`, `r_sen_08`, `r_str_07`, `r_pow_07`, and `r_log_07`, and made the red-team cases `debugging a broken circuit` and `improving a weak chassis` principled.

### 4. Mechanism and Interaction Tie-Breakers

Passive joints, mounts, and load-bearing parts are Structures when the main problem is support, alignment, range, or strength.

Actuated or controlled travel is Movement when the main problem is making motion happen predictably.

Human-facing controls are Control/Input when the main problem is how a person provides a command or value.

Message sending, addressing, and command meaning are Communication when the main problem is getting the right information from sender to receiver.

Evidence: this resolved `r_str_04`, `r_ctl_04`, `r_ctl_07`, and `r_com_05`.

### 5. Integration Versus Invention Openness Rule

Fixed challenge plus named required power cards is Integration.

Open-ended theme with multiple acceptable solution paths is Invention.

The same topic may appear in either form; classify the curriculum card by how much choice the child has, not by the finished object.

Evidence: this made the red-team `robotic arm` case principled as an integration when fixed, while preserving open-ended radio-game prompts as invention cards.

### 6. Stable IDs

Every card should have a stable `id` so dependencies and integration prerequisites can be checked without relying on titles.

Evidence: `tools/validate_curriculum.py` uses IDs to check dependencies, integration references, and dependency cycles.

## Evaluation Metadata

The generated examples keep human-judgement fields such as `primary_family_clarity` and `level_containment`. These are evaluation metadata, not proposed child-facing curriculum fields.

## Complexity Assessment

The amendments add facilitator guidance but do not damage the original purpose. They do not add new card types, new levels, or a second primary family.

The trade-off is that the schema is no longer self-sufficient from three short definitions. Facilitators need a one-page tie-breaker guide to classify edge cases consistently.
