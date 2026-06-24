# Website Review Notes

## Output

Created a single-page static prototype website for The Invention Club:

- `index.html`
- `styles.css`
- `script.js`
- `assets/invention-workshop-hero.png`

Updated `README.md` with local review instructions.

## Communication Priority

The site is written primarily for parents, not curriculum designers. The copy leads with:

- what the club is;
- why it is broader than a coding club;
- what children actually do in sessions;
- how the age pathway changes independence, materials and depth;
- how the curriculum model gives structure without feeling schoolish;
- what safety and support still need confirming before launch.

The curriculum is translated into parent-facing language: children collect practical invention "powers", then use power cards, combination challenges and open invention missions.

## Communication Iteration

After reviewing the rendered page, the site was revised to reduce prose density and make the journey easier to scan:

- The opening explanation was changed into three idea cards plus reassurance callouts.
- The coding comparison now includes a parent-friendly screen-time comparison table.
- Session structure is shown as a five-step strip.
- Age pathways now show age range, group name, independence level and activity style.
- Curriculum depth is handled through expandable sections rather than continuous text.
- Example sessions are presented as project tiles with age suitability and skills developed.
- Parent benefits use short icon-led cards.
- A practical FAQ keeps joining questions out of the main story flow.

## Sources Used

- `docs/website-brief.md` for audience, required sections, age bands, positioning, design direction and required copy themes.
- `docs/schema-under-test.md` for skill families, power cards, integration cards, invention cards and the level ladder.
- `docs/schema-amendments.md` for the "viable with amendments" framing and the need for facilitator guidance.
- `reports/schema-stress-test.md` for the final viability judgement and validation summary.
- `reports/amendment-audit.md` for caution that the final metrics are too clean and that some boundaries remain intent-sensitive.
- `reports/skill-boundary-edge-cases.md` for the human-facing design caveats around comfort, feedback, aesthetics, repairability and planning.
- `curriculum/source/curriculum.v1.json` for Integration/Invention examples and challenge themes, with generated mirrors under `curriculum/generated/`.
- `reports/validation-results.json` for the validated counts, mechanical result, and retained warning state.

## Visual Asset

The hero image was generated with the built-in image generation tool and copied into the workspace as `assets/invention-workshop-hero.png`.

Prompt summary: a warm, credible workshop table scene for a parent-facing children's invention club website, showing hands and materials rather than identifiable faces; motors, wheels, sensors, cardboard, simple electronics, craft materials, compatible building parts and notebook sketches; bright community workshop mood; no readable text, logos, watermarks, brand names, dangerous tools or dark coding-club aesthetic.

## Assumptions

- This is a communication prototype, not a production marketing site.
- The first launch will involve selected age groups, not the full 4-18 pathway at once.
- The register-interest section should show the intended parent questions, but must not submit data in this static version.
- "The Invention Club" has no confirmed contact address, logo, venue, schedule, pricing, safeguarding policy text or booking route yet.
- The generated hero image is acceptable as a placeholder review asset because no real club photography exists yet.

## Human Review Questions

- Is "children learn to invent" the clearest top-line promise?
- Does the page feel exciting without implying unavailable age groups are already running?
- Would parents understand "skill families" after reading the curriculum section?
- Does the site make the club feel structured without making it sound like school?
- Are the younger age pathways believable enough for parents of 4-6 and 6-8 year olds?
- Are the older age pathways ambitious enough for 10.5-18?
- Should the first launch age band be stated more specifically?
- What local details are needed before sharing this with real parents: venue, price, dates, staffing, insurance, safeguarding, consent, contact route?
- Should "coding" be mentioned more gently for parents who are already looking for coding clubs?

## Remaining Production Decisions

- Replace the prototype interest form with the chosen live contact or form process.
- Confirm launch age groups, venue, dates, session length and pricing.
- Add real safety, safeguarding, consent and privacy details before public launch.
- Replace or supplement generated imagery with real workshop photography when available.
- Decide whether holiday workshops should be presented as a launch offer or a future option.
- Test the wording with parents and venue partners, especially the curriculum model section.
