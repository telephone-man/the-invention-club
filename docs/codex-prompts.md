# Codex prompts

Use these prompts in Codex.

## Start with `/plan`

```text
/plan Read AGENTS.md, docs/schema-under-test.md, docs/test-brief.md and docs/failure-conditions.md. Propose a concrete test plan for stress-testing the schema. Do not generate the curriculum yet. Identify what files you will produce, what validation rules you will use, and what would count as success or failure.
```

Review the plan before continuing.

Good signs:
- It attempts to falsify the schema.
- It distinguishes pure skills from integrations.
- It defines failure criteria before generating examples.
- It allows a non-viable conclusion.

Bad signs:
- It tries to make the schema work at all costs.
- It only writes a nice curriculum.
- It avoids edge cases.

## Then use `/goal`

```text
/goal Stress-test the Invention Club curriculum schema in docs/schema-under-test.md against the brief in docs/test-brief.md and failure conditions in docs/failure-conditions.md. Generate toy and realistic sample curricula, red-team edge cases, attempt validation rules, and produce reports/schema-stress-test.md plus canonical curriculum source updates in curriculum/source/curriculum.v1.json. Rebuild generated artefacts with tools/build_curriculum.py; do not hand-author curriculum/generated/*. Success may be “viable”, “viable with amendments”, or “not viable”. Do not force a positive result. Stop when the report gives an evidence-backed verdict and clearly explains blockers or amendments.
```

## Checkpoint prompt

Use this periodically:

```text
Give me a checkpoint summary: current pass, files changed, strongest evidence so far, weakest part of the schema so far, and whether you are leaning viable or non-viable.
```

## Adversarial second pass

After the first report:

```text
Now red-team your own conclusion. Find the strongest argument against your verdict. If you concluded viable, try to prove the schema collapses. If you concluded non-viable, try to find the smallest amendment that rescues it without weakening the original principle.
```

## Minimal amendment prompt

```text
Produce a minimal amendment set.

For each amendment:
- original schema rule
- problem discovered
- proposed change
- evidence from generated cards or edge cases
- downside of the amendment
- whether it is essential or optional
```

## Reminder prompt

Use this if Codex gets too cheerful:

```text
You are not being graded on making the schema work. You are being graded on whether your verdict is evidence-backed.
```
