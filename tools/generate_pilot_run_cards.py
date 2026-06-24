#!/usr/bin/env python3
"""Generate operational pilot facilitator run-card markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "curriculum/generated/pilot-run-cards"
PILOT_KIT_FAMILIES = {"movement", "control_input", "sensing", "power", "structures"}
PILOT_KIT_LEVELS = {1, 2}
GENERATED_NOTICE = [
    "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
    "Source: curriculum/source/curriculum.v1.json",
    "Rebuild: python3 tools/build_curriculum.py",
    "Direct rebuild: python3 tools/generate_pilot_run_cards.py",
    "Status: operational pilot facilitator run-card pack. Review before use. -->",
]


def load_source(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def markdown_list(items: list[Any] | None) -> str:
    if not items:
        return "-"
    return ", ".join(str(item) for item in items if str(item).strip()) or "-"


def pilot_kit_cards(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        card
        for card in source.get("power_cards", [])
        if card.get("primary_family") in PILOT_KIT_FAMILIES and card.get("level") in PILOT_KIT_LEVELS
    ]


def asset_maps(source: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    inventory = source.get("asset_inventory", {})
    physical_assets_by_id = {
        asset.get("id"): asset
        for asset in inventory.get("physical_assets", [])
        if isinstance(asset, dict) and asset.get("id")
    }
    preload_profiles_by_id = {
        profile.get("id"): profile
        for profile in inventory.get("programmable_preload_profiles", [])
        if isinstance(profile, dict) and profile.get("id")
    }
    return physical_assets_by_id, preload_profiles_by_id


def pilot_asset_detail(
    requirement: dict[str, Any],
    physical_assets_by_id: dict[str, dict[str, Any]],
    preload_profiles_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    asset = physical_assets_by_id.get(requirement.get("asset_id"), {})
    safety = asset.get("safety", {}) if isinstance(asset.get("safety"), dict) else {}
    storage = asset.get("storage", {}) if isinstance(asset.get("storage"), dict) else {}
    detail = {
        "asset_id": requirement.get("asset_id"),
        "kit_code": asset.get("kit_code", ""),
        "label": asset.get("label", ""),
        "short_label": asset.get("short_label") or asset.get("label", ""),
        "category": asset.get("category", ""),
        "quantity": requirement.get("quantity"),
        "quantity_basis": requirement.get("quantity_basis"),
        "preparation_state": requirement.get("preparation_state"),
        "preparation_notes": requirement.get("preparation_notes", ""),
        "programming_state": requirement.get("programming_state"),
        "storage": storage,
        "safety_flags": safety.get("hazards", []),
        "supervision_level": safety.get("supervision_level", ""),
        "inspection_check": safety.get("inspection_check", ""),
        "return_check": safety.get("return_check", ""),
    }

    preload_profile_id = requirement.get("preload_profile_id")
    if preload_profile_id:
        preload_profile = preload_profiles_by_id.get(preload_profile_id, {})
        detail["preload_profile_id"] = preload_profile_id
        detail["preload_profile_label"] = preload_profile.get("label", "")
        detail["preload_profile_description"] = preload_profile.get("description", "")
        detail["preload_profile_adult_preparation_notes"] = preload_profile.get("adult_preparation_notes", "")
    if detail["programming_state"] is None:
        detail.pop("programming_state")
    return detail


def pilot_run_card_records(source: dict[str, Any]) -> list[dict[str, Any]]:
    physical_assets_by_id, preload_profiles_by_id = asset_maps(source)
    families_by_id = {
        family.get("id"): family for family in source.get("skill_cards", []) if isinstance(family, dict)
    }
    levels_by_id = {
        level.get("id"): level for level in source.get("levels", []) if isinstance(level, dict)
    }

    records = []
    for card in pilot_kit_cards(source):
        assets = [
            pilot_asset_detail(requirement, physical_assets_by_id, preload_profiles_by_id)
            for requirement in card.get("required_assets", [])
            if isinstance(requirement, dict)
        ]
        family = families_by_id.get(card.get("primary_family"), {})
        level = levels_by_id.get(card.get("level"), {})
        records.append(
            {
                "power_card_id": card.get("id"),
                "title": card.get("title", ""),
                "skill_card_id": card.get("primary_family", ""),
                "skill_family_label": family.get("label") or family.get("name", ""),
                "level": card.get("level"),
                "level_name": level.get("name", ""),
                "i_can_statement": card.get("i_can_statement", ""),
                "success_condition": card.get("success_condition", ""),
                "assets": assets,
                "activity_flow": card.get("activity_flow", {}),
            }
        )
    return records


def append_table(lines: list[str], headers: list[str], rows: list[list[Any]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    if rows:
        for row in rows:
            lines.append("| " + " | ".join(markdown_cell(value) for value in row) + " |")
    else:
        lines.append("| " + " | ".join("-" for _ in headers) + " |")
    lines.append("")


def step_line(step: dict[str, Any], asset_labels_by_id: dict[str, str]) -> str:
    actor = step.get("actor", "-")
    kind = step.get("kind", "-")
    instruction = step.get("instruction", "")
    extras = []
    asset_ids = step.get("asset_ids") or []
    if asset_ids:
        extras.append(
            "assets: "
            + ", ".join(asset_labels_by_id.get(asset_id, asset_id) for asset_id in asset_ids)
        )
    safety_focus = step.get("safety_focus") or []
    if safety_focus:
        extras.append("safety: " + markdown_list(safety_focus))
    expected_result = step.get("expected_result")
    if expected_result:
        extras.append("expected: " + str(expected_result))
    diagram_node_ids = step.get("diagram_node_ids") or []
    if diagram_node_ids:
        extras.append("diagram nodes: " + markdown_list(diagram_node_ids))

    suffix = f" ({'; '.join(extras)})" if extras else ""
    return f"- [{actor} / {kind}] {instruction}{suffix}"


def append_step_section(
    lines: list[str],
    heading: str,
    steps: list[dict[str, Any]],
    asset_labels_by_id: dict[str, str],
) -> None:
    lines.extend([f"##### {heading}", ""])
    for step in steps:
        if isinstance(step, dict):
            lines.append(step_line(step, asset_labels_by_id))
    lines.append("")


def append_child_start(
    lines: list[str],
    child_start: dict[str, Any],
    asset_labels_by_id: dict[str, str],
) -> None:
    lines.extend(["##### Child Start State", ""])
    lines.append(f"- Prompt: {child_start.get('prompt', '-')}")
    lines.append(f"- Starter question: {child_start.get('starter_question', '-')}")
    visible_assets = child_start.get("visible_asset_ids") or []
    visible = [asset_labels_by_id.get(asset_id, asset_id) for asset_id in visible_assets]
    lines.append(f"- Visible assets: {markdown_list(visible)}")
    lines.append("")


def append_preload_notes(lines: list[str], assets: list[dict[str, Any]]) -> None:
    preloaded_assets = [asset for asset in assets if asset.get("preload_profile_id")]
    lines.extend(["##### Preload Profile Notes", ""])
    if not preloaded_assets:
        lines.extend(["- No preloaded board profile required.", ""])
        return
    for asset in preloaded_assets:
        label = asset.get("preload_profile_label") or "-"
        profile_id = asset.get("preload_profile_id") or "-"
        lines.append(f"- {profile_id} - {label}")
        if asset.get("preload_profile_description"):
            lines.append(f"  - Profile: {asset['preload_profile_description']}")
        if asset.get("preload_profile_adult_preparation_notes"):
            lines.append(f"  - Adult prep: {asset['preload_profile_adult_preparation_notes']}")
    lines.append("")


def append_diagram(lines: list[str], flow: dict[str, Any]) -> None:
    diagram = flow.get("diagram_semantics")
    lines.extend(["##### Diagram Semantics", ""])
    diagram_refs = flow.get("diagram_refs") if isinstance(flow.get("diagram_refs"), list) else []
    if diagram_refs:
        lines.append("- Diagram refs:")
        for ref in diagram_refs:
            if isinstance(ref, dict):
                ref_id = ref.get("id") or ref.get("diagram_id") or "-"
                ref_kind = ref.get("kind") or ref.get("type") or "-"
                ref_note = ref.get("note") or ref.get("description") or "-"
                lines.append(f"  - {ref_id} ({ref_kind}): {ref_note}")
        lines.append("")

    if not isinstance(diagram, dict):
        lines.append("- Diagram placeholder: no diagram semantics supplied.")
        lines.append("")
        return

    lines.append(f"- Primary view: {diagram.get('primary_view', '-')}")
    lines.append("")
    nodes = diagram.get("nodes") if isinstance(diagram.get("nodes"), list) else []
    append_table(
        lines,
        ["Node", "Asset", "Role", "Label"],
        [
            [node.get("id"), node.get("asset_id"), node.get("role"), node.get("label")]
            for node in nodes
            if isinstance(node, dict)
        ],
    )

    connections = diagram.get("connections") if isinstance(diagram.get("connections"), list) else []
    if connections:
        append_table(
            lines,
            ["From", "To", "Kind", "Made By"],
            [
                [
                    connection.get("from"),
                    connection.get("to"),
                    connection.get("kind"),
                    connection.get("made_by"),
                ]
                for connection in connections
                if isinstance(connection, dict)
            ],
        )
    else:
        lines.extend(["- Connections: none.", ""])

    states = diagram.get("states") if isinstance(diagram.get("states"), list) else []
    if states:
        append_table(
            lines,
            ["State", "Trigger", "Expected Change"],
            [
                [state.get("id"), state.get("trigger"), state.get("expected_change")]
                for state in states
                if isinstance(state, dict)
            ],
        )
    else:
        lines.extend(["- States: none.", ""])


def render_run_card(record: dict[str, Any]) -> list[str]:
    assets = record.get("assets", [])
    asset_labels_by_id = {
        asset.get("asset_id"): f"{asset.get('kit_code') or '-'} {asset.get('short_label') or asset.get('asset_id')}"
        for asset in assets
        if isinstance(asset, dict) and asset.get("asset_id")
    }
    flow = record.get("activity_flow", {}) if isinstance(record.get("activity_flow"), dict) else {}

    lines = [
        f"#### {record['power_card_id']} - {record['title']}",
        "",
        f"- Skill family: {record.get('skill_family_label') or record.get('skill_card_id')}",
        f"- Level: {record.get('level')} - {record.get('level_name') or '-'}",
        f"- I-can statement: {record.get('i_can_statement') or '-'}",
        f"- Success condition: {record.get('success_condition') or '-'}",
        "",
        "##### Kit Pick List",
        "",
    ]
    append_table(
        lines,
        [
            "Kit Code",
            "Short Label",
            "Qty",
            "Basis",
            "Prep State",
            "Prep Notes",
            "Bin",
            "Compartment",
            "Return Location",
        ],
        [
            [
                asset.get("kit_code"),
                asset.get("short_label"),
                asset.get("quantity"),
                asset.get("quantity_basis"),
                asset.get("preparation_state"),
                asset.get("preparation_notes"),
                asset.get("storage", {}).get("bin_id"),
                asset.get("storage", {}).get("compartment"),
                asset.get("storage", {}).get("return_location"),
            ]
            for asset in assets
            if isinstance(asset, dict)
        ],
    )

    lines.extend(["##### Safety and Prep", ""])
    append_table(
        lines,
        ["Kit Code", "Safety Flags", "Supervision Notes", "Inspection Check", "Return Check", "Preload"],
        [
            [
                asset.get("kit_code"),
                markdown_list(asset.get("safety_flags")),
                f"Level: {asset.get('supervision_level') or '-'}",
                asset.get("inspection_check"),
                asset.get("return_check"),
                (
                    f"{asset.get('preload_profile_id')} - {asset.get('preload_profile_label')}"
                    if asset.get("preload_profile_id")
                    else "-"
                ),
            ]
            for asset in assets
            if isinstance(asset, dict)
        ],
    )
    append_preload_notes(lines, assets)

    append_step_section(lines, "Adult Setup", flow.get("adult_setup", []), asset_labels_by_id)
    append_child_start(lines, flow.get("child_start_state", {}), asset_labels_by_id)
    append_step_section(lines, "Build Steps", flow.get("build_steps", []), asset_labels_by_id)
    append_step_section(lines, "Test Steps", flow.get("test_steps", []), asset_labels_by_id)
    append_step_section(lines, "Debug Steps", flow.get("debug_steps", []), asset_labels_by_id)
    append_step_section(lines, "Reset and Pack-Away", flow.get("reset_and_pack", []), asset_labels_by_id)

    lines.extend(["##### Facilitator Notes", ""])
    for note in flow.get("facilitator_notes", []):
        lines.append(f"- {note}")
    lines.append("")
    append_diagram(lines, flow)
    return lines


def render_pilot_run_cards_markdown(records: list[dict[str, Any]]) -> str:
    lines = [
        *GENERATED_NOTICE,
        "",
        "# Generated Pilot Facilitator Run-Card Pack",
        "",
        "Operational run-cards for the current 20-card Level 1-2 pilot scope.",
        "These are generated from canonical curriculum data and are not final lesson plans.",
        "",
        "## Pilot Scope",
        "",
        f"- Power Cards: {len(records)}",
        "- Levels: 1-2",
        "- Skill families: Movement, Control/Input, Sensing, Structures, Power",
        "",
    ]

    current_family: str | None = None
    current_level: tuple[Any, Any] | None = None
    for record in records:
        family = record.get("skill_family_label") or record.get("skill_card_id")
        if family != current_family:
            current_family = family
            current_level = None
            lines.extend([f"## {family}", ""])

        level_key = (record.get("level"), record.get("level_name"))
        if level_key != current_level:
            current_level = level_key
            lines.extend([f"### Level {record.get('level')} - {record.get('level_name') or '-'}", ""])

        lines.extend(render_run_card(record))

    return "\n".join(lines).rstrip() + "\n"


def expected_pilot_run_cards_markdown(source: dict[str, Any]) -> str:
    return render_pilot_run_cards_markdown(pilot_run_card_records(source))


def generate(source_path: Path, output_dir: Path) -> Path:
    source = load_source(source_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.md"
    output_path.write_text(expected_pilot_run_cards_markdown(source), encoding="utf-8")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()
    generate(Path(args.source), Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
