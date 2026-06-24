# Skill Boundary Edge Cases

Scope: report-only boundary test against `docs/schema-under-test.md` and `docs/schema-amendments.md`. The cases below are candidate power cards, not full projects. Each is written to look atomic while still touching two or more families.

Rules referenced:

- Power card rule: a power card teaches one primitive capability from one primary family.
- Supporting-family rule: other families may be listed when useful, but the card stays in the primary family when the I-can statement, success condition, and main debug prompts are about that family's learning problem.
- Cross-cutting primary-family tie-breakers: Debugging/Testing is primary when diagnostic method is the learning target; Power is primary when energy suitability, voltage, current, duration, or electrical safety is the learning target; Design/Iteration is primary when needs, criteria, constraints, evidence, or trade-offs are the learning target.
- Mechanism and interaction tie-breakers: passive joints, mounts, load-bearing parts, support, alignment, and range are Structures; actuated or controlled travel is Movement; human-facing controls are Control/Input; message sending, addressing, and command meaning are Communication.
- Improve tie-breaker: improvement stays inside the family whose object is being improved unless the transferable test method is the main learning target.
- Openness rule: a fixed capability with one primary learning problem remains a skill; a fixed challenge requiring named skills from different families is an integration; an open-ended theme with many solution paths is an invention.

## Summary

| Confidence | Count | Cases |
| --- | ---: | --- |
| clear | 4 | safety judgement, passive mechanical motion, reducing vibration/friction, calibration |
| borderline | 5 | ergonomics/comfort, behaviour change/user feedback, power generation, repairability, teamwork/planning |
| arbitrary | 1 | aesthetics affecting function |

The schema handles most of the cases if the card author writes the I-can statement tightly. The weak spots are not missing curriculum types; they are facilitator-facing judgement rules for ergonomics, behaviour-change feedback, generated power, repairability, and aesthetic choices that affect use.

## 1. Ergonomics / Comfort

Candidate power card: **Adjust a control for comfort**

- I-can statement: I can change the size, spacing, or angle of one control so it is comfortable to use repeatedly.
- Primary family: `design_iteration`
- Supporting families: `control_input`, `materials_fabrication`
- Skill or demote: Keep as a skill if the success condition is about comfort evidence from a user trial. Demote to integration if the learner must also fabricate a mounted panel or wire the control as part of the same card.
- Schema rule used: Cross-cutting Design/Iteration rule: needs, criteria, constraints, evidence, and trade-offs make Design/Iteration primary. Supporting-family rule keeps Control/Input and Materials/Fabrication secondary when the main learning target is comfort evidence rather than reading the input or making the part.
- Confidence: borderline
- Normal facilitator would understand: Probably, if the card says "comfort criterion" and "user trial" explicitly. Without that wording, a facilitator may classify it as Control/Input because the object is a control.
- Supporting evidence: generated `r_ctl_07` already treats operable control layout as Control/Input with Design/Iteration support, while `r_des_06` treats evidence-based improvement as Design/Iteration.
- Weakness: The amended schema has no explicit ergonomics or comfort tie-breaker. This does not require a new family, but it does require a facilitator note that comfort is a design criterion unless input interpretation is the main learning target.

## 2. Behaviour Change / User Feedback

Candidate power card: **Make feedback easy to act on**

- I-can statement: I can choose a feedback signal that helps a user notice what to do next.
- Primary family: `communication`
- Supporting families: `design_iteration`, `logic_sequencing`
- Skill or demote: Keep as a skill if the work is limited to choosing, naming, and testing the meaning of one feedback signal. Demote to integration if the card requires a sensor trigger, timed rule, and output device to be built together.
- Schema rule used: Mechanism and interaction tie-breaker: message meaning is Communication. Supporting-family rule keeps Design/Iteration and Logic/Sequencing secondary when user response and sequencing are context, not the main taught capability.
- Confidence: borderline
- Normal facilitator would understand: Maybe. Many facilitators would see "behaviour change" as design, classroom management, or logic rather than communication unless the card says the signal meaning is the target.
- Supporting evidence: generated `r_com_05` classifies remote command meanings as Communication with Logic/Sequencing and Movement support; generated `r_com_08` treats reliability and simplicity of messages as Communication trade-offs.
- Weakness: Behaviour-change feedback is under-specified. The schema needs an example-level rule: classify feedback by the thing being learned, not by the desired human outcome. Message clarity is Communication; evidence-based user response design is Design/Iteration; trigger rules are Logic/Sequencing.

