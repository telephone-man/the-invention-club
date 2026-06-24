# Amendment Audit: Genuine Improvement vs Metric-Gaming

## Scope

This audit compares the pre-amendment evidence recorded in `reports/iteration-log.md` and `reports/schema-stress-test.md` with the current amended schema, generated metadata, and `reports/validation-results.json`.

No curriculum files or validation metrics were edited during this audit. The only output produced by the audit is this file.

## Overall Finding

The latest improvement is **mostly genuine, but the final metrics overstate the certainty**.

The amendments do add reusable schema rules that resolve real ambiguity. The strongest improvements are:

- primary versus supporting families;
- Improve-level ownership;
- passive Structures versus active Movement;
- fixed Integration versus open Invention.

However, the perfect final metric of `80/80` clear power cards and `0/14` arbitrary red-team cases should not be treated as proof that all ambiguity disappeared. It is partly a result of generated evaluation metadata (`primary_family_clarity`, `level_containment`, and `principled_or_arbitrary`) being updated by the same process that amended the schema. A stricter real-world audit would keep several cards as "clear with caveat" rather than simply "clear".

Conservative audit result:

- Genuine schema improvement: 14 items
- Genuine but still intent-sensitive: 5 items
- Weak / close to relabelling: 1 item

So the schema is materially stronger, but the final validation metrics are too clean.

## Rules Used In This Audit

- **R1: Supporting families.** A skill remains in its primary family when the I can statement, success condition, and main debug prompts are about that family, even if dependencies or materials come from another family.
- **R2: Cross-cutting primary family.** Debugging/Testing is primary when the diagnostic method is the learning objective; Power is primary for energy suitability, voltage, current, duration, or electrical safety; Design/Iteration is primary for needs, criteria, constraints, evidence, or trade-offs.
- **R3: Improve ownership.** Improve stays inside the family whose object of study is being improved. Do not move every repair/refinement card into Debugging/Testing.
- **R4: Mechanism and interaction tie-breakers.** Passive joints, mounts, and load-bearing parts are Structures; actuated or controlled travel is Movement; human-facing controls are Control/Input; message sending, addressing, and command meaning are Communication.
- **R5: Openness rule.** Fixed challenge plus named required power cards is Integration. Open-ended theme with multiple acceptable solution paths is Invention.

## Skill Card Transitions

### `r_dbg_04` - Test a broken circuit

- Pre to current: `clear/leaky` to `clear/inside`.
- Resolving rule: R1 and R2. The diagnostic method is primary; circuit and power knowledge are supporting context.
- Facilitator understandability: Mostly understandable. A facilitator can ask, "Am I teaching a testing method or teaching circuit theory?"
- Subjective intent dependence: Medium. If the session teaches voltage concepts more than test method, this could be Power.
- Three unseen examples: "test a faulty motor driver" => Debugging/Testing if method is primary; "use a checklist to find a bad sensor reading" => Debugging/Testing; "trace why a traffic light sequence fails" => Debugging/Testing if the transfer method is the focus.
- Audit verdict: Genuine improvement with caveat. It is not mere relabelling, but it still depends on stating the learning objective.

### `r_des_06` - Iterate after a test

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R1 and R2. Design/Iteration is primary when evidence is used to choose a direction; Debugging/Testing supplies evidence.
- Facilitator understandability: Mostly understandable if the card includes criteria or user goals.
- Subjective intent dependence: Medium. If the point is how to run the test, Debugging/Testing would be primary.
- Three unseen examples: "redesign a bridge after a load test" => Design/Iteration if criteria drive the change; "revise a controller after a user test" => Design/Iteration; "choose a material after comparing test results" => Design/Iteration if the decision process is primary.
- Audit verdict: Genuine but intent-sensitive.

### `r_pow_04` - Choose a safe battery

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R2. Power is primary for energy suitability, current, voltage, duration, and electrical safety.
- Facilitator understandability: High. This is a natural Power card.
- Subjective intent dependence: Low. Design trade-offs support the choice, but the main object is the battery/power source.
- Three unseen examples: "choose a battery for two servos" => Power; "reject a coin cell for a motor" => Power; "select a pack for an LED sign runtime" => Power.
- Audit verdict: Genuine schema improvement.

### `r_pow_08` - Explain battery safety trade-offs

- Pre to current: `clear/leaky` to `clear/inside`.
- Resolving rule: R2. Battery capability and safety trade-offs remain Power, with Design/Iteration as supporting context.
- Facilitator understandability: High.
- Subjective intent dependence: Low to medium. It becomes Design/Iteration only if the broader design decision is primary rather than the power trade-off.
- Three unseen examples: "explain why a large pack is unsafe for a wearable" => Power; "compare duration versus current draw" => Power; "write a battery safety note for another team" => Power.
- Audit verdict: Genuine improvement.

### `r_mov_07` - Improve unreliable motion

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R3. The object being improved is the mechanism's motion.
- Facilitator understandability: High. "What are we improving?" is a usable facilitator test.
- Subjective intent dependence: Medium. If the lesson is a general troubleshooting strategy, Debugging/Testing could be primary.
- Three unseen examples: "reduce gear slipping" => Movement; "make a servo gate stop overshooting" => Movement; "smooth a linkage that jams" => Movement.
- Audit verdict: Genuine improvement.

