# Adult Persona Website Feedback

Reviewed: current static website on 2026-06-23

Reviewer stance: adult visitor deciding whether this is worth trust, time, money, and child attention. This pass is deliberately not a curriculum/schema validation and deliberately does not use the website brief as the judging frame.

## Method And Limits

I reviewed the rendered homepage and curriculum page, the current HTML/CSS/JS, and local preview images generated from `index.html` and `curriculum.html`.

Evidence anchors:

- Homepage hero, promise and CTAs: `index.html:35-45`.
- Make/test/improve loop: `index.html:50-84`.
- Age table and unresolved launch age groups: `index.html:89-120`.
- FAQ safety, age availability, school-like positioning and prototype registration: `index.html:143-161`.
- Prototype form and no-submit note: `index.html:167-198`; submit handler reinforces no data sent in `script.js:26-30`.
- Curriculum/card explanation: `curriculum.html:35-82`, `curriculum.html:85-187`, `curriculum.html:191-223`, `curriculum.html:228-381`.
- Mobile/responsive handling is present in CSS, including mobile header/hero changes: `styles.css:1831-1906`.

Validation notes:

- `node --check script.js` passed.
- Local server returned `200 OK` for `index.html` and `curriculum.html`.
- Local reference check found `index.html refs 11 missing 0` and `curriculum.html refs 28 missing 0`.

Limit: the in-app browser setup failed in this environment, so this is based on rendered static previews, source-backed interaction review, and local HTTP validation rather than 100 live browser sessions. The feedback still treats each pass as a visitor journey through the same current pages.

## Shared Audience Frame

I did not model 100 unrelated people. Every reviewer below is an adult who is responsible for, recommending, paying for, transporting, or safeguarding a child who might attend a local enrichment activity.

Shared assumptions:

- They want to know what their child will actually do.
- They need enough trust signals to hand over a child.
- They are comparing this against other uses of family time.
- They are not trying to audit the underlying curriculum.
- They may be excited by making, but they still need practical clarity.

Varied attributes:

- Child age and developmental fit.
- Adult confidence with engineering, coding and making.
- Safety, safeguarding and supervision sensitivity.
- Logistics pressure: price, time, transport, venue, session length.
- Inclusion needs: anxiety, SEND, confidence, gender, prior failure, access.
- Decision stage: curious, comparing, ready to register, cautious referrer.

## 100 Adult Feedback Passes

