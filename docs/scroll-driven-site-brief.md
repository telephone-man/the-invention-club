# Scroll-Driven Site Brief Process

This document outlines a creative process for briefing a scroll-driven version of The Invention Club website.

The aim is not to add animation for spectacle. A good scroll-driven site should start with the story, not the motion. The brief should decide what a parent should understand, feel and remember at each scroll beat.

## 1. Define The Job

Clarify what the page needs to do before deciding how it should move.

Useful questions:

- Is the page explaining an idea?
- Is it selling a club to parents?
- Is it making a curriculum feel exciting?
- Is it helping the founder test positioning?
- Is it getting people to register interest?

For The Invention Club, the likely job is:

> Help parents quickly understand that The Invention Club is broader than coding, structured enough to trust, and exciting enough to imagine their child joining.

This job should guide every animation decision. If a motion effect does not help with understanding, trust, excitement or action, it should probably be removed.

## 2. Map The Parent Journey

Turn the page into a sequence of emotional and informational beats.

Example journey:

| Beat | Parent thought | Page job |
| --- | --- | --- |
| Curiosity | What is this? | Explain the proposition immediately. |
| Recognition | My child would enjoy this. | Show making, play, creativity and confidence. |
| Differentiation | It is not just another coding club. | Contrast coding with broader invention skills. |
| Trust | There is real structure behind it. | Show sessions, age pathways and curriculum logic. |
| Imagination | I can picture what my child will make. | Use project tiles and concrete examples. |
| Reassurance | It is age-appropriate and safe. | Surface support, safety and no-experience-needed messages. |
| Action | I want to register interest. | Make the CTA easy to find and low-friction. |

Each scroll section should have one job. If one section is trying to create curiosity, explain curriculum depth and answer safety questions at once, split it.

## 3. Choose A Scroll Metaphor

Pick the creative device that holds the page together.

Possible metaphors for The Invention Club:

- A child's invention notebook unfolding as you scroll.
- A workshop table where parts assemble into ideas.
- Skill cards being collected and combined.
- A machine gradually coming to life.
- A roadmap from Explore to Invent.
- A wall of project tiles that unlocks as skills are learned.

This choice matters because it shapes layout, motion, imagery and copy.

Recommended direction for the current prototype:

> A workshop table of parts gradually becomes a structured invention pathway.

This fits the existing hero image, the skill-card model and the parent-facing message that the club is both creative and structured.

## 4. Define The Scenes

Break the page into animated scenes, not just sections.

For each scene, define:

- Main message
- Visual treatment
- What changes while scrolling
- What must stay readable
- What action or feeling the user should leave with

Example scene map:

| Scene | Message | Visual treatment | Motion idea | Leave the parent feeling |
| --- | --- | --- | --- | --- |
| Hero | Children learn to invent. | Workshop table, short headline, CTA. | Table fades in; small parts subtly settle into place. | I understand the idea quickly. |
| What children make | This is real, hands-on making. | Three tactile idea cards. | Cards rise in sequence like parts being placed on the table. | My child would enjoy this. |
| Not just coding | Invention is broader than screens. | Comparison cards and screen-time table. | A code-like block visually opens into motor, sensor and structure cards. | This is different from a normal coding club. |
| Session journey | Sessions have a safe structure. | Five-step timeline. | Steps light up as the user scrolls. | I can picture the session rhythm. |
| Age pathways | Same model, different depth. | Age cards along a pathway. | Cards slide or pin along a route from supported play to independent invention. | There is a place for my child's age. |
| Curriculum | Skills combine into inventions. | Skill cards, accordion depth, roadmap. | Skill families connect into project tiles with simple animated lines. | The club has real educational structure. |
| Project examples | Children make concrete things. | Project tiles. | Tiles unlock or flip in small groups. | I can imagine the outcomes. |
| Safety and support | Making is risk-aware and age-appropriate. | Reassurance callouts and FAQ. | Motion slows down; content is steady and easy to read. | I trust the approach. |
| Register | Join the first wave. | Static interest form. | Form settles into view like the final card in the journey. | I know what to do next. |

## 5. Decide What Must Stay Static

Scroll animation can damage clarity if the brief does not protect the essentials.

Fixed anchors:

- Navigation remains simple.
- Main headings stay readable.
- The primary CTA appears early and late.
- Parent reassurance is never hidden behind animation.
- Age suitability is easy to scan.
- Safety information is not buried inside motion.
- Mobile may use simpler reveals.
- Reduced-motion users get a non-animated experience.

The page should never rely on animation as the only way to understand the content.

## 6. Specify Motion Personality

Describe how the movement should feel.

For The Invention Club, the motion should feel:

- Tactile
- Playful
- Workshop-like
- Curious
- Smooth but not flashy
- More like parts clicking into place than a tech startup spectacle

Avoid:

- Heavy parallax for its own sake
- Dark hacker visuals
- Overly childish bouncing
- Scrolljacking that fights normal scrolling
- Animations that delay reading
- Effects that make parents work to understand the offer

## 7. Identify Assets Needed

Before implementation, decide what the scroll experience needs.

Possible assets:

- Hero image
- Workshop table image
- Simple icons
- Skill cards
- Project tiles
- Notebook textures
- Animated lines or connectors
- Small component illustrations
- No extra assets, using only HTML, CSS and light JavaScript

Recommended asset approach for this prototype:

- Keep the existing hero image.
- Use the existing card system as the main visual language.
- Add motion through CSS classes and small vanilla JavaScript observers.
- Use simple graphic shapes, lines and icons rather than asset-heavy illustration.
- Avoid adding a framework or animation library unless a later production brief explicitly allows it.

## 8. Write Acceptance Criteria

The brief should end with concrete checks.

A scroll-driven version should pass these checks:

- A parent can understand the club within the first screen.
- Scrolling feels like a guided journey, not decoration.
- Every animation supports a message.
- The page remains readable with animations disabled.
- Reduced-motion preferences are respected.
- Mobile experience is simpler but complete.
- Register interest remains easy to find.
- Age pathways remain instantly scannable.
- Safety and support information remains steady and readable.
- No backend, frontend framework, booking system, payment flow, authentication or CMS is added.

## Core Creative Question

The key creative question is:

> What should the page reveal as the parent scrolls?

For The Invention Club, the strongest answer is probably:

> It starts as a table of parts, then gradually reveals a structured pathway from playful making to confident invention.

That gives the animation a reason to exist. The scroll is not just movement; it is the parent discovering that the club has both creative energy and a real learning structure.