### `r_ctl_08` - Improve input reliability

- Pre to current: `clear/leaky` to `clear/inside`.
- Resolving rule: R3 and R4. The object being improved is how the input is pressed, read, or understood.
- Facilitator understandability: Mostly understandable, but less crisp than the motor or battery examples because it mixes physical, electrical, and usability failures.
- Subjective intent dependence: Medium to high. It could become Debugging/Testing or Design/Iteration depending on what the facilitator emphasizes.
- Three unseen examples: "make a button easier to press" => Control/Input; "reduce joystick dead-zone confusion" => Control/Input; "make a safety hold switch harder to trigger accidentally" => Control/Input.
- Audit verdict: Genuine but still intent-sensitive. The metric improvement is defensible, but not as strong as the final `clear` label implies.

### `r_sen_08` - Improve a noisy sensor setup

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R3. The object being improved is the sensor reading.
- Facilitator understandability: High.
- Subjective intent dependence: Medium. If the activity teaches a general debugging routine, Debugging/Testing could be primary.
- Three unseen examples: "shield a light sensor from room glare" => Sensing; "calibrate a distance sensor for dark material" => Sensing; "smooth a jumpy tilt sensor reading" => Sensing.
- Audit verdict: Genuine improvement.

### `r_str_07` - Improve a weak chassis

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R3. Chassis strength is a Structures object of study; testing and iteration are supporting.
- Facilitator understandability: High.
- Subjective intent dependence: Medium. It becomes Design/Iteration if the lesson is comparing redesign options rather than strengthening a chassis.
- Three unseen examples: "brace a rover frame after a load test" => Structures; "reduce chassis twist" => Structures; "strengthen a bridge deck joint" => Structures.
- Audit verdict: Genuine improvement.

### `r_pow_07` - Diagnose power drop

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R2 and R3. Power is primary when the failure is understood through voltage/current behavior in the power path.
- Facilitator understandability: Mostly understandable for technical facilitators; less obvious for novice facilitators because the title says "diagnose".
- Subjective intent dependence: Medium to high. If the transfer skill is fault isolation, Debugging/Testing is a plausible primary family.
- Three unseen examples: "find why a motor browns out the board" => Power; "measure voltage sag under load" => Power; "choose a thicker wire after voltage drop" => Power.
- Audit verdict: Genuine but intent-sensitive. Not metric-gaming, but the card needs its rationale.

### `r_log_07` - Debug wrong order

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R3. The object being improved is sequence logic, not generic debugging.
- Facilitator understandability: Mostly understandable.
- Subjective intent dependence: Medium. The word "debug" can pull this into Debugging/Testing unless the success condition is clearly about sequence order.
- Three unseen examples: "fix a traffic-light state order" => Logic/Sequencing; "repair a countdown that skips a step" => Logic/Sequencing; "correct a game rule that fires too early" => Logic/Sequencing.
- Audit verdict: Genuine improvement with caveat.

### `r_ctl_04` - Debounce a button

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R4. Human-facing controls are Control/Input when the main problem is converting a human action into one command or value.
- Facilitator understandability: High enough if "one press counts once" is kept as the success condition.
- Subjective intent dependence: Medium. It could become Logic/Sequencing if timing rules are the main lesson, or Debugging/Testing if fault isolation is the main lesson.
- Three unseen examples: "make one switch toggle once per press" => Control/Input; "ignore joystick centre jitter" => Control/Input; "turn a knob range into stable zones" => Control/Input.
- Audit verdict: Genuine improvement.

### `r_ctl_07` - Arrange a control panel

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R4. Human-facing controls are Control/Input when the main problem is how a person provides commands.
- Facilitator understandability: Medium. A facilitator could understand it, but may reasonably see it as Design/Iteration or Materials/Fabrication.
- Subjective intent dependence: High. Layout, labels, and user testing are design-heavy.
- Three unseen examples: "place emergency stop where it is easy to reach" => Control/Input if command access is primary; "group joystick and fire button for a game controller" => Control/Input; "label a control box so another child can operate it" => Control/Input if operation is primary.
- Audit verdict: Genuine but weak. It is not pure relabelling, but it should remain "clear with caveat" rather than unqualified clear.

### `r_str_04` - Build a hinge joint

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R4. Passive joints, mounts, and load-bearing parts are Structures when support, alignment, range, or strength is primary.
- Facilitator understandability: High. Passive versus actuated is a practical distinction.
- Subjective intent dependence: Low to medium. It becomes Movement if the lesson is controlled actuation.
- Three unseen examples: "make a cardboard flap hinge that does not tear" => Structures; "align a drawbridge pivot" => Structures if passive support is primary; "build a folding stand that holds weight" => Structures.
- Audit verdict: Genuine improvement.

