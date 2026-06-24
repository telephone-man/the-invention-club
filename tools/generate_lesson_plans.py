#!/usr/bin/env python3
"""Generate facilitator lesson-plan markdown from the canonical curriculum."""

from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

import generate_pilot_micro_packs


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "curriculum/generated/lesson-plans"
DEFAULT_SESSION_OUTPUT_DIR = ROOT / "curriculum/generated/session-lesson-plans"
SESSION_LESSON_PACK_IDS = {"first_session"}
GENERATED_NOTICE = [
    "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
    "Source: curriculum/source/curriculum.v1.json",
    "Rebuild: python3 tools/generate_lesson_plans.py",
    "Status: experimental facilitator planning aid. Review before use. -->",
]
SESSION_GENERATED_NOTICE = [
    "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
    "Source: curriculum/source/curriculum.v1.json",
    "Rebuild: python3 tools/generate_lesson_plans.py",
    "Status: validated facilitator session lesson plan. Review before use. -->",
]


def load_source(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(text: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in text).strip("-").replace("--", "-")


def dependency_closure(card: dict[str, Any], power_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    ordered: OrderedDict[str, dict[str, Any]] = OrderedDict()

    def visit(power_id: str) -> None:
        power = power_by_id.get(power_id)
        if not power or power_id in ordered:
            return
        for dependency_id in power.get("dependencies", []):
            visit(dependency_id)
        ordered[power_id] = power

    for power_id in card.get("required_power_cards", []):
        visit(power_id)
    return list(ordered.values())


def unique_materials(cards: list[dict[str, Any]]) -> list[str]:
    seen: OrderedDict[str, None] = OrderedDict()
    for card in cards:
        for material in card.get("materials", []):
            seen[str(material)] = None
    return list(seen)


def safety_notes(cards: list[dict[str, Any]]) -> list[str]:
    notes = [
        "Use age-appropriate materials and supervised tools.",
        "Disconnect power before changing wiring or moving parts.",
    ]
    families = {card.get("primary_family") for card in cards}
    if "power" in families:
        notes.append("Check polarity, voltage/current suitability, and battery temperature during tests.")
    if "movement" in families:
        notes.append("Keep fingers, loose material, and hair clear of moving mechanisms.")
    if "materials_fabrication" in families:
        notes.append("Pre-set safe cutting, joining, and fastening boundaries before children begin.")
    if "structures" in families:
        notes.append("Test load-bearing parts with small loads before increasing challenge.")
    return notes


def markdown_cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, list):
        text = ", ".join(str(item) for item in value if str(item).strip())
    else:
        text = str(value)
    text = text.strip()
    if not text:
        return "-"
    return text.replace("|", "\\|").replace("\n", "<br>")


def append_table(lines: list[str], headers: list[str], rows: list[list[Any]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    if rows:
        for row in rows:
            lines.append("| " + " | ".join(markdown_cell(value) for value in row) + " |")
    else:
        lines.append("| " + " | ".join("-" for _ in headers) + " |")
    lines.append("")


def card_sequence_by_id(pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item.get("power_card_id"): item
        for item in pack.get("card_sequence", [])
        if isinstance(item, dict) and item.get("power_card_id")
    }


def filtered_steps(pack: dict[str, Any], card_id: str, card: dict[str, Any], section: str) -> list[dict[str, Any]]:
    exclusions = generate_pilot_micro_packs.excluded_asset_ids_by_card(pack)
    return [
        step
        for step in card.get("activity_flow", {}).get(section, [])
        if isinstance(step, dict)
        and not generate_pilot_micro_packs.step_uses_excluded_asset(step, card_id, exclusions)
    ]


def step_text(step: dict[str, Any]) -> str:
    expected = step.get("expected_result")
    if expected:
        return f"{step.get('instruction', '')} Expected evidence: {expected}"
    return str(step.get("instruction", ""))


def render_session_lesson_plan(
    pack: dict[str, Any],
    source: dict[str, Any],
    power_by_id: dict[str, dict[str, Any]],
    family_by_id: dict[str, dict[str, Any]],
    level_by_id: dict[int, dict[str, Any]],
) -> str:
    target_ids = [card_id for card_id in pack.get("target_power_card_ids", []) if card_id in power_by_id]
    target_cards = [power_by_id[card_id] for card_id in target_ids]
    rows = generate_pilot_micro_packs.micro_pack_asset_rows(source, pack)
    assumptions = pack.get("group_size_assumptions", {})
    child_counts = [str(count) for count in assumptions.get("child_counts", [])]
    minutes = assumptions.get("session_minutes", {})
    sequence = card_sequence_by_id(pack)
    diagram_filename = generate_pilot_micro_packs.r_pow_02_diagram_filename(pack)
    target_support = pack.get("target_age_support_assumptions", {})
    families = []
    for card in target_cards:
        family = family_by_id.get(card.get("primary_family"), {})
        if family and family not in families:
            families.append(family)
    levels = []
    for card in target_cards:
        level = level_by_id.get(card.get("level"), {})
        if level and level not in levels:
            levels.append(level)

    lines: list[str] = []
    lines.extend(SESSION_GENERATED_NOTICE)
    lines.extend(["", f"# {pack.get('title', pack.get('id', 'Session Lesson Plan'))}", ""])
    lines.append(f"- Session ID: {pack.get('id', '-')}")
    lines.append(f"- Session length: {minutes.get('min', '-')} to {minutes.get('max', '-')} minutes")
    lines.append(f"- Children: {', '.join(child_counts)}")
    lines.append(f"- Pairing: {assumptions.get('pairing_model', '-')}")
    lines.append(f"- Adults: {pack.get('adult_ratio', {}).get('required_facilitators', '-')} facilitator; {pack.get('adult_ratio', {}).get('recommended_helpers', '-')} helper recommended")
    lines.append("")

    lines.extend(["## Target Age And Support Assumptions", ""])
    lines.append(f"- Target age: {target_support.get('target_age', 'Not specified in canonical source.')}")
    lines.append(f"- Support level: {target_support.get('support_level', '-')}")
    lines.append(f"- Access note: {target_support.get('access_note', '-')}")
    lines.append("")

    lines.extend(["## Learning Objectives", ""])
    for card in target_cards:
        lines.append(f"- {card['id']}: {card.get('i_can_statement', '')}")
    lines.append("")

    lines.extend(["## Linked Power Cards", ""])
    append_table(
        lines,
        ["Card", "Title", "Skill family", "Level", "I-can statement"],
        [
            [
                card.get("id"),
                card.get("title"),
                family_by_id.get(card.get("primary_family"), {}).get("label"),
                f"{card.get('level')} - {level_by_id.get(card.get('level'), {}).get('name')}",
                card.get("i_can_statement"),
            ]
            for card in target_cards
        ],
    )

    lines.extend(["## Relevant Skill Cards And Families", ""])
    for family in families:
        lines.append(f"- {family.get('label')}: {family.get('primary_learning_problem', family.get('summary', ''))}")
    lines.append("")

    lines.extend(["## Level Expectations And Coding Boundary", ""])
    for level in levels:
        lines.append(
            f"- Level {level.get('id')} - {level.get('name')}: {level.get('child_facing_summary')} "
            f"Coding: {level.get('coding_expectation')}"
        )
    lines.append("- Session coding rule: No child-authored code in this session.")
    lines.append("")

    lines.extend(["## Preparation Checklist", ""])
    for item in pack.get("adult_setup_checklist", []):
        lines.append(f"- [ ] {item}")
    for card_id in target_ids:
        for step in filtered_steps(pack, card_id, power_by_id[card_id], "adult_setup"):
            lines.append(f"- [ ] {card_id}: {step.get('instruction', '')}")
    lines.append("")

    lines.extend(["## Room And Table Setup", ""])
    for item in pack.get("packing_assumptions", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.extend(["## Kit List By Bin", ""])
    quantity_headers = [f"{count} children" for count in child_counts]
    append_table(
        lines,
        ["Bin", "Compartment", "Kit", "Item", "Cards", "Basis", "Calc", *quantity_headers, "Return check"],
        [
            [
                row.get("storage", {}).get("bin_id"),
                row.get("storage", {}).get("compartment"),
                row.get("kit_code"),
                row.get("short_label"),
                row.get("power_card_ids"),
                row.get("quantity_basis"),
                row.get("quantity_formula"),
                *[row.get("quantity_by_child_count", {}).get(count) for count in child_counts],
                row.get("return_check"),
            ]
            for row in rows
        ],
    )

    lines.extend(["## Battery Count-Back Sheet", ""])
    count_back_asset_ids = {
        asset_id
        for item in pack.get("reset_count_back", {}).get("battery_count_back", [])
        if isinstance(item, dict)
        for asset_id in item.get("asset_ids", [])
    }
    battery_rows = [row for row in rows if row.get("asset_id") in count_back_asset_ids]
    append_table(
        lines,
        ["Kit", "Item", *quantity_headers, "Before", "After", "Count-back note"],
        [
            [
                row.get("kit_code"),
                row.get("short_label"),
                *[row.get("quantity_by_child_count", {}).get(count) for count in child_counts],
                "",
                "",
                row.get("return_check"),
            ]
            for row in battery_rows
        ],
    )
    for item in pack.get("reset_count_back", {}).get("battery_count_back", []):
        if isinstance(item, dict):
            lines.append(f"- {item.get('note', '')}")
    lines.append("")

    lines.extend(["## Safety Rules", ""])
    for rule in pack.get("safety_rules", []):
        lines.append(f"- {rule}")
    lines.append("")

    lines.extend(["## Timing Plan And Facilitator Script", ""])
    append_table(
        lines,
        ["Time", "Block", "Cards", "Facilitator script"],
        [
            [
                block.get("minutes"),
                block.get("title"),
                ", ".join(block.get("target_power_card_ids", [])) or "-",
                block.get("facilitator_script"),
            ]
            for block in pack.get("timing_blocks", [])
            if isinstance(block, dict)
        ],
    )

    lines.extend(["## Child-Facing Prompts", ""])
    append_table(
        lines,
        ["Card", "Prompt", "Starter question"],
        [
            [
                card_id,
                power_by_id[card_id].get("activity_flow", {}).get("child_start_state", {}).get("prompt"),
                power_by_id[card_id].get("activity_flow", {}).get("child_start_state", {}).get("starter_question"),
            ]
            for card_id in target_ids
        ],
    )

    lines.extend(["## Activity Sequence", ""])
    for card_id in target_ids:
        card = power_by_id[card_id]
        seq = sequence.get(card_id, {})
        lines.append(f"### {card_id} - {card.get('title', '')}")
        lines.append(f"- Purpose: {seq.get('purpose', '-')}")
        for heading, section in (("Build", "build_steps"), ("Test", "test_steps"), ("Debug", "debug_steps")):
            steps = filtered_steps(pack, card_id, card, section)
            if steps:
                lines.append(f"- {heading}:")
                lines.extend(f"  - {step_text(step)}" for step in steps)
        lines.append(f"- Handoff cue: {seq.get('handoff_cue', '-')}")
        lines.append("")

    lines.extend(["## Success And Evidence Criteria", ""])
    append_table(
        lines,
        ["Card", "Success condition", "Stop condition"],
        [
            [
                card_id,
                power_by_id[card_id].get("success_condition"),
                sequence.get(card_id, {}).get("stop_condition"),
            ]
            for card_id in target_ids
        ],
    )

    lines.extend(["## Debug Prompts", ""])
    for card_id in target_ids:
        card = power_by_id[card_id]
        prompts = list(card.get("debug_prompts", []))
        prompts.extend(step.get("instruction", "") for step in filtered_steps(pack, card_id, card, "debug_steps"))
        lines.append(f"### {card_id}")
        lines.extend(f"- {prompt}" for prompt in prompts if str(prompt).strip())
        lines.append("")

    lines.extend(["## Differentiation", ""])
    differentiation = pack.get("lesson_differentiation", {})
    for label, key in (("Simplify", "simplify"), ("Repeat", "repeat"), ("Stretch", "stretch"), ("Stop condition", "stop_condition")):
        lines.append(f"- {label}: {differentiation.get(key, '-')}")
    lines.append("")

    lines.extend(["## Reset And Pack-Away Checklist", ""])
    for step in pack.get("reset_count_back", {}).get("pack_away_steps", []):
        lines.append(f"- [ ] {step}")
    for card_id in target_ids:
        for step in filtered_steps(pack, card_id, power_by_id[card_id], "reset_and_pack"):
            lines.append(f"- [ ] {card_id}: {step.get('instruction', '')}")
    lines.append("")

    lines.extend(["## Assessment And Observation Notes", ""])
    for note in pack.get("pilot_observation_focus", []):
        lines.append(f"- {note}")
    lines.append("")

    lines.extend(["## Follow-Up Recommendations", ""])
    for recommendation in pack.get("follow_up_recommendations", []):
        lines.append(f"- {recommendation}")
    lines.append("")

    lines.extend(["## Deliberately Deferred Cards", ""])
    append_table(
        lines,
        ["Card", "Reason"],
        [
            [item.get("power_card_id"), item.get("reason")]
            for item in pack.get("deferred_power_cards", [])
            if isinstance(item, dict)
        ],
    )

    lines.extend(["## Diagram Reference", ""])
    lines.append(f"- r_pow_02 safe circuit: `../pilot-micro-packs/{diagram_filename}`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_integration_plan(
    integration: dict[str, Any],
    source: dict[str, Any],
    power_by_id: dict[str, dict[str, Any]],
    family_by_id: dict[str, dict[str, Any]],
) -> str:
    required = dependency_closure(integration, power_by_id)
    required_ids = set(integration.get("required_power_cards", []))
    prerequisites = [card for card in required if card["id"] not in required_ids]
    direct_cards = [power_by_id[card_id] for card_id in integration.get("required_power_cards", []) if card_id in power_by_id]
    family_labels = [family_by_id[family_id]["label"] for family_id in integration.get("families_combined", []) if family_id in family_by_id]
    matching_inventions = [
        invention
        for invention in source.get("invention_cards", [])
        if set(integration.get("families_combined", [])) & set(invention.get("possible_skill_families", []))
    ][:3]

    lines = [
        *GENERATED_NOTICE,
        "",
        f"# {integration['title']}",
        "",
        "Generated facilitator lesson plan. Review safety, materials, age fit, and support needs before use.",
        "",
        "## Card Type",
        "",
        "Integration Card - fixed challenge using named Power Cards from different Skill Cards.",
        "",
        "## Challenge",
        "",
        integration["challenge"],
        "",
        "## Families Combined",
        "",
        *[f"- {label}" for label in family_labels],
        "",
        "## Required Power Cards",
        "",
        *[
            f"- Level {card['level']} {family_by_id[card['primary_family']]['label']}: {card['title']} - {card['i_can_statement']}"
            for card in direct_cards
        ],
        "",
    ]

    if prerequisites:
        lines.extend(
            [
                "## Useful Prerequisites",
                "",
                *[
                    f"- Level {card['level']} {family_by_id[card['primary_family']]['label']}: {card['title']}"
                    for card in prerequisites
                ],
                "",
            ]
        )

    lines.extend(
        [
            "## Materials",
            "",
            *[f"- {material}" for material in unique_materials(required)],
            "",
            "## Success Condition",
            "",
            integration["success_condition"],
            "",
            "## Debug Prompts",
            "",
            *[
                f"- {prompt}"
                for card in direct_cards
                for prompt in card.get("debug_prompts", [])
            ],
            "",
            "## Choice Points",
            "",
            *[f"- {choice}" for choice in integration.get("choice_points", [])],
            "",
            "## Make It Yours",
            "",
            *[f"- {prompt}" for prompt in integration.get("make_it_yours_prompts", [])],
            "",
            "## Safety Notes",
            "",
            *[f"- {note}" for note in safety_notes(required)],
            "",
        ]
    )

    if matching_inventions:
        lines.extend(
            [
                "## Possible Follow-On Invention Cards",
                "",
                *[
                    f"- {invention['theme']}: {invention['open_ended_challenge']}"
                    for invention in matching_inventions
                ],
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def write_integration_lesson_outputs(source: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale_path in output_dir.glob("integration-*.md"):
        stale_path.unlink()
    index_path = output_dir / "index.md"
    if index_path.exists():
        index_path.unlink()

    power_by_id = {card["id"]: card for card in source["power_cards"]}
    family_by_id = {family["id"]: family for family in source["skill_cards"]}
    generated_files = []

    for integration in source["integration_cards"]:
        filename = f"integration-{integration['id']}-{slug(integration['title'])}.md"
        output_path = output_dir / filename
        output_path.write_text(
            render_integration_plan(integration, source, power_by_id, family_by_id),
            encoding="utf-8",
        )
        generated_files.append(filename)

    index_lines = [
        *GENERATED_NOTICE,
        "",
        "# Generated Lesson Plans",
        "",
        "These files are generated from `curriculum/source/curriculum.v1.json`.",
        "They are facilitator-facing planning aids, not public website content.",
        "",
    ]
    index_lines.extend(f"- [{filename}]({filename})" for filename in generated_files)
    (output_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def write_session_lesson_outputs(source: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale_path in output_dir.glob("*.md"):
        stale_path.unlink()

    power_by_id = {card["id"]: card for card in source["power_cards"]}
    family_by_id = {family["id"]: family for family in source["skill_cards"]}
    level_by_id = {level["id"]: level for level in source["levels"]}
    generated_files = []

    for pack in source.get("pilot_micro_packs", []):
        if pack.get("id") not in SESSION_LESSON_PACK_IDS:
            continue
        filename = f"{generate_pilot_micro_packs.slugify(pack['id'])}.md"
        output_path = output_dir / filename
        output_path.write_text(
            render_session_lesson_plan(pack, source, power_by_id, family_by_id, level_by_id),
            encoding="utf-8",
        )
        generated_files.append((filename, pack.get("title", pack["id"])))

    index_lines = [
        *SESSION_GENERATED_NOTICE,
        "",
        "# Generated Session Lesson Plans",
        "",
        "These facilitator-facing session lesson plans are generated from canonical pilot micro-pack data.",
        "They are distinct from the legacy Integration Card lesson-plan drafts.",
        "",
    ]
    index_lines.extend(f"- [{title}]({filename})" for filename, title in generated_files)
    (output_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def generate(source_path: Path, output_dir: Path, session_output_dir: Path = DEFAULT_SESSION_OUTPUT_DIR) -> None:
    source = load_source(source_path)
    write_integration_lesson_outputs(source, output_dir)
    write_session_lesson_outputs(source, session_output_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--session-output-dir", default=str(DEFAULT_SESSION_OUTPUT_DIR))
    args = parser.parse_args()
    generate(Path(args.source), Path(args.output_dir), Path(args.session_output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