## 3. Safety Judgement

Candidate power card: **Reject an unsafe power choice**

- I-can statement: I can reject a battery or supply that could overheat, short, or fail for a chosen load.
- Primary family: `power`
- Supporting families: `design_iteration`, `debugging_testing`
- Skill or demote: Keep as a skill. It is an atomic judgement about energy suitability and safety, not a multi-family build.
- Schema rule used: Cross-cutting Power rule: energy suitability, voltage, current, duration, and electrical safety make Power primary. Supporting-family rule keeps design criteria and test evidence secondary.
- Confidence: clear
- Normal facilitator would understand: Yes. This is close to an existing generated skill.
- Supporting evidence: generated `r_pow_04` is "Choose a safe battery" with Design/Iteration support; the red-team case "choosing a safe battery" also classifies this as a skill.
- Weakness: The existing red-team weakness still applies: there is no explicit Safety support tag. The Power tie-breaker is enough for electrical safety, but non-electrical safety would become less clear.

## 4. Passive Mechanical Motion

Candidate power card: **Limit a hinge range**

- I-can statement: I can add a stop so a passive hinge moves through the intended range without tearing or over-travelling.
- Primary family: `structures`
- Supporting families: `movement`, `materials_fabrication`
- Skill or demote: Keep as a skill. Demote to integration only if the hinge is actuated and the learner must also control the moving action.
- Schema rule used: Mechanism and interaction tie-breaker: passive joints, support, alignment, and range are Structures; actuated travel is Movement; combining passive structure with actuation becomes Integration.
- Confidence: clear
- Normal facilitator would understand: Yes, assuming "passive" is stated.
- Supporting evidence: generated `r_str_04` classifies a hinge joint as Structures with Movement and Materials/Fabrication support; red-team "structure with moving hinge" uses the same rule.
- Weakness: No new rule needed.

## 5. Power Generation

Candidate power card: **Measure generated power**

- I-can statement: I can compare how much useful voltage or stored charge a hand crank or small solar cell provides under two conditions.
- Primary family: `power`
- Supporting families: `movement`, `sensing`, `debugging_testing`
- Skill or demote: Keep as a skill if the task is measurement and power suitability. Demote to integration if the learner must design a full generator mechanism, storage circuit, and powered output.
- Schema rule used: Cross-cutting Power rule: energy suitability, voltage, current, and duration make Power primary. Supporting-family rule keeps the hand motion, light condition, and measurement method secondary.
- Confidence: borderline
- Normal facilitator would understand: Probably, but only if "generated voltage or stored charge" is the success condition.
- Supporting evidence: generated `r_pow_03` measures voltage and `r_pow_04` chooses safe power; the family definition for Power is "Provide safe, adequate energy for components."
- Weakness: The Power rule talks mainly about providing and choosing energy, not generating or harvesting it. This probably needs a wording clarification, not a new family.

## 6. Reducing Vibration Or Friction

Candidate power card: **Reduce rubbing in a linkage**

- I-can statement: I can reduce rubbing, vibration, or sticking in one moving mechanism and show that the motion is more reliable.
- Primary family: `movement`
- Supporting families: `materials_fabrication`, `debugging_testing`, `structures`
- Skill or demote: Keep as a skill. It is a refinement of a motion problem, not a whole build.
- Schema rule used: Improve tie-breaker: improvement stays in the family whose object is being improved. Mechanism tie-breaker makes predictable actuated or mechanical motion a Movement problem.
- Confidence: clear
- Normal facilitator would understand: Yes.
- Supporting evidence: generated `r_mov_07` improves unreliable motion with Debugging/Testing support; generated `r_mov_08` explains motion trade-offs.
- Weakness: No new rule needed.

## 7. Calibration

Candidate power card: **Calibrate a threshold**

- I-can statement: I can set a sensor threshold using readings from the actual room or model.
- Primary family: `sensing`
- Supporting families: `logic_sequencing`, `debugging_testing`, `design_iteration`
- Skill or demote: Keep as a skill if the work is choosing and checking the threshold. Demote to integration if the learner must also build the response system that acts on the threshold.
- Schema rule used: Supporting-family rule: the sensor reading and threshold evidence are the main learning target, so Sensing remains primary even when a later logic rule uses the threshold.
- Confidence: clear
- Normal facilitator would understand: Yes.
- Supporting evidence: generated `r_sen_05` is "Calibrate a sensor"; generated `r_sen_03` sets a sensor threshold.
- Weakness: No new rule needed.

