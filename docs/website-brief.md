# The Invention Club website brief

## Purpose

Create a static prototype website for "The Invention Club".

The site is primarily for parents who may pay for their child to attend local sessions.

The site should also help the founder review and communicate the idea clearly.

This is not a full booking platform. It is a polished communication prototype.

## Core positioning

The Invention Club is a hands-on creative engineering club for children.

It is not a normal coding club.

Children learn practical invention skills — movement, sensing, control, structures, power, communication, debugging and design — then combine those skills into their own creations.

Code, micro:bits, motors, sensors, cardboard, LEGO-compatible parts, craft materials and electronics are all treated as invention materials.

Core message:

Children do not just learn to code. They learn to invent.

## Audience

Primary audience:
- Parents and carers

Secondary audience:
- Schools
- Community venues
- Holiday workshop partners

The copy should answer parent questions:
- What is this?
- Will my child enjoy it?
- Is it safe?
- Is it structured?
- Is it creative?
- What age is it for?
- What will my child actually do?
- How do I register interest?

## Delivery model

Initial model:
- Local in-person weekly club
- Ad-hoc special project holiday workshops

Do not build booking, payments, authentication, admin dashboards or CMS.

CTA:
- Register interest

## Age ranges

Use age ranges inspired by UK Scout section ages:

- Mini Inventors: 4–6
- Junior Inventors: 6–8
- Inventors: 8–10½
- Advanced Inventors: 10½–14
- Studio Inventors: 14–18

Important message:
The skill-family schema is shared across age ranges, but the activities, materials, independence, safety boundaries and depth change by age.

Younger children should be described as exploring playful making, cause-and-effect, big parts, stories and adult-supported builds.

Older children should be described as taking on more electronics, robotics, debugging, design choices, trade-offs, open-ended invention challenges and mentoring.

Do not imply every age band is already available. Say that initial sessions will launch for selected age groups and the wider pathway is being developed.

## Curriculum model

Explain the curriculum in parent-friendly language.

Use the idea of children collecting practical invention "powers".

Required concepts:
- Skill families
- Power cards
- Integration cards
- Invention challenges
- Age-appropriate pathways

Explain:

A skill family is a type of invention power, such as making things move or making things notice the world.

A power card teaches one practical capability.

An integration card combines two or more skills into a fixed challenge.

An invention challenge gives children a more open-ended mission where they choose how to solve it.

Do not overuse academic language.

## Skill families to show

Use these 10 families:

1. Movement
2. Control/Input
3. Sensing
4. Structures
5. Power
6. Materials/Fabrication
7. Logic/Sequencing
8. Communication
9. Debugging/Testing
10. Design/Iteration

Give each a child-friendly phrase:

- Movement: Make it move
- Control/Input: Make it obey
- Sensing: Make it notice
- Structures: Make it strong
- Power: Make it run safely
- Materials/Fabrication: Make it real
- Logic/Sequencing: Make it decide
- Communication: Make it signal
- Debugging/Testing: Make it work again
- Design/Iteration: Make it better

## Level ladder

Show the shared ladder:

1. Encounter — recognise it and use it safely
2. Activate — make the basic thing happen
3. Adjust — change how it behaves
4. Apply — use it in a new context
5. Coordinate — make several related things work together
6. Improve — test, debug, refine or explain trade-offs

Make clear that younger children may use simpler versions of the ladder.

## Example combinations

Include examples such as:

- Movement + Control/Input = button-controlled motor
- Movement + Communication + Control/Input = remote-controlled vehicle
- Sensing + Communication + Logic = alarm system
- Structures + Movement + Materials = hinged bridge
- Debugging + Design + Movement = improve a weak robot
- Power + Sensing + Movement = solar-powered fan

## Example sessions

Include these example sessions:

1. Make it move
   Children explore wheels, motors, spinners, flaps and moving creatures.

2. Make it obey
   Children use buttons, switches, remotes or simple controls.

3. Make it notice
   Children use sensors to detect light, distance, tilt, sound or touch.

4. Build it strong
   Children make towers, bridges, frames, hinges and chassis stronger.

5. Inventor challenge day
   Children combine skills to make something useful, funny, helpful, surprising or weird.

## Parent benefits

Emphasise:
- creativity
- confidence
- practical problem-solving
- resilience
- teamwork
- curiosity
- engineering thinking
- debugging without fear
- making ideas real

Avoid overclaiming academic outcomes.

## Safety and safeguarding copy

Include a reassuring section covering:
- age-appropriate materials
- supervised tools
- safe batteries and electronics
- structured sessions
- risk-aware making
- suitable adult support

Do not invent specific policies, insurance details or registration claims.

Use wording like:
"Full safety, safeguarding and consent arrangements will be confirmed before launch."

## Human review section

Include a small section called something like:

"Curriculum under review"

Explain:
The curriculum model has been stress-tested using generated examples and edge cases. The current conclusion is that the model is viable with amendments, especially around how human-facing design skills such as comfort, usability, feedback and aesthetics are handled.

Ask reviewers:
- Are the age bands clear?
- Would parents understand "skill families"?
- Does the curriculum sound structured without sounding schoolish?
- Are the examples exciting enough?
- Are the younger age pathways believable?
- Are the older age pathways ambitious enough?
- Is the distinction between skill, integration and invention clear?
- What would make you trust this as a parent?

## Required website sections

Build a single-page static website with these sections:

1. Hero
2. What is The Invention Club?
3. Why not just coding?
4. How a session works
5. Age pathways
6. Curriculum model
7. Skill families
8. Example combinations
9. Example sessions
10. For parents
11. Holiday workshops
12. Safety and support
13. Curriculum under review
14. Register interest

## Design direction

Visual style:
- playful but credible
- bright but not babyish
- maker/workshop feel
- tactile
- parent-friendly
- not corporate SaaS
- not hacker/dark-mode coding club

Use:
- cards
- badges
- simple icons or emoji-like visual motifs if appropriate
- skill-map feel
- notebook/workshop language

Avoid:
- stock-photo-heavy corporate style
- pretending to be a school
- overwhelming parents with curriculum jargon

## Technical requirements

Use static HTML, CSS and JavaScript only.

No backend.
No booking system.
No payments.
No auth.
No CMS.
No external paid dependencies.

The site must:
- run locally by opening index.html or with a simple static server
- be responsive
- have accessible HTML structure
- include clear CTA buttons
- include a register-interest form mockup or CTA area
- have documented run/review instructions

Create or update:
- index.html
- styles.css
- script.js if useful
- README.md with local review instructions
- reports/website-review-notes.md

## Source material

Use these existing files where helpful:
- curriculum/source/curriculum.v1.json as the canonical curriculum source
- curriculum/schema/curriculum.schema.json for the source contract
- curriculum/generated/* only as generated rebuild output, not hand-authored source
- reports/validation-results.json
- reports/schema-stress-test.md
- reports/skill-boundary-edge-cases.md, if present
- docs/schema-under-test.md
- docs/schema-amendments.md, if present

Do not dump raw YAML or raw report text onto the page.
Summarise it into clear parent-facing content.

## Definition of done

Done when:
- The static site runs locally.
- The required sections exist.
- Parents can understand the idea within one minute.
- The curriculum model is explained clearly.
- Age pathways are included.
- The site says the curriculum is under review, not final/proven.
- The CTA is "Register interest".
- No backend or booking system has been added.
- reports/website-review-notes.md explains what was built, assumptions made, and what needs human review.