### `r_com_05` - Apply remote commands

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R4. Message meaning, addressing, and sender/receiver interpretation are Communication.
- Facilitator understandability: Mostly understandable, but only if the card is about messages rather than the remote-controlled build.
- Subjective intent dependence: Medium to high. A remote vehicle lesson could easily be Integration, Control/Input, or Movement.
- Three unseen examples: "map radio code 3 to stop" => Communication; "make a receiver ignore unknown commands" => Communication; "name commands from the receiver point of view" => Communication.
- Audit verdict: Genuine but intent-sensitive.

### `r_dbg_06` - Coordinate subsystem tests

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R2. Debugging/Testing is primary when the transferable test method is the learning objective across domains.
- Facilitator understandability: High for facilitators comfortable with subsystem testing; moderate for novice facilitators.
- Subjective intent dependence: Medium. If the task fixes one specific subsystem, that subsystem's family may be primary.
- Three unseen examples: "test power, code, and motor separately before changing a rover" => Debugging/Testing; "order checks for a robot that resets" => Debugging/Testing; "compare sensor, logic, and output tests before repair" => Debugging/Testing.
- Audit verdict: Genuine improvement.

### `r_des_08` - Scope an invention challenge

- Pre to current: `borderline/leaky` to `clear/inside`.
- Resolving rule: R2 and R5. Design/Iteration is primary when children use constraints and criteria to turn an open theme into a buildable challenge.
- Facilitator understandability: Medium. It is understandable, but it feels like a planning/meta-design card rather than a primitive invention-club capability.
- Subjective intent dependence: High. It could be a facilitation move, an invention card, or a design skill depending on how it is used.
- Three unseen examples: "turn 'help pets' into a buildable feeder challenge" => Design/Iteration if scoping is taught; "turn 'secret signals' into success criteria" => Design/Iteration; "choose constraints for a classroom helper invention" => Design/Iteration.
- Audit verdict: Weak / close to relabelling. The rule can classify it, but this item is not strong evidence that the schema improved. It should not carry much weight in the final metric.

## Red-Team Transition Audit

### `robotic arm`

- Pre to current: `arbitrary` to `principled`.
- Resolving rule: R5, with R4 support. A fixed challenge with named Movement, Structures, and Control/Input prerequisites is Integration; open-ended arm design is Invention.
- Facilitator understandability: High if the card states fixed required powers.
- Subjective intent dependence: Medium. The same object can appear in different card types, but the rule classifies the curriculum prompt rather than the object.
- Three unseen examples: "fixed two-servo grabber with required servo and frame cards" => Integration; "invent a helper arm for a chosen user" => Invention; "set a single servo angle" => Movement skill.
- Audit verdict: Genuine improvement. This is a strong amendment because it classifies by prompt structure, not by object name.

### `structure with moving hinge`

- Pre to current: `arbitrary` to `principled`.
- Resolving rule: R4. Passive load-bearing hinge is Structures; actuated controlled travel is Movement; combined hinge-plus-actuator challenge is Integration.
- Facilitator understandability: High.
- Subjective intent dependence: Low to medium.
- Three unseen examples: "passive folding bridge hinge" => Structures; "servo opens a flap to a set angle" => Movement; "sensor opens hinged door" => Integration.
- Audit verdict: Genuine improvement.

### `debugging a broken circuit`

- Pre to current: `arbitrary` to `principled`.
- Resolving rule: R1 and R2. Diagnostic method primary; circuit/power knowledge supports the context.
- Facilitator understandability: Mostly understandable.
- Subjective intent dependence: Medium. If the point is voltage or current behavior, Power is primary.
- Three unseen examples: "use a checklist to find an open LED circuit" => Debugging/Testing; "measure where voltage disappears in a motor circuit" => Debugging/Testing if method is primary; "compare two possible circuit faults one at a time" => Debugging/Testing.
- Audit verdict: Genuine improvement with caveat.

### `improving a weak chassis`

- Pre to current: `arbitrary` to `principled`.
- Resolving rule: R3. Improve stays in the family whose object is being improved; chassis strength is Structures.
- Facilitator understandability: High.
- Subjective intent dependence: Medium. If children choose among user criteria or repair strategies, Design/Iteration may become primary.
- Three unseen examples: "strengthen a rover base after load testing" => Structures; "reduce wobble in a tower" => Structures; "compare two chassis redesigns against user criteria" => Design/Iteration if criteria are primary.
- Audit verdict: Genuine improvement.

## Audit Conclusion

The amendments are **not merely metric-gaming**. They introduce reusable rules that classify new examples consistently and preserve the original skill/integration/invention model.

But the latest validation result is too optimistic. Several transitions still depend on facilitator intent, especially:

- `r_ctl_08`
- `r_ctl_07`
- `r_com_05`
- `r_pow_07`
- `r_des_08`

The main genuine improvement is not the perfect metric. The genuine improvement is that ambiguous cards now have explicit questions a facilitator can answer:

1. What is the child primarily learning?
2. What object of study is being improved?
3. Are other families primary or merely supporting?
4. Is the card a fixed cross-family challenge or an open-ended invention prompt?

Recommended interpretation: keep the final verdict **Viable with amendments**, but treat the reported `80/80` and `0/14` as a best-case structured classification result, not as proof that ambiguity has disappeared in real facilitation.
