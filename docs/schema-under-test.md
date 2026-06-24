# Invention Club schema under test

A curriculum is a map of skill families.

A skill family is a group of primitive capabilities with the same primary learning problem.

Each family uses the same level ladder:

1. Encounter — recognise/use safely
2. Activate — make the basic thing happen
3. Adjust — change its behaviour
4. Apply — use it in a different context
5. Coordinate — use multiple related elements together
6. Improve — debug, refine, optimise or explain trade-offs

Each global level must define these dimensions:
- adult support
- child independence
- kit state
- coding expectation
- physical build complexity
- debugging/evidence expectation
- integration readiness

Coding boundary:
- Level 1: no code.
- Level 2: no child-authored code; preloaded or plug-and-play code is allowed.
- Level 3: adjust one parameter, setting, threshold, timing value or mode.
- Level 4: guided adaptation of a known code or logic pattern.
- Level 5: coordinate multiple inputs, outputs, states, messages or subsystems.
- Level 6: debug, optimise, compare or justify trade-offs.

A power card teaches one primitive capability from one primary family.

An integration card combines two or more power cards from different families.

An invention card invites children to use any unlocked skills to solve or create something.

Projects are not the curriculum.
Projects are evidence that children can combine skills.

A level may introduce more mastery inside the same family, but should not require a new family as the main learning objective.

Amendment under test: a card may name supporting families when other family knowledge is useful but not the main learning objective. Supporting families do not change the card type. A power card remains inside its primary family when the I can statement, success condition and main debug prompts are about that family's learning problem, even if a dependency or material comes from another family.

For ambiguous cards, include a short classification rationale explaining why the primary family was chosen.

Tie-breaker for cross-cutting skills:
- Debugging/Testing is primary when the diagnostic method is what the child is learning.
- Power is primary when the child is learning energy suitability, voltage, current, duration or electrical safety.
- Design/Iteration is primary when the child is learning to use needs, criteria, constraints, evidence or trade-offs to choose a direction.
- Otherwise, cross-cutting concerns should usually be supporting families on the domain card, not new primary families.

Tie-breaker for Improve level:
- Improve inside a family means debug, refine, optimise or explain trade-offs in that family's own object of study.
- Do not move every level-6 repair or refinement card into Debugging/Testing.
- Use Debugging/Testing as the primary family only when the transferable testing method is the main learning objective across possible domains.

Tie-breaker for mechanisms and interaction:
- Passive joints, mounts and load-bearing parts are Structures when the main problem is support, alignment, range or strength.
- Actuated or controlled travel is Movement when the main problem is making motion happen predictably.
- Human-facing controls are Control/Input when the main problem is how a person provides a command or value, even if layout and labelling draw on Design/Iteration.
- Message sending, addressing and command meaning are Communication when the main problem is getting the right information from sender to receiver.

Tie-breaker for integration versus invention:
- Fixed challenge plus named required power cards is Integration.
- Open-ended theme with multiple acceptable solution paths is Invention.
- If the same topic can be either, classify the curriculum card by how much choice the child has, not by the finished object.

Every card should be classifiable as one of:
- Power card
- Integration card
- Invention card

Every power card should have:
- id
- title
- I can statement
- primary family
- level
- dependencies
- materials
- success condition
- debug prompts
- stretch challenge
- possible integrations

Every integration card should have:
- id
- title
- families combined
- required power cards
- challenge
- success condition
- choice points
- make-it-yours prompts

Every invention card should have:
- id
- theme
- open-ended challenge
- possible skill families
- constraints
- reflection prompts

Known concern:
Overlap may emerge. For example:
- “I can start and stop a motor with a button” might look like Movement or Control.

The proposed resolution is:
- “make a motor move” is Movement
- “read a button” is Control/Input
- “button-controlled motor” is Integration, not a level inside either family
