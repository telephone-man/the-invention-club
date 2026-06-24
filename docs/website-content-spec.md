# Website Content Spec

This is the source of truth for parent-facing website changes to The Invention Club prototype.

The site is a static communication prototype. It should help parents understand the idea, not act like a finished booking system.

## Mission Statement

The Invention Club is a hands-on creative engineering club where children learn to invent, not just code.

## Parent Promise

Children learn to make ideas real.

They do this by making, testing, changing and explaining practical prototypes with motors, sensors, switches, wheels, cardboard, electronics, craft materials and design choices.

## Primary Audience

The primary audience is parents and carers who may want their child to attend local sessions.

The secondary audience is schools, venues, holiday workshop partners and reviewers helping the founder shape the offer.

## Page Purposes

`index.html` is the parent-facing landing page. It should answer:

- What is this?
- Will my child enjoy it?
- Is it broader than coding?
- What ages is it for?
- Is it structured and safe?
- How do I register interest?

`curriculum.html` is the "How sessions work" page. It should make the club feel concrete, safe and imaginable by explaining the card system without sounding academic: children choose a broad Skill Card on the page, choose a level, work through generated Power Cards mapped to that skill family, test what happened, improve one thing, then choose whether to repeat, stretch, switch skills, combine powers or take on an open invention.

## CTA Hierarchy

Primary CTA:

- Register interest

Secondary CTA:

- See how sessions work

Use "How sessions work" for links to the card-system explanation page. Keep the public nav label consistent.

## Voice

Use language that is:

- clear;
- warm;
- practical;
- parent-friendly;
- honest about prototype status.

Prefer:

- Children learn to invent.
- Make it move.
- Make it notice.
- Make it stronger.
- Try it, test it, change it.
- Register interest.

Avoid:

- academic curriculum jargon as the lead message;
- startup language;
- school-prospectus language;
- exaggerated future outcomes;
- claims that booking, payment, dates, pricing, policies or safeguarding arrangements are confirmed before they are.

## Brand Constraints

The site should feel:

- playful but credible;
- tactile and workshop-like;
- bright but not babyish;
- structured without feeling schoolish;
- broader than a coding club.

Use the existing warm paper, teal, coral and gold visual system unless there is a clear reason to revise it.

The homepage should prioritise communication over curriculum completeness. Deeper curriculum explanation belongs on `curriculum.html`.

## Production Visual Language

The selected production visual direction is **Workbench**.

Future website changes should preserve a tactile maker feel: chunky dark outlines, warm bench and paper surfaces, maker labels, rails, trays, labelled bins and practical workshop groupings.

Avoid drifting back toward generic landing-page patterns such as repeated white cards with soft shadows, stock SaaS section layouts, decorative card grids that do not explain the offer, or overly polished corporate styling.

Use visual structure to help parents understand the idea:

- homepage: parent clarity and action;
- how sessions work page: guided learning loop using Skill Cards, levelled Power Cards, testing, improvement, requirement chips and practical challenge cards.

## Skill Icon Guidelines

Skill icons should make the card system feel specific to invention, not like generic suits from a template.

The governing rule is `docs/playing-card-icon-design-brief.md`. Treat the icons as playing-card symbols first and decorative artwork second.

Use:

- one clear object or action per skill;
- instantly recognisable subjects: wheels, buttons, sensors, trusses, batteries, tools, message signals, repair marks and iteration arrows;
- bold silhouettes, thick shapes, strong contrast and enough padding to read at small card size;
- a consistent generated/rendered image style for the Skill Card deck: warm paper background, tactile maker materials, clear icon-like subject, and no text inside the image;
- optimised project-local image assets under `assets/skill-icons/` when using rendered Skill Card artwork;
- the current approved Skill Card image for each skill stored directly in `assets/skill-icons/`, without versioned subdirectories;
- decorative images marked with empty `alt` text when the surrounding card text already names the skill.

Avoid:

- emoji as the main icon artwork;
- generic abstract shapes as the only distinction between skills;
- stock icon sets that make the site feel like a SaaS template;
- detailed miniature scenes that become hard to read at card size;
- one-off generated images with inconsistent lighting, angle or material style;
- readable text, labels, logos or brand marks inside the icon artwork.

### Skill Card Image Briefs

All ten Skill Card images should share the same visual system: square rendered image, centred object, warm off-white paper background, tactile cardboard/workbench materials, soft natural light, no hands, no children, no faces, no readable text, no logos and no brand marks.

Individual images should emphasise:

- `Make it move`: a small wheel, axle and motor module; the object should clearly suggest physical motion and mechanism.
- `Make it obey`: a sturdy push button, switch or control panel; the object should clearly suggest a child can command an action.
- `Make it notice`: a sensor module or sensing object; the object should clearly suggest detecting distance, light, tilt or touch.
- `Make it strong`: a triangular truss, braced frame or load-bearing craft structure; the object should clearly suggest stability.
- `Make it run safely`: a battery pack with polarity and simple safety treatment; the object should clearly suggest safe power choice, not danger.
- `Make it real`: cardboard, ruler, safe cutter, folded material or joined parts; the object should clearly suggest fabrication.
- `Make it decide`: branching blocks, simple decision path, rule cards or flow pieces; the object should clearly suggest logic and sequencing without code-screen imagery.
- `Make it signal`: radio module, antenna, message tile or signal waves; the object should clearly suggest sending or receiving information.
- `Make it work again`: magnifier, test lead, repair tool or fault-finding setup; the object should clearly suggest testing and repair.
- `Make it better`: a prototype before/after cue, circular improvement arrow or upgraded part; the object should clearly suggest iteration and refinement.

## Card-System Page Rule

The learning detail should read like a practical card system, not an academic report.

The main message is not simply "choose what to try next". The cards help children navigate a guided learning loop: choose, try, test, improve, then decide the next useful move. This structure builds enough powers across enough levels for children to tackle Integration Cards and Invention Cards with more confidence. Guided practice comes first; more open creativity appears through later combination and invention challenges.

Use this hierarchy:

- Skill Cards;
- Power Cards;
- Integration Cards;
- Invention Cards;
- levels from 1 to 6;
- practical challenges;
- child choice.

Do not present Skill Cards, Power Cards, Integration Cards and Invention Cards as four equal options at the top of the page. The normal day-to-day flow is Skill Card -> level -> generated Power Card -> test -> improve -> repeat/stretch/switch/combine. Integration Cards and Invention Cards are separate challenge modes that open up once enough powers have been built.

The generated schema term for the small day-to-day card is `power_card`. The page may still use "Skill Card" as a parent-friendly label for the broad skill choice, but the displayed card results should come from generated Power Card data.

Do not expose schema stress-test conclusions, audit language or reviewer questions on the public card-system page.

## Prototype Boundaries

Do not add:

- backend submission;
- booking;
- payment;
- authentication;
- admin dashboards;
- CMS behaviour;
- confirmed claims about launch dates, pricing, safeguarding, insurance or availability.

The site may show a prototype interest form, but it must clearly state that the static page does not send details yet.
