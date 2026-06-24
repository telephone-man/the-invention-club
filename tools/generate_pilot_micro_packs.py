#!/usr/bin/env python3
"""Generate narrow pilot micro-pack operational aids."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_OUTPUT_DIR = ROOT / "curriculum/generated/pilot-micro-packs"
GENERATED_NOTICE = [
    "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
    "Source: curriculum/source/curriculum.v1.json",
    "Rebuild: python3 tools/build_curriculum.py",
    "Status: generated operational pilot micro-pack. Review before use. -->",
]


def load_source(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


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


def power_cards_by_id(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        card.get("id"): card
        for card in source.get("power_cards", [])
        if isinstance(card, dict) and card.get("id")
    }


def physical_assets_by_id(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        asset.get("id"): asset
        for asset in source.get("asset_inventory", {}).get("physical_assets", [])
        if isinstance(asset, dict) and asset.get("id")
    }


def pair_count_for_children(child_count: int, assumptions: dict[str, Any]) -> int:
    explicit = assumptions.get("pair_counts_by_child_count", {})
    if isinstance(explicit, dict):
        value = explicit.get(str(child_count))
        if isinstance(value, int) and value > 0:
            return value
    return math.ceil(child_count / 2)


def quantity_for_children(requirement: dict[str, Any], child_count: int, assumptions: dict[str, Any]) -> int:
    quantity = int(requirement.get("quantity") or 0)
    basis = requirement.get("quantity_basis")
    if basis == "per_child":
        return quantity * child_count
    if basis == "per_pair":
        return quantity * pair_count_for_children(child_count, assumptions)
    if basis == "per_table":
        return quantity * int(assumptions.get("table_count") or 1)
    if basis in {"per_session", "demo_only"}:
        return quantity
    return quantity


def quantity_formula(requirement: dict[str, Any], assumptions: dict[str, Any]) -> str:
    quantity = int(requirement.get("quantity") or 0)
    basis = str(requirement.get("quantity_basis") or "")
    if basis == "per_pair":
        child_counts = assumptions.get("child_counts", [])
        pairs = ", ".join(
            f"{child_count} children={pair_count_for_children(int(child_count), assumptions)} pairs"
            for child_count in child_counts
        )
        return f"{quantity} x pair count ({pairs})"
    if basis == "per_table":
        return f"{quantity} x {int(assumptions.get('table_count') or 1)} table"
    if basis == "per_child":
        return f"{quantity} x child count"
    if basis == "demo_only":
        return f"{quantity} adult-controlled demo item"
    if basis == "per_session":
        return f"{quantity} per session"
    return str(quantity)


def asset_detail(
    requirement: dict[str, Any],
    assets_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    asset = assets_by_id.get(requirement.get("asset_id"), {})
    safety = asset.get("safety", {}) if isinstance(asset.get("safety"), dict) else {}
    return {
        "asset_id": requirement.get("asset_id"),
        "kit_code": asset.get("kit_code", ""),
        "label": asset.get("label", ""),
        "short_label": asset.get("short_label") or asset.get("label", ""),
        "category": asset.get("category", ""),
        "quantity": requirement.get("quantity"),
        "quantity_basis": requirement.get("quantity_basis"),
        "preparation_state": requirement.get("preparation_state"),
        "preparation_notes": requirement.get("preparation_notes", ""),
        "storage": asset.get("storage", {}),
        "safety_flags": safety.get("hazards", []),
        "supervision_level": safety.get("supervision_level", ""),
        "inspection_check": safety.get("inspection_check", ""),
        "return_check": safety.get("return_check", ""),
    }


def excluded_asset_ids_by_card(pack: dict[str, Any]) -> dict[str, dict[str, str]]:
    exclusions: dict[str, dict[str, str]] = {}
    for exclusion in pack.get("asset_exclusions", []):
        if not isinstance(exclusion, dict):
            continue
        card_id = str(exclusion.get("power_card_id", ""))
        asset_id = str(exclusion.get("asset_id", ""))
        if card_id and asset_id:
            exclusions.setdefault(card_id, {})[asset_id] = str(exclusion.get("reason", ""))
    return exclusions


def step_uses_excluded_asset(step: dict[str, Any], card_id: str, exclusions: dict[str, dict[str, str]]) -> bool:
    excluded_for_card = set(exclusions.get(card_id, {}))
    if not excluded_for_card:
        return False
    return any(asset_id in excluded_for_card for asset_id in step.get("asset_ids", []))


def micro_pack_asset_rows(source: dict[str, Any], pack: dict[str, Any]) -> list[dict[str, Any]]:
    power_by_id = power_cards_by_id(source)
    assets_by_id = physical_assets_by_id(source)
    assumptions = pack.get("group_size_assumptions", {})
    child_counts = [int(count) for count in assumptions.get("child_counts", [])]
    exclusions = excluded_asset_ids_by_card(pack)
    rows_by_key: dict[tuple[str, str, str], dict[str, Any]] = {}

    for card_id in pack.get("target_power_card_ids", []):
        card = power_by_id.get(card_id, {})
        for requirement in card.get("required_assets", []):
            if not isinstance(requirement, dict):
                continue
            asset_id = str(requirement.get("asset_id", ""))
            if asset_id in exclusions.get(str(card_id), {}):
                continue
            detail = asset_detail(requirement, assets_by_id)
            key = (
                str(detail.get("asset_id", "")),
                str(detail.get("quantity_basis", "")),
                str(detail.get("preparation_state", "")),
            )
            if key not in rows_by_key:
                rows_by_key[key] = {
                    **detail,
                    "power_card_ids": [],
                    "quantity_by_child_count": {str(count): 0 for count in child_counts},
                    "quantity_formula": quantity_formula(requirement, assumptions),
                }
            row = rows_by_key[key]
            if card_id not in row["power_card_ids"]:
                row["power_card_ids"].append(card_id)
            for child_count in child_counts:
                calculated = quantity_for_children(requirement, child_count, assumptions)
                current = int(row["quantity_by_child_count"].get(str(child_count), 0))
                row["quantity_by_child_count"][str(child_count)] = max(current, calculated)

    return sorted(
        rows_by_key.values(),
        key=lambda row: (
            str(row.get("storage", {}).get("bin_id", "")),
            int(row.get("storage", {}).get("pack_order") or 0),
            str(row.get("kit_code", "")),
            str(row.get("asset_id", "")),
        ),
    )


def r_pow_02_diagram_filename(pack: dict[str, Any]) -> str:
    for ref in pack.get("diagram_refs", []):
        if isinstance(ref, dict) and ref.get("power_card_id") == "r_pow_02":
            filename = str(ref.get("output_filename", "")).strip()
            if filename:
                return filename
    return f"{slugify(str(pack.get('id', 'first-session')))}-r_pow_02-safe-circuit.svg"


def asset_label(asset_id: str, assets_by_id: dict[str, dict[str, Any]]) -> str:
    asset = assets_by_id.get(asset_id, {})
    kit_code = asset.get("kit_code")
    short_label = asset.get("short_label") or asset.get("label") or asset_id
    return f"{kit_code} {short_label}".strip()


def render_r_pow_02_safe_circuit_svg(source: dict[str, Any]) -> str:
    assets_by_id = physical_assets_by_id(source)
    battery = asset_label("part_aa_battery_pack", assets_by_id)
    led = asset_label("part_led_module", assets_by_id)
    leads = asset_label("part_croc_clip_lead", assets_by_id)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="760" viewBox="0 0 1100 760" role="img" aria-labelledby="title desc">
  <title id="title">r_pow_02 safe LED circuit</title>
  <desc id="desc">Battery pack connected to LED module with positive and negative clip leads after adult check.</desc>
  <rect width="1100" height="760" fill="#fffaf0"/>
  <rect x="40" y="40" width="1020" height="680" rx="24" fill="#f5eee2" stroke="#24211f" stroke-width="6"/>
  <text x="72" y="104" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#063d42">r_pow_02: Power one load - LED module only</text>
  <text x="72" y="144" font-family="Arial, sans-serif" font-size="22" fill="#24211f">No loose AA cells. Battery pack switch stays OFF until adult check is complete.</text>

  <rect x="110" y="250" width="290" height="170" rx="18" fill="#2b2f34" stroke="#24211f" stroke-width="6"/>
  <rect x="136" y="288" width="86" height="74" rx="10" fill="#f4be38" stroke="#24211f" stroke-width="4"/>
  <rect x="246" y="288" width="86" height="74" rx="10" fill="#fffaf0" stroke="#24211f" stroke-width="4"/>
  <text x="155" y="335" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#24211f">+</text>
  <text x="270" y="335" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#24211f">-</text>
  <rect x="238" y="380" width="120" height="32" rx="8" fill="#fffaf0" stroke="#24211f" stroke-width="4"/>
  <text x="255" y="403" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#b94b3f">SWITCH OFF</text>
  <text x="110" y="462" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#063d42">{battery}</text>

  <rect x="720" y="270" width="260" height="130" rx="18" fill="#ffffff" stroke="#24211f" stroke-width="6"/>
  <circle cx="800" cy="335" r="34" fill="#f15f45" stroke="#24211f" stroke-width="5"/>
  <path d="M790 335h20M800 325v20" stroke="#24211f" stroke-width="5" stroke-linecap="round"/>
  <circle cx="900" cy="335" r="34" fill="#dbe8f0" stroke="#24211f" stroke-width="5"/>
  <path d="M888 335h24" stroke="#24211f" stroke-width="5" stroke-linecap="round"/>
  <text x="720" y="442" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#063d42">{led}</text>

  <path d="M400 302 C505 190 620 190 720 302" fill="none" stroke="#d54a3a" stroke-width="14" stroke-linecap="round"/>
  <path d="M400 370 C510 520 620 520 720 370" fill="none" stroke="#24211f" stroke-width="14" stroke-linecap="round"/>
  <text x="494" y="205" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#b94b3f">positive lead</text>
  <text x="500" y="540" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#24211f">negative return</text>
  <text x="486" y="590" font-family="Arial, sans-serif" font-size="20" fill="#24211f">Use {leads}; connect only after the adult checks polarity and path.</text>

  <rect x="420" y="282" width="260" height="112" rx="12" fill="#f4be38" stroke="#24211f" stroke-width="5"/>
  <text x="448" y="325" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#24211f">ADULT CHECK</text>
  <text x="448" y="358" font-family="Arial, sans-serif" font-size="18" fill="#24211f">before power on</text>

  <rect x="88" y="606" width="924" height="56" rx="12" fill="#ffffff" stroke="#24211f" stroke-width="4"/>
  <text x="116" y="642" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#063d42">First pilot rule: LED module only. Do not use the optional motor comparison load in this session.</text>
</svg>
'''


def render_micro_pack_markdown(source: dict[str, Any], pack: dict[str, Any]) -> str:
    power_by_id = power_cards_by_id(source)
    rows = micro_pack_asset_rows(source, pack)
    assumptions = pack.get("group_size_assumptions", {})
    child_counts = [int(count) for count in assumptions.get("child_counts", [])]
    diagram_filename = r_pow_02_diagram_filename(pack)
    exclusions = excluded_asset_ids_by_card(pack)

    lines: list[str] = []
    lines.extend(GENERATED_NOTICE)
    lines.extend(["", f"# {pack.get('title', pack.get('id', 'Pilot micro-pack'))}", ""])
    lines.append(f"- Session ID: {pack.get('id', '-')}")
    lines.append(f"- Target Power Cards: {', '.join(pack.get('target_power_card_ids', []))}")
    minutes = assumptions.get("session_minutes", {})
    lines.append(f"- Session length: {minutes.get('min', '-')} to {minutes.get('max', '-')} minutes")
    lines.append(f"- Children: {', '.join(str(count) for count in child_counts)}")
    lines.append(
        "- Pair model: "
        + str(assumptions.get("pairing_model", "pairs; one trio when the child count is odd"))
    )
    lines.append(f"- Tables/stations: {assumptions.get('table_count', 1)}")
    adult_ratio = pack.get("adult_ratio", {})
    lines.append(
        f"- Adults: {adult_ratio.get('required_facilitators', '-')} facilitator; "
        f"{adult_ratio.get('recommended_helpers', '-')} helper recommended"
    )
    lines.append("")

    lines.extend(["## One-Page Facilitator Timing Script", ""])
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

    lines.extend(["## Safety Rules", ""])
    for rule in pack.get("safety_rules", []):
        lines.append(f"- {rule}")
    lines.append("")

    lines.extend(["## Adult Setup Checklist", ""])
    for item in pack.get("adult_setup_checklist", []):
        lines.append(f"- [ ] {item}")
    for card_id in pack.get("target_power_card_ids", []):
        card = power_by_id.get(card_id, {})
        for step in card.get("activity_flow", {}).get("adult_setup", []):
            if isinstance(step, dict) and not step_uses_excluded_asset(step, card_id, exclusions):
                lines.append(f"- [ ] {card_id}: {step.get('instruction', '')}")
    lines.append("")

    lines.extend(["## Kit Pick List By Bin", ""])
    append_table(
        lines,
        [
            "Bin",
            "Compartment",
            "Kit",
            "Item",
            "Cards",
            "Basis",
            "Calc",
            "4 children",
            "5 children",
            "6 children",
            "Return check",
        ],
        [
            [
                row.get("storage", {}).get("bin_id"),
                row.get("storage", {}).get("compartment"),
                row.get("kit_code"),
                row.get("short_label"),
                row.get("power_card_ids"),
                row.get("quantity_basis"),
                row.get("quantity_formula"),
                row.get("quantity_by_child_count", {}).get("4"),
                row.get("quantity_by_child_count", {}).get("5"),
                row.get("quantity_by_child_count", {}).get("6"),
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
        ["Kit", "Item", "4 children", "5 children", "6 children", "Before", "After", "Count-back note"],
        [
            [
                row.get("kit_code"),
                row.get("short_label"),
                row.get("quantity_by_child_count", {}).get("4"),
                row.get("quantity_by_child_count", {}).get("5"),
                row.get("quantity_by_child_count", {}).get("6"),
                "",
                "",
                row.get("return_check"),
            ]
            for row in battery_rows
        ],
    )
    for item in pack.get("reset_count_back", {}).get("battery_count_back", []):
        if isinstance(item, dict) and item.get("note"):
            lines.append(f"- {item['note']}")
    lines.append("")

    lines.extend(["## Child-Facing Prompts", ""])
    append_table(
        lines,
        ["Card", "Prompt", "Starter question"],
        [
            [
                card_id,
                power_by_id.get(card_id, {}).get("activity_flow", {}).get("child_start_state", {}).get("prompt"),
                power_by_id.get(card_id, {}).get("activity_flow", {}).get("child_start_state", {}).get("starter_question"),
            ]
            for card_id in pack.get("target_power_card_ids", [])
        ],
    )

    lines.extend(["## Card Sequence", ""])
    for item in pack.get("card_sequence", []):
        if not isinstance(item, dict):
            continue
        card_id = item.get("power_card_id")
        card = power_by_id.get(card_id, {})
        lines.append(f"### {card_id} - {card.get('title', '')}")
        lines.append(f"- Purpose: {item.get('purpose', '-')}")
        lines.append(f"- Stop condition: {item.get('stop_condition', '-')}")
        lines.append(f"- Handoff cue: {item.get('handoff_cue', '-')}")
        lines.append("")

    lines.extend(["## r_pow_02 Safe-Circuit Diagram", ""])
    lines.append(f"![r_pow_02 safe LED circuit]({diagram_filename})")
    lines.append("")
    lines.append("- Diagram rule: battery pack, clip leads, and LED module only.")
    lines.append("- Adult check happens before the battery pack switch is turned on.")
    lines.append("- Do not use loose AA cells or the optional motor comparison load in this micro-pack.")
    lines.append("")

    lines.extend(["## Reset And Pack-Away Checklist", ""])
    for step in pack.get("reset_count_back", {}).get("pack_away_steps", []):
        lines.append(f"- [ ] {step}")
    for card_id in pack.get("target_power_card_ids", []):
        card = power_by_id.get(card_id, {})
        for step in card.get("activity_flow", {}).get("reset_and_pack", []):
            if isinstance(step, dict) and not step_uses_excluded_asset(step, card_id, exclusions):
                lines.append(f"- [ ] {card_id}: {step.get('instruction', '')}")
    lines.append("")

    lines.extend(["## What To Observe During The Pilot", ""])
    for note in pack.get("pilot_observation_focus", []):
        lines.append(f"- {note}")
    lines.append("")

    lines.extend(["## Deliberately Deferred", ""])
    append_table(
        lines,
        ["Card", "Reason"],
        [
            [item.get("power_card_id"), item.get("reason")]
            for item in pack.get("deferred_power_cards", [])
            if isinstance(item, dict)
        ],
    )

    if pack.get("asset_exclusions"):
        lines.extend(["## Asset Exclusions For This Micro-Pack", ""])
        append_table(
            lines,
            ["Card", "Asset", "Reason"],
            [
                [item.get("power_card_id"), item.get("asset_id"), item.get("reason")]
                for item in pack.get("asset_exclusions", [])
                if isinstance(item, dict)
            ],
        )

    return "\n".join(lines).rstrip() + "\n"


def write_micro_pack_outputs(source: dict[str, Any], output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for pack in source.get("pilot_micro_packs", []):
        if not isinstance(pack, dict):
            continue
        slug = slugify(str(pack.get("id", "pilot-micro-pack")))
        (output_dir / f"{slug}.md").write_text(render_micro_pack_markdown(source, pack), encoding="utf-8")
        if any(isinstance(ref, dict) and ref.get("power_card_id") == "r_pow_02" for ref in pack.get("diagram_refs", [])):
            (output_dir / r_pow_02_diagram_filename(pack)).write_text(
                render_r_pow_02_safe_circuit_svg(source),
                encoding="utf-8",
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    source = load_source(Path(args.source))
    write_micro_pack_outputs(source, Path(args.output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