| # | Reviewer lens | Varied need | Feedback |
| ---: | --- | --- | --- |
| 1 | Parent of a 5-year-old | Safety first | The hero is exciting, but the words "motors" and "sensors" make me look for adult ratios and tool rules quickly. The safety FAQ says arrangements will be confirmed later, so I would not be ready to commit yet. |
| 2 | Parent of a 5-year-old | Adult participation | "Adult-supported" sounds right for 4-6, but I cannot tell whether I stay in the room, help at the table, or drop off. |
| 3 | Parent of a 6-year-old | High-energy child | The make/test/improve loop feels like it could suit a child who learns by doing. I still need session length and whether there is enough movement, not just table work. |
| 4 | Parent of a 6-year-old | Sensitive to noise and mess | The workshop look is appealing, but I cannot tell how loud, crowded, messy, or structured the room will be. |
| 5 | Grandparent | Paying for activity | The offer sounds wholesome and practical. I would need price, term length, and location before I could help pay or book. |
| 6 | Parent of a young child | Materials concern | Cardboard, batteries and parts sound fun, but I want to know what materials are safe for younger children and what is avoided. |
| 7 | Parent with no tech background | Confidence gap | "No coding experience" helps, but motors, sensors and polarity still sound like something I might not understand. Reassure me that parents do not need to prepare or troubleshoot. |
| 8 | Parent with engineering background | Depth check | The card system and levels suggest real structure. I would like a concrete example of what an 8-year-old finishes after three sessions. |
| 9 | Parent of daughter | Belonging | The broad creativity feels less stereotypically "coding club", which is good. I still want a visible inclusion signal that this is for children who do not already see themselves as engineers. |
| 10 | Parent worried about screen time | Physical making | The homepage strongly signals hands-on making, which is reassuring. I would like one plain line saying screens are not the main activity. |
| 11 | Working parent | Scheduling | I understand the concept quickly, but I cannot tell when sessions run, how long they last, or whether they are term-time, weekends, holidays or after school. |
| 12 | Parent comparing clubs | Price/value | The site makes the club feel premium and thoughtful. Without pricing, I cannot compare it to coding, Lego, art or sports clubs. |
| 13 | Parent ready to act | Registration | The main CTA is easy to find. It becomes frustrating when the form says it does not submit yet. |
| 14 | Parent not ready to act | Low-pressure interest | I like that "Register interest" feels softer than booking. It fits a prototype or first cohort well. |
| 15 | Parent who needs contact | Follow-up | I cannot see an email address, phone number, named organiser, or what happens after interest is registered. |
| 16 | Parent with transport constraints | Venue | The "first local sessions" wording is promising, but local to where? I need a town or venue before I can judge feasibility. |
| 17 | Parent with multiple children | Sibling fit | The age table helps, but I cannot tell whether siblings in different age bands can attend at the same time. |
| 18 | Parent with limited budget | Commitment | I need to know whether this is a one-off workshop, trial session, block booking, subscription, or waitlist. |
| 19 | Parent who hates long forms | Form shape | The prototype form asks only three things, which feels respectful. A live version should keep that simplicity. |
| 20 | Parent who wants certainty | Availability | "Initial sessions will launch for selected age groups" is honest but leaves me unsure whether my child is eligible. |
| 21 | Parent of a 4-year-old | Developmental fit | "Stories, big parts and cause-and-effect play" makes the youngest band plausible. I still need reassurance that this is not too advanced or fiddly. |
| 22 | Parent of a 7-year-old | Right challenge | "Buttons, wheels, switches and simple structures" is clear and age-appropriate. This is one of the strongest parts of the homepage. |
| 23 | Parent of a 9-year-old | Stretch | The 8-10.5 band mentions motors, sensors, stronger builds and logic, which sounds rich. I would like examples of projects, not only categories. |
| 24 | Parent of an 11-year-old | Independence | "More self-directed" and robotics/radio control sound attractive. I need proof that the club will not feel babyish. |
| 25 | Parent of a 15-year-old | Teen credibility | "Studio Inventors" sounds ambitious, but the homepage image and playful card language may skew younger unless older work is shown. |
| 26 | Parent of a child between bands | Placement | The 10.5 split is precise but unusual. I would want to know whether placement is by age, maturity, experience, or conversation. |
| 27 | Parent of mixed ability child | Flexibility | The levels on the curriculum page make it seem children can repeat or stretch, which is reassuring. Bring some of that flexibility earlier on the homepage. |
| 28 | Parent of child who dislikes school | Tone | The FAQ line that it is "workshop-first" helps. The curriculum page is still school-like in structure, though less so in language. |
| 29 | Parent of academically advanced child | Rigor | The card system gives real progression. It would be stronger with one sentence about how facilitators decide when to move up a level. |
| 30 | Parent of younger sibling | Mixed ages | I cannot tell whether the full 4-18 range means mixed-age sessions or separate cohorts. This matters for safety and social fit. |
| 31 | Teacher | Learning value | Make/test/improve is a strong learning habit, and the loop is memorable. I would like to see how reflection or sharing happens at the end. |
| 32 | STEM coordinator | Curriculum confidence | The skill families cover a broad engineering space. The public page should not expose too much taxonomy before parents know the offer is real. |
| 33 | Parent who wants creativity | Child-led promise | The site balances structure and freedom well. "Cards guide the loop without taking over" is a good phrase. |
| 34 | Parent who wants measurable progress | Outcomes | "You've earned this power when" on generated cards is concrete. Surface one or two earned-power examples before the curriculum page. |
| 35 | Parent tired of worksheets | Practicality | The visual and copy both say children make real things, not worksheets. That is a strong differentiator. |
| 36 | Parent seeking coding club | Expectation mismatch | I might wonder whether this includes enough coding. The FAQ says coding is one material, but a coding-seeking parent may want clearer positioning. |
| 37 | Parent avoiding coding club | Reassurance | I like that it is not screen-first and not just coding. The phrase "creative engineering" works for me. |
| 38 | Parent concerned about failure | Emotional learning | The repeat/improve loop normalises things not working. That is excellent, but name the emotional benefit more plainly. |
| 39 | Parent who values design thinking | Breadth | "User needs, criteria, feedback and iteration" is good, but buried on the curriculum page. It may reassure parents who worry this is just gadgets. |
| 40 | Parent looking for take-home value | Tangible output | I cannot tell whether children take home builds, photos, cards, badges, notes, or just the experience. |
| 41 | Child-led parent | Motivation | "I want to make it move" is a strong child-facing hook. More examples in that voice would help adults imagine their child choosing. |
| 42 | Parent of cautious child | On-ramp | Level 1 "Encounter" sounds gentle. I like that a child can recognise and handle parts before being expected to build. |
| 43 | Parent of highly confident child | Challenge | The higher levels and integration cards suggest challenge is available. I need a visible route from beginner play to serious builds. |
| 44 | Parent of child who gives up | Persistence | The loop teaches iteration, which is valuable. The site should say facilitators help children through stuck moments. |
| 45 | Parent of child who loves stories | Imagination | Younger group references stories, and invention cards like "Creature with personality" sound engaging. This could be brought into the homepage. |
| 46 | Parent of child who likes rules | Structure | The card and level structure may make the activity feel safe and understandable. Good for children who like clear steps. |
| 47 | Parent of child who hates rules | Freedom | The phrase "without taking over" helps, but the curriculum page still contains many card types. Some children may feel boxed in unless freedom is emphasized. |
| 48 | Parent of social child | Peer aspect | I cannot tell whether children collaborate, share inventions, work in pairs, or mostly build alone. |
| 49 | Parent of shy child | Social safety | I would want to know whether sharing is optional and how facilitators handle confidence. |
| 50 | Parent who wants fun | Energy | The site feels warm and tactile, but some sections are more explanatory than playful. Real child project photos would add delight. |
| 51 | Parent of neurodivergent child | Sensory/access | The site does not mention sensory needs, quiet options, transition support, or predictable routines. |
| 52 | Parent of dyslexic child | Reading load | The homepage is fairly scannable, but the curriculum page has many labels. Icons and short examples help; long taxonomy may still be heavy. |
| 53 | Parent of child with motor difficulties | Accessibility | Hands-on making is appealing but could be worrying. I need to know whether adaptations are possible. |
| 54 | Parent of anxious child | First session | I would like a "what happens in the first 10 minutes" explanation to reduce anxiety. |
| 55 | Parent of child with low confidence | Achievement | The levels and earned powers could be motivating. Show that success can mean noticing, testing or improving, not only finished builds. |
| 56 | Parent concerned about gender inclusion | Social proof | The site avoids macho engineering language, which is good. It still needs inclusive imagery or wording before public launch. |
| 57 | Parent whose child had bad club experience | Trust recovery | The honest prototype wording is good, but I would need stronger safeguarding and behaviour-management information. |
| 58 | Foster carer | Consent and safeguarding | I cannot evaluate suitability without consent, collection, emergency contact, photo policy and safeguarding basics. |
| 59 | Parent of child with allergies | Materials | There is no allergy/materials statement. Even a short "materials vary; tell us needs" line would help. |
| 60 | Parent with accessibility needs | Adult access | I cannot tell whether the venue will be wheelchair accessible or whether adults can communicate access requirements. |
| 61 | Tech-confident parent | Technical credibility | The curriculum examples feel technically plausible. I would enjoy a deeper page, but it should stay optional. |
| 62 | Tech-anxious parent | Intimidation | "Polarity", "loads" and "radio control" could intimidate me. Put the reassuring plain-English examples before technical words. |
| 63 | Maker parent | Materials and tools | I want to know what tools children actually use: scissors, hot glue, soldering, microcontrollers, craft knives, batteries. |
| 64 | Non-maker parent | Home support | I need to know whether this requires buying kits or having parts at home. The site does not say. |
| 65 | Parent with robotics expectations | Scope | The older age band mentions robotics, but the examples are light-touch. I need to know how serious robotics gets. |
| 66 | Parent against screen-heavy clubs | Differentiation | The site successfully differentiates from coding-only clubs. Make that screen-light position explicit without attacking coding. |
| 67 | Parent who values repair | Practical mindset | "Make it work again" and repairability are strong, distinctive ideas. They deserve more parent-facing prominence. |
| 68 | Parent who fears unsafe electronics | Batteries | "Safe batteries" is reassuring but too vague. Parents need concrete guardrails before launch. |
| 69 | Parent who wants modern skills | Future value | The mix of sensors, logic, communication and design feels relevant. It sounds broader than craft and more physical than coding. |
| 70 | Parent who dislikes jargon | Language | "Skill Cards", "Power Cards", "Integration Cards" and "Invention Cards" are understandable one by one, but together may feel like a game system to learn. |
| 71 | Parent comparing to art club | Creativity | The club looks more purposeful than craft but still creative. Show finished artifacts or rough prototypes so the difference is visible. |
| 72 | Parent comparing to coding club | Distinctiveness | The offer is clearly not just coding. This is good, but may need "coding when useful" as a positioning phrase. |
| 73 | Parent comparing to Lego club | Materials | The mixed materials are appealing. I need to know whether children use branded kits, loose parts, recycled materials, electronics or all of these. |
| 74 | Parent comparing to tutoring | Pressure | The site does not feel academically pressured, which is positive. Avoid adding too much curriculum detail to the main parent journey. |
| 75 | Parent comparing to sports | Confidence and teamwork | The site sells thinking and making, but not teamwork, resilience or social confidence as clearly. |
| 76 | Parent comparing holiday camps | Format | I cannot tell whether this is weekly, one-off, camp, after-school or weekend. That is a core decision blocker. |
| 77 | Parent comparing childcare options | Supervision | The site is educational, not childcare-oriented. If parents may use it that way, supervision and collection details matter. |
| 78 | Parent comparing premium clubs | Professionalism | The visual design feels polished and distinctive. Lack of organiser details makes it less trustworthy than the design suggests. |
| 79 | Parent comparing free community activities | Value | I can see the learning value, but without price, equipment included, and facilitator expertise, value is hard to judge. |
| 80 | Parent looking for trial | Risk reduction | A trial or taster session would fit the "first local sessions" stage. The site does not mention whether that exists. |
| 81 | Parent of older child | Autonomy | The "studio" path sounds promising. It needs older-looking examples, not only a general hero image that reads younger. |
| 82 | Parent of teen interested in engineering | Portfolio | I would want to know whether teens create portfolio-worthy builds, documentation, mentoring or public showcases. |
| 83 | Parent of teen not academic | Practical route | The hands-on path could be very appealing for a non-academic teen. Make the older pathway feel credible and not remedial. |
| 84 | Parent of exam-age child | Time trade-off | For 14-18, I need to know session commitment and how it fits around school/exams. |
| 85 | Parent of experienced maker | Avoid repetition | I need to know whether experienced children can skip beginner levels or start with a challenge. |
| 86 | Parent of beginner teen | Shame risk | A teen beginner may not want to be mixed with younger or more skilled children. Grouping needs clarity. |
| 87 | Parent of child interested in electronics | Depth | The power cards show electronics concepts, but I cannot see actual hardware choices or safety limits. |
| 88 | Parent of child interested in design | Design | The "Make it better" family is valuable. It could counterbalance the gadget impression if mentioned earlier. |
| 89 | Parent of child interested in storytelling | Story | The invention-card examples have imagination. Put one of these examples on the homepage to make the offer warmer. |
| 90 | Parent worried about frustration | Facilitation | The site describes what children do but not what adults/facilitators do when a build fails. |
| 91 | School leader | Partnership | The concept could fit enrichment or after-school provision. I need safeguarding, insurance, staffing, space requirements and age cohort plan. |
| 92 | Community venue manager | Practical hosting | The site makes the activity look attractive, but I need room setup, storage, mess, power sockets, cleanup and risk assessment. |
| 93 | PTA organiser | Parent communication | The headline and age table are easy to forward. Missing date, price and location would stop me from circulating it. |
| 94 | Home-ed organiser | Mixed-age group | The broad age range is useful for home-ed families, but mixed-age facilitation needs explaining. |
| 95 | SENCO | Support | The flexible levels are promising. No explicit SEND/access statement means I would need a conversation before referring. |
| 96 | Local employer/mentor | Skills story | The design/build/test loop is a credible skill story. I would want clearer safeguarding and role boundaries before volunteering. |
| 97 | Local council/community funder | Outcomes | The club has a compelling educational purpose. I need outcomes, inclusion reach, and evidence of demand. |
| 98 | Childminder | Drop-off responsibility | I cannot tell whether non-parent carers can register, bring children, or handle consent. |
| 99 | Parent ambassador | Word-of-mouth | The site is easy to describe: children build real ideas. I would still get asked "where, when, how much, is it safe?" immediately. |
| 100 | Cautious general adult | Overall trust | The site makes me interested and gives a clear maker identity. The unresolved launch, safety and registration details keep it in "promising prototype" rather than "ready to join". |

