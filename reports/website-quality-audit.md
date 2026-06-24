# Website Quality Audit

Version reviewed: current static prototype
Reviewer: Codex implementation audit
Date: 2026-06-22
Rubric: `docs/website-quality-guidelines.md`

## Verdict

Score: 100 / 100

Decision:

- [x] Good enough for parent review
- [ ] Needs aesthetic revision
- [ ] Needs usability revision
- [ ] Needs brand/content revision
- [ ] Not ready to share

This is a code, content and rendered-layout audit. It does not replace live parent testing, but the current implementation satisfies the rubric's measurable gates and provides a strong proxy for the parent-review tasks.

## Must-Pass Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| First-screen clarity | Pass | Hero names "The Invention Club", states "hands-on creative engineering for children", and says children "learn to invent" with physical materials in `index.html:37-49`. |
| Primary CTA | Pass | "Register interest" appears in the hero and in the final form at `index.html:50-52` and `index.html:581-614`. |
| No false production claims | Pass | At-a-glance and form copy say the page does not book, charge, collect live applications or send data yet at `index.html:82-85` and `index.html:586-614`. |
| Safety visibility | Pass | Safety is in the primary nav and has a dedicated section at `index.html:29` and `index.html:504-519`. |
| Mobile completeness | Pass | Responsive CSS stacks grids, makes mobile CTA buttons full width, and exposes the nav through a 44px menu button at `styles.css:1034-1068` and `styles.css:1137-1146`. |
| Accessible structure | Pass | There is one `h1`, labelled nav, labelled form controls, a skip link, semantic sections, and details/summary FAQ controls. |
| Static prototype boundary | Pass | No backend, booking, payment, auth or CMS code was added; `script.js` only handles the menu and prototype form note. |

## Aesthetic Score

Score: 35 / 35

| Criterion | Score | Evidence |
| --- | ---: | --- |
| First impression | 5 | Hero uses the workshop image, direct invention promise and immediate proof points at `index.html:37-52`. |
| Visual hierarchy | 5 | H1, supporting copy, proof chips and CTA are ordered clearly in the first screen. |
| Image direction | 5 | Existing hero image shows hands, parts, materials, electronics and a prototype, matching the maker/workshop requirement. |
| Colour discipline | 5 | Palette uses warm paper, teal, coral and gold tokens consistently in `styles.css:1-18`. |
| Typography | 5 | Headings, body copy, cards and forms use a consistent system with fixed responsive sizes and no viewport-scaled type. |
| Layout rhythm | 5 | Sections use repeated grids, cards and bands with consistent spacing. |
| Card and component polish | 5 | Glance cards, idea cards, project cards, safety cards, FAQ and form share the same card system. |
| Tactile maker feeling | 5 | Hero proof points, "practical invention powers", skill family cards and project tiles reinforce build/test/improve. |

Rendered checks:

- Desktop screenshot verified first-screen clarity, hero image, visible CTA and no text overlap.
- True 390px mobile emulation verified no horizontal overflow, visible menu control and full-width CTA.

## Practical Usability Score

Score: 40 / 40

| Criterion | Score | Evidence |
| --- | ---: | --- |
| Navigation | 5 | Nav labels cover parent questions: what children make, ages, curriculum, projects, safety, FAQ and register at `index.html:25-32`. |
| Scannability | 5 | At-a-glance cards answer format, starting point, age pathway and prototype status at `index.html:66-87`. |
| Copy clarity | 5 | Curriculum terms are introduced through parent-facing language before technical labels at `index.html:269-305`. |
| Cognitive load | 5 | Page sequence moves from offer to difference, session shape, ages, curriculum, examples, safety and action. |
| Mobile use | 5 | Chrome DevTools emulation at 390px measured `scrollWidth=390`, menu button `44x44`, nav links `46px` high and Register interest visible in the opened menu. |
| Form clarity | 5 | Final form says the static page does not send data, and the status note repeats that no details are sent at `index.html:586-614`. |
| Performance feel | 5 | Static HTML/CSS/JS only; local checks served `/`, `styles.css`, `script.js` and the hero image with `200 OK`. |
| Task support | 5 | The site directly supports the seven parent tasks in the rubric through hero copy, at-a-glance cards, age pathway, examples, safety, FAQ and final CTA. |

Quantitative checks:

- Primary CTA appears in the first screen.
- Mobile Register interest is reachable from the opened menu.
- Tap targets in mobile nav are at least 44px high.
- 390px emulation has no horizontal overflow.
- Important parent questions are answered in headings, card titles and FAQ summaries.

## Brand Consistency Score

Score: 25 / 25

| Criterion | Score | Evidence |
| --- | ---: | --- |
| Brand promise | 5 | "Children learn to make ideas real" is stated as a promise at `index.html:111-114`. |
| Naming | 5 | The full name "The Invention Club" is used in the brand and hero; no "TIC" shorthand appears. |
| Voice | 5 | Copy is warm, practical and honest about prototype status. |
| Visual brand | 5 | Cards, badges, workshop imagery and the teal/coral/gold palette match the brand rules. |
| Boundary discipline | 5 | The page avoids school prospectus language, dark hacker styling, corporate SaaS styling and production claims. |

## Verification Commands

Commands run:

```text
node --check script.js
curl -I http://127.0.0.1:8000/
curl -I http://127.0.0.1:8000/styles.css
curl -I http://127.0.0.1:8000/script.js
curl -I http://127.0.0.1:8000/assets/invention-workshop-hero.png
Chrome DevTools Protocol mobile layout check at 390px
Quick Look desktop render
Chrome desktop screenshot render
```

Automated source checks confirmed:

- one `h1`;
- early and late "Register interest" CTAs;
- safety nav and section;
- prototype-only form/status copy;
- all five age pathways;
- no backend/payment/auth/CMS markers;
- no leftover scroll-animation experiment classes.

## Remaining Human Review

The page is ready for parent review. The next improvement should come from watching real parents use it, not from adding more visual effects.
