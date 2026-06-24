#!/usr/bin/env python3
"""Generate facilitator lesson-plan markdown from the canonical curriculum."""

from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "curriculum/generated/lesson-plans"
GENERATED_NOTICE = [
    "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
    "Source: curriculum/source/curriculum.v1.json",
    "Rebuild: python3 tools/generate_lesson_plans.py",
    "Status: experimental facilitator planning aid. Review before use. -->",
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


def generate(source_path: Path, output_dir: Path) -> None:
    source = load_source(source_path)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()
    generate(Path(args.source), Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