## 8. Repairability

Candidate power card: **Make one part replaceable**

- I-can statement: I can add access or a removable fastening so one part can be replaced without damaging the rest of the build.
- Primary family: `structures`
- Supporting families: `materials_fabrication`, `design_iteration`, `debugging_testing`
- Skill or demote: Keep as a skill if the target is access, fastening, and load/support after removal. Demote to integration if the replaceable part must also be electrically tested, rewired, or redesigned as part of the same card.
- Schema rule used: Mechanism and interaction tie-breaker: mounts, access, support, and load paths are Structures. Cross-cutting Design/Iteration rule is supporting because repairability is a criterion, not the primary object being taught.
- Confidence: borderline
- Normal facilitator would understand: Maybe. Some would classify this as Materials/Fabrication because the visible work is a fastening method; others would classify it as Design/Iteration because repairability is a criterion.
- Supporting evidence: generated `r_str_06` includes frame, mounts, and access points as Structures; generated `r_str_08` includes access and repair as structural trade-offs.
- Weakness: Repairability is currently implicit inside Structures and Design/Iteration. If repairable design becomes common, the schema needs a clearer tie-breaker: repair access is Structures when the learning object is mounting/access; Design/Iteration when the learning object is choosing repairability as a criterion.

## 9. Aesthetics Affecting Function

Candidate power card: **Make a signal look usable**

- I-can statement: I can change the colour, contrast, shape, or finish of one visible signal so a user notices its meaning faster.
- Primary family: `communication`
- Supporting families: `materials_fabrication`, `design_iteration`
- Skill or demote: Keep as a skill only if the signal meaning and user recognition test are the whole card. Demote to integration if the card also requires fabricating the display, powering it, or designing a themed object.
- Schema rule used: Mechanism and interaction tie-breaker: command or message meaning is Communication. Supporting-family rule is used to treat material finish and visual design as support.
- Confidence: arbitrary
- Normal facilitator would understand: Not consistently. A normal facilitator could reasonably choose Communication, Materials/Fabrication, or Design/Iteration depending on whether they notice message meaning, visual making, or user criteria first.
- Supporting evidence: generated `r_com_05` uses command meaning as Communication; generated `r_mat_05` treats enclosure choices as Materials/Fabrication; generated `r_des_04` treats criteria-based choice as Design/Iteration.
- Weakness: This is the hardest case in this set. The current schema does not say whether visual form that changes usability is a communication problem, a fabrication problem, or a design problem. This needs a new tie-breaker or at least a worked example.

## 10. Teamwork Or Planning

Candidate power card: **Plan blocked build steps**

- I-can statement: I can order a team's next three build tasks so one person's task does not block another's.
- Primary family: `design_iteration`
- Supporting families: `logic_sequencing`, `materials_fabrication`, `debugging_testing`
- Skill or demote: Keep as a skill if it is a planning capability with a small fixed success condition. Demote to invention if the card becomes an open-ended team challenge, or to integration if success depends on completing several technical build skills together.
- Schema rule used: Cross-cutting Design/Iteration rule: roles, constraints, criteria, and build planning make Design/Iteration primary. Logic/Sequencing is supporting because ordering is used to manage a build, not to teach programmable or behavioural sequence logic.
- Confidence: borderline
- Normal facilitator would understand: Probably, because generated `r_des_05` already covers roles, order, and team build planning. The risk is that a facilitator treats this as classroom process rather than a child-facing skill.
- Supporting evidence: generated `r_des_05` is "Coordinate a build plan"; generated `r_des_08` scopes an invention challenge and shows that planning can sit close to invention work.
- Weakness: The schema can classify this, but the boundary between curriculum skill and facilitator process remains soft. A one-page guide should say when teamwork/planning is a child skill versus session management.

## Findings

The amended schema does not collapse under these ten harder skill-boundary cases, but it relies heavily on precise authoring. Four cases are clear because the amended rules directly cover them. Five are viable but borderline because the same visible activity can be reframed by changing the I-can statement and success condition. One case, aesthetics affecting function, is arbitrary enough that normal facilitators would probably disagree.

The strongest practical rule remains: classify by the taught learning problem, not by the object being touched. The weakest area is human-facing design where comfort, feedback, visual form, and repair access affect whether something works. Those cases do not necessarily require new families, but they do need explicit examples or a new tie-breaker note in facilitator guidance.