## What Seems Good

These positives came through without relying on the intended website goals:

- The first screen communicates the offer quickly: a named club, hands-on engineering, physical materials, and two clear next actions (`index.html:35-45`).
- The visual direction feels tactile and credible rather than generic education marketing. The previewed homepage reads as a real workshop idea, not just a coding class.
- The make/test/improve loop is memorable and parent-legible (`index.html:50-84`). It frames failure as iteration, which is a real emotional and educational strength.
- The age table is one of the strongest trust-building pieces because it maps age to support level and typical making in plain terms (`index.html:89-120`).
- The FAQ handles some obvious parent objections without over-explaining: no coding experience, not school-like, initial age-group uncertainty, safety not final, and prototype form status (`index.html:143-161`).
- The curriculum page is useful for adults who want depth. It explains cards, levels, repeat/stretch/switch/combine, and bigger challenges with examples (`curriculum.html:35-381`).
- The site is honest that the form is a prototype and does not send data (`index.html:167-198`, `script.js:26-30`). For a prototype, that honesty protects trust.
- The current implementation has no obvious broken local asset references, and both main pages respond locally.

## Worth Improving Or Confusing

These are the highest-frequency and highest-severity issues across the 100 passes:

1. Launch facts are missing.
   Adults repeatedly need venue, location, dates, session length, price, format, first cohort, and whether this is weekly, trial, termly, holiday or waitlist.

2. Safety and safeguarding are not yet actionable.
   The site says full safety, safeguarding and consent arrangements will be confirmed before launch (`index.html:151-153`). That is honest, but for real adult decisions it is the biggest blocker.

3. "Register interest" is clear but currently frustrating.
   The CTA is prominent, but the form does not submit and says no details are sent (`index.html:167-198`, `script.js:26-30`). Fine for internal prototype review; confusing if shared as a real recruitment page.

4. Age breadth creates credibility questions.
   A 4-18 range is ambitious. The age table helps, but adults still need to know which age bands launch first and whether groups are separate (`index.html:89-120`).

5. The curriculum page may be too system-heavy for many adults.
   Skill Cards, Power Cards, levels, Integration Cards and Invention Cards are understandable individually, but together they risk making parents feel there is a game system to learn.

6. Evidence of real outcomes is thin.
   Adults asked for example builds, what children take home, what progress looks like after a few sessions, and older-child examples.

7. Inclusion and access are under-specified.
   SEND, sensory needs, anxious children, motor access, allergies, gender inclusion, venue access and adult communication routes are not visible.

8. Facilitator role is not clear enough.
   The site says what children do, but adults want to know what the adult/facilitator does when a child is stuck, unsafe, frustrated, too fast or too slow.

9. Older teen credibility needs separate proof.
   "Studio Inventors" is promising, but older-child/teen parents need evidence of serious projects, autonomy, mentoring or portfolio value.

10. Contact and follow-up route are absent.
   There is no named organiser, email, privacy note, or "what happens next" path visible in the current site.

## Do Not Overfit The 100 Passes

The feedback is varied, but the site should not try to satisfy every subjective preference. The repeated adult decision blockers are much narrower:

- Confirm the first launch offer.
- Add a concise safety/safeguarding/consent trust block.
- Make the interest/contact route real or label the page as prototype-only before sharing.
- Show a few concrete child outcomes or example builds.
- Clarify age grouping and first cohort.
- Add a short inclusion/access route.

Avoid watering down the strongest positioning. The hands-on, physical, invention-led identity is the best signal on the page. The likely improvement is not more generic reassurance; it is a small number of concrete trust facts around the existing offer.

## Viability Read

For adult review: viable as a prototype.

For public recruitment: viable with specific amendments. It needs launch logistics, safety/safeguarding basics, a real contact/interest route, first-cohort clarity, and a few concrete examples before many adults would move from interest to action.

Ambiguity to keep visible: the current site may be intentionally pre-launch. If so, the no-submit form and unresolved safety/age availability are acceptable prototype boundaries. If the page is shown to real parents as an invitation, those same boundaries become trust and conversion problems.
