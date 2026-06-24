#!/usr/bin/env python3
"""Validate the canonical curriculum source and generated artefacts."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import generate_lesson_plans
import generate_pilot_micro_packs
import generate_pilot_run_cards


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_GENERATED_DIR = ROOT / "curriculum/generated"
DEFAULT_LEVEL_AUDIT_OUTPUT = ROOT / "reports/power-card-level-audit.md"
SCHEMA_PATH = ROOT / "curriculum/schema/curriculum.schema.json"

REQUIRED_TOP_LEVEL = {
    "meta",
    "levels",
    "skill_cards",
    "power_cards",
    "integration_cards",
    "invention_cards",
    "asset_inventory",
    "preload_profiles",
    "lesson_plan_profiles",
    "pilot_micro_packs",
    "red_team_cases",
    "audit_warnings",
}

POWER_FIELDS = {
    "id",
    "title",
    "i_can_statement",
    "primary_family",
    "level",
    "dependencies",
    "materials",
    "success_condition",
    "debug_prompts",
    "stretch_challenge",
    "possible_integrations",
    "supporting_families",
    "classification_rationale",
    "result_image",
    "result_alt",
}

INTEGRATION_FIELDS = {
    "id",
    "title",
    "families_combined",
    "required_power_cards",
    "challenge",
    "success_condition",
    "choice_points",
    "make_it_yours_prompts",
}

INVENTION_FIELDS = {
    "id",
    "theme",
    "open_ended_challenge",
    "possible_skill_families",
    "constraints",
    "reflection_prompts",
}

WEAK_BOUNDARY_WARNING_IDS = {
    "human_facing_design_boundaries",
    "metrics_overstate_certainty",
}

LEVEL_DIMENSION_FIELDS = {
    "adult_support",
    "child_independence",
    "kit_state",
    "coding_expectation",
    "physical_build_complexity",
    "debugging_evidence_expectation",
    "integration_readiness",
}

PILOT_KIT_FAMILIES = {"movement", "control_input", "sensing", "power", "structures"}
PILOT_KIT_LEVELS = {1, 2}
PREPARATION_STATES = {"blank", "preloaded", "loose", "prebuilt", "adult-prepared"}
QUANTITY_BASES = {"per_child", "per_pair", "per_table", "per_session", "demo_only"}
PROGRAMMING_STATES = {"blank", "preloaded_locked", "child_editable_template", "child_authored_allowed"}
SUPERVISION_LEVELS = {"standard", "direct", "adult_controlled", "demo_only"}
ACTIVITY_FLOW_STEP_SECTIONS = ("adult_setup", "build_steps", "test_steps", "debug_steps", "reset_and_pack")
ACTIVITY_FLOW_REQUIRED_SECTIONS = set(ACTIVITY_FLOW_STEP_SECTIONS) | {"child_start_state", "facilitator_notes"}
ACTIVITY_FLOW_ALLOWED_SECTIONS = ACTIVITY_FLOW_REQUIRED_SECTIONS | {"diagram_refs", "diagram_semantics"}
ACTIVITY_STEP_ACTORS = {"adult", "child", "pair", "table"}
ACTIVITY_STEP_KINDS = {"prepare", "observe", "sort", "connect", "assemble", "test", "debug", "reset"}
LEVEL_1_CHILD_DISALLOWED_STEP_KINDS = {"connect", "assemble"}
PROGRAMMING_EDIT_PATTERNS = [
    r"\b(write|edit|author|create|modify|change)\s+(code|a program|program|script|firmware)\b",
    r"\b(code|program|script|firmware)\s+from\s+scratch\b",
    r"\bflash\s+(the\s+)?(board|micro:bit|firmware)\b",
]
RESET_REQUIRED_CATEGORIES = {
    "power_source",
    "programmable_board",
    "programmable_board_accessory",
    "wire",
    "load",
}
DIAGRAM_PRIMARY_VIEWS = {"parts_layout", "sorting_grid", "safe_circuit", "mechanism", "structure_test"}
SAFETY_SENSITIVE_CATEGORIES = {
    "actuator",
    "load",
    "power_connector",
    "power_source",
    "programmable_board",
    "programmable_board_accessory",
    "wire",
}
RUN_CARD_SAFETY_METADATA_CATEGORIES = {
    "power_source",
    "programmable_board",
    "programmable_board_accessory",
    "wire",
    "load",
}
RUN_CARD_REQUIRED_HEADINGS = {
    "##### Kit Pick List",
    "##### Safety and Prep",
    "##### Preload Profile Notes",
    "##### Adult Setup",
    "##### Child Start State",
    "##### Build Steps",
    "##### Test Steps",
    "##### Debug Steps",
    "##### Reset and Pack-Away",
    "##### Facilitator Notes",
    "##### Diagram Semantics",
}
SESSION_LESSON_REQUIRED_SECTIONS = {
    "## Target Age And Support Assumptions",
    "## Learning Objectives",
    "## Linked Power Cards",
    "## Relevant Skill Cards And Families",
    "## Level Expectations And Coding Boundary",
    "## Preparation Checklist",
    "## Room And Table Setup",
    "## Kit List By Bin",
    "## Battery Count-Back Sheet",
    "## Safety Rules",
    "## Timing Plan And Facilitator Script",
    "## Child-Facing Prompts",
    "## Activity Sequence",
    "## Success And Evidence Criteria",
    "## Debug Prompts",
    "## Differentiation",
    "## Reset And Pack-Away Checklist",
    "## Assessment And Observation Notes",
    "## Follow-Up Recommendations",
    "## Deliberately Deferred Cards",
    "## Diagram Reference",
}
ELECTRICAL_LIMIT_ASSET_IDS = {
    "part_aa_battery_pack",
    "part_aa_cell",
    "part_battery_holder",
    "part_button_module",
    "part_coin_cell",
    "part_coin_cell_holder",
    "part_croc_clip_lead",
    "part_dc_motor",
    "part_distance_sensor_module",
    "part_joystick_module",
    "part_led_indicator_module",
    "part_led_module",
    "part_led_strip",
    "part_light_sensor_module",
    "part_micro_servo",
    "part_microbit_board",
    "part_microbit_breakout",
    "part_numeric_display_module",
    "part_potentiometer_module",
    "part_solenoid_sample",
    "part_switch_module",
    "part_tilt_sensor_module",
    "part_toggle_switch",
    "part_touch_sensor_module",
}

EXPECTED_CODING_BOUNDARY = {
    1: "No code.",
    2: "No child-authored code; preloaded or plug-and-play code is allowed.",
    3: "Adjust one parameter, setting, threshold, timing value, or mode in a known pattern.",
    4: "Guided adaptation of a known code or logic pattern.",
    5: "Coordinate multiple inputs, outputs, states, messages, or subsystems.",
    6: "Debug, optimise, compare, or justify trade-offs in code, logic, or physical behaviour.",
}

LEVEL_REVIEW_RULES = [
    {
        "id": "child_authored_code_boundary",
        "minimum_level": 3,
        "label": "child-authored code or program editing",
        "rationale": "Level 1 has no code and Level 2 allows only preloaded or plug-and-play code.",
        "patterns": [
            r"\b(write|edit|author|create|modify|change)\s+(code|a program|program|script)\b",
            r"\b(code|program|script)\s+from\s+scratch\b",
        ],
    },
    {
        "id": "adjust_one_variable_boundary",
        "minimum_level": 3,
        "label": "adjusting a setting, threshold, timing value, or mode",
        "rationale": "Level 3 is the first level where the child adjusts one variable in a known setup.",
        "patterns": [
            r"\b(adjust|tune|calibrate|debounce)\b",
            r"\b(change|set|map)\s+(a|an|the|one|second|different|chosen)?\s*(threshold|timing|parameter|setting|mode|range|zone|speed|mapping|command)\b",
            r"\b(threshold|timing|parameter|setting|mode|zones?)\b",
        ],
    },
    {
        "id": "guided_adaptation_boundary",
        "minimum_level": 4,
        "label": "adapting a known pattern to a new context",
        "rationale": "Level 4 is the first level where the child applies or adapts a known pattern in a new context.",
        "patterns": [
            r"\b(adapt|apply|transfer)\b",
            r"\b(new|different)\s+(context|setting|place|user|material|environment|challenge|build)\b",
            r"\bfit\s+(a\s+)?real\b",
        ],
    },
    {
        "id": "coordination_boundary",
        "minimum_level": 5,
        "label": "coordinating multiple elements or subsystems",
        "rationale": "Level 5 is the first level where multiple inputs, outputs, states, messages, or subsystems are coordinated.",
        "patterns": [
            r"\bcoordinate\b",
            r"\bcombine\b",
            r"\bmultiple\b",
            r"\bseveral\b",
            r"\btwo\s+(actuators|controls|inputs|sensors|senders|receivers|boards|servos|subsystems)\b",
            r"\bsubsystems?\b",
        ],
    },
    {
        "id": "improvement_tradeoff_boundary",
        "minimum_level": 6,
        "label": "debugging, optimisation, or trade-off justification",
        "rationale": "Level 6 is the first level where the child debugs, optimises, compares, or justifies trade-offs.",
        "patterns": [
            r"\bdebug\b",
            r"\bimprove\b",
            r"\boptimise\b",
            r"\boptimize\b",
            r"\btrade[- ]offs?\b",
            r"\bjustify\b",
            r"\bfailure\s+rate\b",
            r"\breliability\b",
        ],
    },
]

POWER_CARD_CORE_AUDIT_FIELDS = (
    "title",
    "i_can_statement",
    "success_condition",
    "debug_prompts",
)

POWER_CARD_STRETCH_AUDIT_FIELDS = ("stretch_challenge",)


def json_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        text = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    return text


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(json_text(path))
    except FileNotFoundError:
        errors.append(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: JSON parse error at line {exc.lineno}: {exc.msg}")
    return {}


def expected_browser_curriculum_payload(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "levels": source.get("levels", []),
        "families": [
            {key: value for key, value in family.items() if key not in {"icon_asset", "summary"}}
            for family in source.get("skill_cards", [])
            if isinstance(family, dict)
        ],
        "powerCards": source.get("power_cards", []),
        "integrationCards": source.get("integration_cards", []),
        "inventionCards": source.get("invention_cards", []),
        "assetInventory": source.get("asset_inventory", {}),
        "preloadProfiles": source.get("preload_profiles", []),
    }


def pilot_kit_cards(source: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        card
        for card in source.get("power_cards", [])
        if isinstance(card, dict)
        and card.get("primary_family") in PILOT_KIT_FAMILIES
        and card.get("level") in PILOT_KIT_LEVELS
    ]


def pilot_asset_detail(
    requirement: dict[str, Any],
    physical_assets_by_id: dict[str, dict[str, Any]],
    preload_profiles_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    asset = physical_assets_by_id.get(requirement.get("asset_id"), {})
    safety = asset.get("safety", {}) if isinstance(asset.get("safety"), dict) else {}
    stock = asset.get("stock", {}) if isinstance(asset.get("stock"), dict) else {}
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
        "storage": asset.get("storage", {}),
        "safety_flags": safety.get("hazards", []),
        "supervision_level": safety.get("supervision_level", ""),
        "age_floor": safety.get("age_floor"),
        "inspection_check": safety.get("inspection_check", ""),
        "return_check": safety.get("return_check", ""),
        "stock": {
            "reusable": stock.get("reusable"),
            "consumable": stock.get("consumable"),
            "reorder_unit": stock.get("reorder_unit", ""),
            "reorder_trigger": stock.get("reorder_trigger", ""),
        },
    }
    if detail["programming_state"] is None:
        detail.pop("programming_state")
    preload_profile_id = requirement.get("preload_profile_id")
    if preload_profile_id:
        preload_profile = preload_profiles_by_id.get(preload_profile_id, {})
        detail["preload_profile_id"] = preload_profile_id
        detail["preload_profile_label"] = preload_profile.get("label", "")
    return detail


def aggregate_pilot_assets(asset_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aggregated: dict[tuple[str, str, str, str, str], dict[str, Any]] = {}
    for row in asset_rows:
        key = (
            str(row.get("asset_id", "")),
            str(row.get("quantity_basis", "")),
            str(row.get("preparation_state", "")),
            str(row.get("preload_profile_id", "")),
            str(row.get("programming_state", "")),
        )
        if key not in aggregated:
            aggregated[key] = {
                "asset_id": row.get("asset_id"),
                "kit_code": row.get("kit_code", ""),
                "label": row.get("label", ""),
                "short_label": row.get("short_label", ""),
                "category": row.get("category", ""),
                "total_quantity": 0,
                "quantity_basis": row.get("quantity_basis"),
                "preparation_state": row.get("preparation_state"),
                "storage": row.get("storage", {}),
                "safety_flags": row.get("safety_flags", []),
                "supervision_level": row.get("supervision_level", ""),
                "age_floor": row.get("age_floor"),
                "inspection_check": row.get("inspection_check", ""),
                "return_check": row.get("return_check", ""),
                "stock": row.get("stock", {}),
                "used_by_power_cards": [],
            }
            if row.get("programming_state"):
                aggregated[key]["programming_state"] = row.get("programming_state")
            if row.get("preload_profile_id"):
                aggregated[key]["preload_profile_id"] = row.get("preload_profile_id")
                aggregated[key]["preload_profile_label"] = row.get("preload_profile_label", "")
        aggregated[key]["total_quantity"] += int(row.get("quantity") or 0)
        used_by = row.get("power_card_id")
        if used_by and used_by not in aggregated[key]["used_by_power_cards"]:
            aggregated[key]["used_by_power_cards"].append(used_by)
    return sorted(
        aggregated.values(),
        key=lambda item: (
            str(item.get("storage", {}).get("zone", "")),
            str(item.get("storage", {}).get("bin_id", "")),
            int(item.get("storage", {}).get("pack_order") or 0),
            str(item.get("kit_code", "")),
            str(item.get("asset_id", "")),
            str(item.get("quantity_basis", "")),
            str(item.get("preparation_state", "")),
            str(item.get("preload_profile_id", "")),
        ),
    )


def expected_pilot_kit_list(source: dict[str, Any]) -> dict[str, Any]:
    inventory = source.get("asset_inventory", {})
    physical_assets_by_id = {
        asset.get("id"): asset
        for asset in inventory.get("physical_assets", [])
        if isinstance(asset, dict)
    }
    preload_profiles_by_id = {
        profile.get("id"): profile
        for profile in inventory.get("programmable_preload_profiles", [])
        if isinstance(profile, dict)
    }
    families_by_id = {
        family.get("id"): family
        for family in source.get("skill_cards", [])
        if isinstance(family, dict)
    }

    by_power_card: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []
    family_rows: dict[str, list[dict[str, Any]]] = {}
    for card in pilot_kit_cards(source):
        assets = []
        for requirement in card.get("required_assets", []):
            if not isinstance(requirement, dict):
                continue
            detail = pilot_asset_detail(requirement, physical_assets_by_id, preload_profiles_by_id)
            assets.append(detail)
            aggregate_row = dict(detail)
            aggregate_row["power_card_id"] = card.get("id")
            aggregate_row["power_card_title"] = card.get("title")
            all_rows.append(aggregate_row)
            family_rows.setdefault(card.get("primary_family", ""), []).append(aggregate_row)
        by_power_card.append(
            {
                "power_card_id": card.get("id"),
                "title": card.get("title"),
                "skill_card_id": card.get("primary_family"),
                "level": card.get("level"),
                "assets": assets,
            }
        )

    by_skill_card = []
    for family_id in sorted(family_rows):
        family = families_by_id.get(family_id, {})
        family_cards = [card for card in by_power_card if card.get("skill_card_id") == family_id]
        by_skill_card.append(
            {
                "skill_card_id": family_id,
                "label": family.get("label") or family.get("name", ""),
                "power_card_ids": [card["power_card_id"] for card in family_cards],
                "assets": aggregate_pilot_assets(family_rows[family_id]),
            }
        )

    return {
        "pilot_scope": {
            "levels": sorted(PILOT_KIT_LEVELS),
            "skill_card_ids": sorted(PILOT_KIT_FAMILIES),
            "power_card_ids": [card["power_card_id"] for card in by_power_card],
        },
        "by_power_card": by_power_card,
        "by_skill_card": by_skill_card,
        "global_packing_by_bin": aggregate_pilot_assets(all_rows),
    }


def extract_window_json(path: Path, global_name: str, errors: list[str]) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
        prefix = f"window.{global_name} = "
        start = text.index(prefix) + len(prefix)
        payload = text[start:].strip()
        if payload.endswith(";"):
            payload = payload[:-1]
        return json.loads(payload)
    except FileNotFoundError:
        errors.append(f"Missing browser bundle: {path}")
    except ValueError:
        errors.append(f"{path}: missing {global_name} assignment")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: browser JSON parse error at line {exc.lineno}: {exc.msg}")
    return {}


def require_object(data: Any, name: str, errors: list[str]) -> bool:
    if not isinstance(data, dict):
        errors.append(f"{name}: must be an object")
        return False
    return True


def require_list(value: Any, name: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{name}: must be a list")
        return []
    return value


def missing_fields(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if field not in record)


def duplicate_ids(records: list[dict[str, Any]], label: str, errors: list[str]) -> set[str]:
    ids: set[str] = set()
    for record in records:
        record_id = record.get("id")
        if not record_id:
            errors.append(f"{label}: record missing id")
            continue
        if record_id in ids:
            errors.append(f"{label}: duplicate id {record_id}")
        ids.add(record_id)
    return ids


def validate_safety_profile(asset_id: str, asset: dict[str, Any], errors: list[str]) -> None:
    category = asset.get("category")
    is_sensitive = category in SAFETY_SENSITIVE_CATEGORIES or asset_id in ELECTRICAL_LIMIT_ASSET_IDS
    safety = asset.get("safety")
    if not isinstance(safety, dict):
        if is_sensitive:
            errors.append(f"asset_inventory.physical_assets: safety-sensitive asset {asset_id} missing safety object")
        return

    hazards = safety.get("hazards")
    if not isinstance(hazards, list):
        errors.append(f"asset_inventory.physical_assets: asset {asset_id} safety.hazards must be a list")
    elif is_sensitive and not hazards:
        errors.append(f"asset_inventory.physical_assets: safety-sensitive asset {asset_id} missing safety hazards")

    supervision_level = safety.get("supervision_level")
    if supervision_level not in SUPERVISION_LEVELS:
        errors.append(
            f"asset_inventory.physical_assets: asset {asset_id} has invalid supervision_level {supervision_level!r}"
        )

    age_floor = safety.get("age_floor")
    if not isinstance(age_floor, int) or age_floor < 0:
        errors.append(f"asset_inventory.physical_assets: asset {asset_id} missing non-negative safety.age_floor")

    for field in ("inspection_check", "return_check"):
        if not str(safety.get(field, "")).strip():
            errors.append(f"asset_inventory.physical_assets: asset {asset_id} missing safety.{field}")

    if category in {"actuator", "load", "power_source", "programmable_board"} and supervision_level == "standard":
        errors.append(
            f"asset_inventory.physical_assets: asset {asset_id} needs direct or adult-controlled supervision"
        )

    if "coin_cell" in asset_id and supervision_level != "adult_controlled":
        errors.append(f"asset_inventory.physical_assets: asset {asset_id} coin cells require adult_controlled supervision")

    if asset_id in ELECTRICAL_LIMIT_ASSET_IDS:
        limits = safety.get("electrical_limits")
        if not isinstance(limits, dict):
            errors.append(f"asset_inventory.physical_assets: asset {asset_id} missing safety.electrical_limits")
        else:
            max_voltage = limits.get("max_voltage_v")
            max_current = limits.get("max_current_ma")
            if not isinstance(max_voltage, (int, float)) or max_voltage <= 0:
                errors.append(
                    f"asset_inventory.physical_assets: asset {asset_id} electrical_limits missing positive max_voltage_v"
                )
            if not isinstance(max_current, int) or max_current <= 0:
                errors.append(
                    f"asset_inventory.physical_assets: asset {asset_id} electrical_limits missing positive max_current_ma"
                )
            if not str(limits.get("notes", "")).strip():
                errors.append(f"asset_inventory.physical_assets: asset {asset_id} electrical_limits missing notes")


def validate_top_level(source: dict[str, Any], errors: list[str]) -> None:
    for field in sorted(REQUIRED_TOP_LEVEL - set(source)):
        errors.append(f"source: missing top-level section {field}")
    schema_version = source.get("meta", {}).get("schema_version")
    if schema_version != "curriculum.v1":
        errors.append(f"source: expected meta.schema_version 'curriculum.v1', found {schema_version!r}")


def validate_schema_contract(source: dict[str, Any], errors: list[str], warnings: list[str]) -> dict[str, Any]:
    schema = load_json(SCHEMA_PATH, errors)
    strategy = {
        "schema_path": str(SCHEMA_PATH.relative_to(ROOT)),
        "mode": "custom_validator_with_schema_contract_check",
        "reason": (
            "The repository does not depend on a JSON Schema runtime; this validator parses the schema, "
            "checks its required top-level contract, and then applies stricter semantic rules that JSON "
            "Schema alone does not express."
        ),
    }
    if not isinstance(schema, dict):
        return strategy

    required = set(schema.get("required", []))
    if required != REQUIRED_TOP_LEVEL:
        errors.append(
            f"schema: top-level required fields {sorted(required)} do not match validator required fields {sorted(REQUIRED_TOP_LEVEL)}"
        )
    missing = sorted(required - set(source))
    if missing:
        errors.append(f"schema: source missing schema-required top-level fields {missing}")

    schema_version = (
        schema.get("properties", {})
        .get("meta", {})
        .get("properties", {})
        .get("schema_version", {})
        .get("const")
    )
    if schema_version != "curriculum.v1":
        errors.append(f"schema: expected meta.schema_version const 'curriculum.v1', found {schema_version!r}")

    power_card_properties = schema.get("$defs", {}).get("power_card", {}).get("properties", {})
    if "activity_flow" not in power_card_properties:
        errors.append("schema: power_card must define optional activity_flow property")
    missing_activity_defs = sorted(
        definition
        for definition in (
            "activity_flow",
            "activity_step",
            "child_start_state",
            "diagram_semantics",
            "diagram_node",
            "diagram_connection",
            "diagram_state",
        )
        if definition not in schema.get("$defs", {})
    )
    if missing_activity_defs:
        errors.append(f"schema: missing activity_flow-related definitions {missing_activity_defs}")

    warnings.append(
        "JSON schema contract parsed; custom semantic validation is used because no JSON Schema runtime is vendored."
    )
    return strategy


def validate_levels(source: dict[str, Any], errors: list[str]) -> set[int]:
    levels = require_list(source.get("levels"), "levels", errors)
    level_ids = set()
    for level in levels:
        if not isinstance(level, dict):
            errors.append("levels: each level must be an object")
            continue
        level_id = level.get("id")
        level_ids.add(level_id)
        for field in ("id", "name", "child_facing_summary", "facilitator_definition", "coding_expectation"):
            if not str(level.get(field, "")).strip():
                errors.append(f"levels: level {level_id!r} missing non-empty {field}")
        dimensions = level.get("dimensions")
        if not isinstance(dimensions, dict):
            errors.append(f"levels: level {level_id!r} missing dimensions object")
        else:
            missing_dimensions = sorted(LEVEL_DIMENSION_FIELDS - set(dimensions))
            if missing_dimensions:
                errors.append(f"levels: level {level_id!r} missing dimensions {missing_dimensions}")
            extra_dimensions = sorted(set(dimensions) - LEVEL_DIMENSION_FIELDS)
            if extra_dimensions:
                errors.append(f"levels: level {level_id!r} has unknown dimensions {extra_dimensions}")
            for dimension in sorted(LEVEL_DIMENSION_FIELDS):
                if not str(dimensions.get(dimension, "")).strip():
                    errors.append(f"levels: level {level_id!r} dimension {dimension} must be non-empty")
            if dimensions.get("coding_expectation") != level.get("coding_expectation"):
                errors.append(
                    f"levels: level {level_id!r} coding_expectation must match dimensions.coding_expectation"
                )
        expected_coding = EXPECTED_CODING_BOUNDARY.get(level_id)
        if expected_coding and level.get("coding_expectation") != expected_coding:
            errors.append(
                f"levels: level {level_id!r} coding_expectation {level.get('coding_expectation')!r} does not match required boundary {expected_coding!r}"
            )
    if level_ids != {1, 2, 3, 4, 5, 6}:
        errors.append(f"levels: expected ids [1, 2, 3, 4, 5, 6], found {sorted(level_ids)}")
    return {level_id for level_id in level_ids if isinstance(level_id, int)}


def validate_skill_cards(source: dict[str, Any], level_ids: set[int], errors: list[str]) -> set[str]:
    families = require_list(source.get("skill_cards"), "skill_cards", errors)
    family_ids = duplicate_ids([family for family in families if isinstance(family, dict)], "skill_cards", errors)
    if len(families) != 10:
        errors.append(f"skill_cards: expected 10 families, found {len(families)}")

    for family in families:
        if not isinstance(family, dict):
            errors.append("skill_cards: each family must be an object")
            continue
        family_id = family.get("id", "<missing-id>")
        for field in ("name", "label", "group", "suit", "primary_learning_problem", "icon_asset"):
            if not str(family.get(field, "")).strip():
                errors.append(f"skill_cards: family {family_id} missing non-empty {field}")
        levels = require_list(family.get("levels"), f"skill_cards: family {family_id} levels", errors)
        family_level_ids = {level.get("level") for level in levels if isinstance(level, dict)}
        if family_level_ids != level_ids:
            errors.append(
                f"skill_cards: family {family_id} levels should be {sorted(level_ids)}, found {sorted(family_level_ids)}"
            )
    return family_ids


def validate_power_cards(
    source: dict[str, Any],
    family_ids: set[str],
    level_ids: set[int],
    errors: list[str],
) -> dict[str, dict[str, Any]]:
    powers = require_list(source.get("power_cards"), "power_cards", errors)
    power_by_id: dict[str, dict[str, Any]] = {}
    if len(powers) != 120:
        errors.append(f"power_cards: expected 120 cards, found {len(powers)}")

    for power in powers:
        if not isinstance(power, dict):
            errors.append("power_cards: each card must be an object")
            continue
        power_id = power.get("id", "<missing-id>")
        for field in missing_fields(power, POWER_FIELDS):
            errors.append(f"power_cards: card {power_id} missing field {field}")
        if power_id in power_by_id:
            errors.append(f"power_cards: duplicate id {power_id}")
        power_by_id[power_id] = power

        primary_family = power.get("primary_family")
        if primary_family not in family_ids:
            errors.append(f"power_cards: card {power_id} references unknown primary family {primary_family!r}")
        if power.get("level") not in level_ids:
            errors.append(f"power_cards: card {power_id} has invalid level {power.get('level')!r}")

        for list_field in ("dependencies", "materials", "debug_prompts", "possible_integrations", "supporting_families"):
            if not isinstance(power.get(list_field), list):
                errors.append(f"power_cards: card {power_id} field {list_field} must be a list")

        supporting_families = power.get("supporting_families", [])
        for family_id in supporting_families if isinstance(supporting_families, list) else []:
            if family_id not in family_ids:
                errors.append(f"power_cards: card {power_id} references unknown supporting family {family_id!r}")
            if family_id == primary_family:
                errors.append(f"power_cards: card {power_id} repeats primary family in supporting_families")

        rationale = str(power.get("classification_rationale", "")).strip()
        if supporting_families and not rationale:
            errors.append(f"power_cards: card {power_id} has supporting_families but no classification_rationale")

    for power_id, power in power_by_id.items():
        for dependency_id in power.get("dependencies", []):
            dependency = power_by_id.get(dependency_id)
            if dependency is None:
                errors.append(f"power_cards: card {power_id} depends on unknown card {dependency_id}")
                continue
            if dependency.get("level", 0) > power.get("level", 0):
                errors.append(
                    f"power_cards: card {power_id} level {power.get('level')} depends upward on {dependency_id} level {dependency.get('level')}"
                )
            if dependency.get("primary_family") != power.get("primary_family"):
                supporting = power.get("supporting_families", [])
                if dependency.get("primary_family") not in supporting:
                    errors.append(
                        f"power_cards: card {power_id} has cross-family dependency {dependency_id} without supporting family {dependency.get('primary_family')}"
                    )
                if not str(power.get("classification_rationale", "")).strip():
                    errors.append(
                        f"power_cards: card {power_id} has cross-family dependency {dependency_id} but no classification_rationale"
                    )

    validate_dependency_cycles(power_by_id, errors)
    return power_by_id


def validate_dependency_cycles(power_by_id: dict[str, dict[str, Any]], errors: list[str]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(power_id: str) -> None:
        if power_id in visiting:
            start = stack.index(power_id)
            cycles.append(stack[start:] + [power_id])
            return
        if power_id in visited:
            return
        visiting.add(power_id)
        stack.append(power_id)
        for dependency_id in power_by_id[power_id].get("dependencies", []):
            if dependency_id in power_by_id:
                dfs(dependency_id)
        stack.pop()
        visiting.remove(power_id)
        visited.add(power_id)

    for power_id in power_by_id:
        dfs(power_id)

    for cycle in cycles:
        errors.append(f"power_cards: dependency cycle detected: {' -> '.join(cycle)}")
    return cycles


def step_has_programming_edit_language(text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in PROGRAMMING_EDIT_PATTERNS)


def activity_flow_steps(flow: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    steps: list[tuple[str, dict[str, Any]]] = []
    for section in ACTIVITY_FLOW_STEP_SECTIONS:
        section_steps = flow.get(section)
        if isinstance(section_steps, list):
            steps.extend((section, step) for step in section_steps if isinstance(step, dict))
    return steps


def validate_activity_diagram(
    power_id: str,
    power: dict[str, Any],
    flow: dict[str, Any],
    required_asset_ids: set[str],
    steps: list[tuple[str, dict[str, Any]]],
    errors: list[str],
) -> None:
    diagram_refs = flow.get("diagram_refs")
    if diagram_refs is not None:
        if not isinstance(diagram_refs, list):
            errors.append(f"power_cards: pilot card {power_id} activity_flow.diagram_refs must be a list")
        else:
            for index, ref in enumerate(diagram_refs, start=1):
                if not isinstance(ref, dict):
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.diagram_refs[{index}] must be an object"
                    )
                    continue
                for field in ("id", "label"):
                    if not str(ref.get(field, "")).strip():
                        errors.append(
                            f"power_cards: pilot card {power_id} activity_flow.diagram_refs[{index}] missing {field}"
                        )

    diagram = flow.get("diagram_semantics")
    if diagram is None:
        return
    if not isinstance(diagram, dict):
        errors.append(f"power_cards: pilot card {power_id} activity_flow.diagram_semantics must be an object")
        return

    primary_view = diagram.get("primary_view")
    if primary_view not in DIAGRAM_PRIMARY_VIEWS:
        errors.append(
            f"power_cards: pilot card {power_id} activity_flow.diagram_semantics has invalid primary_view {primary_view!r}"
        )

    nodes = diagram.get("nodes")
    node_ids: set[str] = set()
    if not isinstance(nodes, list) or not nodes:
        errors.append(f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes must be a non-empty list")
        nodes = []
    for index, node in enumerate(nodes, start=1):
        if not isinstance(node, dict):
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes[{index}] must be an object"
            )
            continue
        node_id = node.get("id")
        if not str(node_id or "").strip():
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes[{index}] missing id"
            )
        elif node_id in node_ids:
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes duplicate id {node_id}"
            )
        else:
            node_ids.add(str(node_id))
        asset_id = node.get("asset_id")
        if asset_id not in required_asset_ids:
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes[{index}] asset_id {asset_id!r} is not in required_assets"
            )
        for field in ("role", "label"):
            if not str(node.get(field, "")).strip():
                errors.append(
                    f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.nodes[{index}] missing {field}"
                )

    connections = diagram.get("connections")
    if not isinstance(connections, list):
        errors.append(f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.connections must be a list")
        connections = []
    for index, connection in enumerate(connections, start=1):
        if not isinstance(connection, dict):
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.connections[{index}] must be an object"
            )
            continue
        for endpoint_field in ("from", "to"):
            endpoint = connection.get(endpoint_field)
            endpoint_node_id = str(endpoint or "").split(".", 1)[0]
            if endpoint_node_id not in node_ids:
                errors.append(
                    f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.connections[{index}] {endpoint_field} endpoint {endpoint!r} references unknown node"
                )
        if not str(connection.get("kind", "")).strip():
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.connections[{index}] missing kind"
            )
        if power.get("level") == 1 and connection.get("kind") != "conceptual":
            errors.append(
                f"power_cards: level 1 card {power_id} has non-conceptual diagram connection {connection.get('kind')!r}"
            )

    states = diagram.get("states")
    if states is not None:
        if not isinstance(states, list):
            errors.append(f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.states must be a list")
        else:
            for index, state in enumerate(states, start=1):
                if not isinstance(state, dict):
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.states[{index}] must be an object"
                    )
                    continue
                for field in ("id", "trigger", "expected_change"):
                    if not str(state.get(field, "")).strip():
                        errors.append(
                            f"power_cards: pilot card {power_id} activity_flow.diagram_semantics.states[{index}] missing {field}"
                        )

    for section, step in steps:
        diagram_node_ids = step.get("diagram_node_ids")
        if diagram_node_ids is None:
            continue
        if not isinstance(diagram_node_ids, list):
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow.{section}.{step.get('id', '<missing-id>')} diagram_node_ids must be a list"
            )
            continue
        for node_id in diagram_node_ids:
            if node_id not in node_ids:
                errors.append(
                    f"power_cards: pilot card {power_id} activity_flow.{section}.{step.get('id', '<missing-id>')} references unknown diagram node {node_id}"
                )


def validate_activity_flows(
    source: dict[str, Any],
    power_by_id: dict[str, dict[str, Any]],
    physical_assets_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    pilot_card_ids = {card.get("id") for card in pilot_kit_cards(source)}
    for power_id, power in power_by_id.items():
        in_pilot_scope = power_id in pilot_card_ids
        flow = power.get("activity_flow")
        if in_pilot_scope and not isinstance(flow, dict):
            errors.append(f"power_cards: pilot card {power_id} missing activity_flow object")
            continue
        if not in_pilot_scope and flow is not None:
            errors.append(f"power_cards: card {power_id} has activity_flow outside the current pilot scope")
            continue
        if flow is None:
            continue
        if not isinstance(flow, dict):
            errors.append(f"power_cards: card {power_id} activity_flow must be an object")
            continue

        missing_sections = sorted(ACTIVITY_FLOW_REQUIRED_SECTIONS - set(flow))
        if missing_sections:
            errors.append(f"power_cards: pilot card {power_id} activity_flow missing sections {missing_sections}")
        unknown_sections = sorted(set(flow) - ACTIVITY_FLOW_ALLOWED_SECTIONS)
        if unknown_sections:
            errors.append(f"power_cards: pilot card {power_id} activity_flow has unknown sections {unknown_sections}")
        if "diagram_refs" not in flow and "diagram_semantics" not in flow:
            errors.append(
                f"power_cards: pilot card {power_id} activity_flow must include diagram_refs or diagram_semantics"
            )

        required_assets = power.get("required_assets", [])
        requirement_by_asset = {
            requirement.get("asset_id"): requirement
            for requirement in required_assets
            if isinstance(requirement, dict) and requirement.get("asset_id")
        }
        required_asset_ids = set(requirement_by_asset)

        child_start = flow.get("child_start_state")
        if not isinstance(child_start, dict):
            errors.append(f"power_cards: pilot card {power_id} activity_flow.child_start_state must be an object")
        else:
            for field in ("prompt", "starter_question"):
                if not str(child_start.get(field, "")).strip():
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.child_start_state missing {field}"
                    )
            visible_asset_ids = child_start.get("visible_asset_ids")
            if not isinstance(visible_asset_ids, list):
                errors.append(
                    f"power_cards: pilot card {power_id} activity_flow.child_start_state.visible_asset_ids must be a list"
                )
            else:
                for asset_id in visible_asset_ids:
                    if asset_id not in required_asset_ids:
                        errors.append(
                            f"power_cards: pilot card {power_id} child_start_state visible asset {asset_id!r} is not in required_assets"
                        )
                    if requirement_by_asset.get(asset_id, {}).get("quantity_basis") == "demo_only":
                        errors.append(
                            f"power_cards: pilot card {power_id} child_start_state exposes demo_only asset {asset_id!r}"
                        )

        facilitator_notes = flow.get("facilitator_notes")
        if not isinstance(facilitator_notes, list) or not facilitator_notes:
            errors.append(f"power_cards: pilot card {power_id} activity_flow.facilitator_notes must be a non-empty list")
        elif any(not str(note).strip() for note in facilitator_notes):
            errors.append(f"power_cards: pilot card {power_id} activity_flow.facilitator_notes must be non-empty strings")

        steps = activity_flow_steps(flow)
        step_ids: set[str] = set()
        all_safety_focus: set[str] = set()
        reset_asset_ids: set[str] = set()
        for section in ACTIVITY_FLOW_STEP_SECTIONS:
            section_steps = flow.get(section)
            if not isinstance(section_steps, list) or not section_steps:
                errors.append(f"power_cards: pilot card {power_id} activity_flow.{section} must be a non-empty list")
                continue
            for index, step in enumerate(section_steps, start=1):
                if not isinstance(step, dict):
                    errors.append(f"power_cards: pilot card {power_id} activity_flow.{section}[{index}] must be an object")
                    continue
                step_id = step.get("id")
                if not str(step_id or "").strip():
                    errors.append(f"power_cards: pilot card {power_id} activity_flow.{section}[{index}] missing id")
                elif step_id in step_ids:
                    errors.append(f"power_cards: pilot card {power_id} activity_flow duplicate step id {step_id}")
                else:
                    step_ids.add(str(step_id))

                actor = step.get("actor")
                kind = step.get("kind")
                instruction = str(step.get("instruction", "")).strip()
                if actor not in ACTIVITY_STEP_ACTORS:
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} has invalid actor {actor!r}"
                    )
                if kind not in ACTIVITY_STEP_KINDS:
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} has invalid kind {kind!r}"
                    )
                if not instruction:
                    errors.append(f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} missing instruction")

                if (
                    power.get("level") == 1
                    and actor in {"child", "pair", "table"}
                    and kind in LEVEL_1_CHILD_DISALLOWED_STEP_KINDS
                ):
                    errors.append(
                        f"power_cards: level 1 card {power_id} has child-facing {kind} step {step_id}; Level 1 must stay observation/sorting focused"
                    )
                if actor in {"child", "pair", "table"} and step_has_programming_edit_language(instruction):
                    errors.append(
                        f"power_cards: card {power_id} activity_flow.{section}.{step_id} uses child-facing programming/editing language"
                    )

                asset_ids = step.get("asset_ids", [])
                if asset_ids is None:
                    asset_ids = []
                if not isinstance(asset_ids, list):
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} asset_ids must be a list"
                    )
                    asset_ids = []
                for asset_id in asset_ids:
                    if asset_id not in required_asset_ids:
                        errors.append(
                            f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} references asset {asset_id!r} outside required_assets"
                        )
                    if requirement_by_asset.get(asset_id, {}).get("quantity_basis") == "demo_only":
                        allowed_demo_step = actor == "adult" or (actor == "child" and kind == "observe")
                        if not allowed_demo_step:
                            errors.append(
                                f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} uses demo_only asset {asset_id!r} outside adult or child observation step"
                            )
                if section == "reset_and_pack":
                    reset_asset_ids.update(asset_ids)

                safety_focus = step.get("safety_focus", [])
                if safety_focus is None:
                    safety_focus = []
                if not isinstance(safety_focus, list):
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow.{section}.{step_id} safety_focus must be a list"
                    )
                    safety_focus = []
                all_safety_focus.update(str(item) for item in safety_focus if str(item).strip())

        setup_text = " ".join(
            str(step.get("instruction", ""))
            for step in flow.get("adult_setup", [])
            if isinstance(step, dict)
        )
        for asset_id, requirement in requirement_by_asset.items():
            preload_profile_id = requirement.get("preload_profile_id")
            if requirement.get("preparation_state") == "preloaded":
                if not preload_profile_id:
                    errors.append(f"power_cards: pilot card {power_id} activity_flow preloaded asset {asset_id} has no profile")
                elif preload_profile_id not in setup_text:
                    errors.append(
                        f"power_cards: pilot card {power_id} adult_setup must name preload profile {preload_profile_id}"
                    )

            asset = physical_assets_by_id.get(asset_id, {})
            safety = asset.get("safety", {}) if isinstance(asset.get("safety"), dict) else {}
            hazards = set(safety.get("hazards", [])) if isinstance(safety.get("hazards"), list) else set()
            supervision_level = safety.get("supervision_level")
            if supervision_level in {"direct", "adult_controlled", "demo_only"} and hazards:
                if not hazards.intersection(all_safety_focus):
                    errors.append(
                        f"power_cards: pilot card {power_id} activity_flow lacks safety_focus matching hazards for supervised asset {asset_id}"
                    )

            reset_required = (
                requirement.get("quantity_basis") == "demo_only"
                or supervision_level in {"adult_controlled", "demo_only"}
                or asset.get("category") in RESET_REQUIRED_CATEGORIES
            )
            if reset_required and asset_id not in reset_asset_ids:
                errors.append(
                    f"power_cards: pilot card {power_id} reset_and_pack must mention asset {asset_id}"
                )

        validate_activity_diagram(power_id, power, flow, required_asset_ids, steps, errors)


def iter_card_field_text(card: dict[str, Any], fields: tuple[str, ...]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in fields:
        value = card.get(field)
        if isinstance(value, list):
            values.extend((field, str(item)) for item in value if str(item).strip())
        elif str(value or "").strip():
            values.append((field, str(value)))
    return values


def find_rule_match(
    card: dict[str, Any],
    rule: dict[str, Any],
    fields: tuple[str, ...],
) -> tuple[str, str] | None:
    for field, text in iter_card_field_text(card, fields):
        for pattern in rule["patterns"]:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return field, text
    return None


def audit_power_card_levels(power_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for power_id in sorted(power_by_id):
        card = power_by_id[power_id]
        current_level = card.get("level")
        if not isinstance(current_level, int):
            continue
        for rule in LEVEL_REVIEW_RULES:
            minimum_level = int(rule["minimum_level"])
            if current_level >= minimum_level:
                continue
            match = find_rule_match(card, rule, POWER_CARD_CORE_AUDIT_FIELDS)
            scope = "core"
            if match is None:
                match = find_rule_match(card, rule, POWER_CARD_STRETCH_AUDIT_FIELDS)
                scope = "stretch"
            if match is None:
                continue
            field, evidence = match
            items.append(
                {
                    "card_id": power_id,
                    "title": card.get("title", ""),
                    "primary_family": card.get("primary_family", ""),
                    "current_level": current_level,
                    "suggested_minimum_level": minimum_level,
                    "rule_id": rule["id"],
                    "rule_label": rule["label"],
                    "scope": scope,
                    "field": field,
                    "evidence": evidence,
                    "rationale": rule["rationale"],
                }
            )
    return {
        "rules": [
            {
                "id": rule["id"],
                "minimum_level": rule["minimum_level"],
                "label": rule["label"],
                "rationale": rule["rationale"],
            }
            for rule in LEVEL_REVIEW_RULES
        ],
        "items": items,
        "cards_needing_review": sorted({item["card_id"] for item in items}),
    }


def add_level_audit_warnings(level_audit: dict[str, Any], warnings: list[str]) -> None:
    items = level_audit.get("items", [])
    cards = level_audit.get("cards_needing_review", [])
    if not items:
        warnings.append("level_audit: no Power Cards matched current level-exceedance heuristics.")
        return
    warnings.append(
        f"level_audit: {len(cards)} Power Cards need human level-boundary review; see reports/power-card-level-audit.md."
    )
    for item in items:
        warnings.append(
            "level_audit: "
            f"{item['card_id']} level {item['current_level']} may exceed its level via {item['rule_id']} "
            f"(suggested minimum level {item['suggested_minimum_level']}, {item['scope']} field {item['field']})."
        )


def markdown_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def write_level_audit_report(path: Path, level_audit: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    items = level_audit.get("items", [])
    cards = level_audit.get("cards_needing_review", [])
    lines = [
        "<!-- GENERATED FILE - DO NOT EDIT BY HAND.",
        "Source: curriculum/source/curriculum.v1.json",
        "Rebuild: python3 tools/validate_curriculum.py --source curriculum/source/curriculum.v1.json --curriculum-dir curriculum/generated --output reports/validation-results.json",
        "Status: heuristic review aid; warnings require human judgement before changing card levels. -->",
        "",
        "# Power Card Level Audit",
        "",
        f"- Cards needing human review: {len(cards)}",
        f"- Review items: {len(items)}",
        "",
        "This report flags cards whose wording appears to exceed the current level model. It does not prove the card is wrong; it identifies places for human review.",
        "",
        "## Rules",
        "",
        "| Rule | First Allowed Level | Reason |",
        "| --- | ---: | --- |",
    ]
    for rule in level_audit.get("rules", []):
        lines.append(
            f"| {markdown_escape(rule['label'])} | {rule['minimum_level']} | {markdown_escape(rule['rationale'])} |"
        )
    lines.extend(["", "## Review Items", ""])
    if not items:
        lines.append("No Power Cards matched the current level-exceedance heuristics.")
    else:
        lines.extend(
            [
                "| Card | Current Level | Suggested Minimum | Rule | Scope | Field | Evidence |",
                "| --- | ---: | ---: | --- | --- | --- | --- |",
            ]
        )
        for item in items:
            lines.append(
                "| "
                f"{markdown_escape(item['card_id'])} - {markdown_escape(item['title'])} | "
                f"{item['current_level']} | "
                f"{item['suggested_minimum_level']} | "
                f"{markdown_escape(item['rule_label'])} | "
                f"{markdown_escape(item['scope'])} | "
                f"{markdown_escape(item['field'])} | "
                f"{markdown_escape(item['evidence'])} |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_integrations(
    source: dict[str, Any],
    family_ids: set[str],
    power_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    integrations = require_list(source.get("integration_cards"), "integration_cards", errors)
    if len(integrations) != 30:
        errors.append(f"integration_cards: expected 30 cards, found {len(integrations)}")
    duplicate_ids([card for card in integrations if isinstance(card, dict)], "integration_cards", errors)

    for integration in integrations:
        if not isinstance(integration, dict):
            errors.append("integration_cards: each card must be an object")
            continue
        integration_id = integration.get("id", "<missing-id>")
        for field in missing_fields(integration, INTEGRATION_FIELDS):
            errors.append(f"integration_cards: card {integration_id} missing field {field}")

        families_combined = integration.get("families_combined", [])
        required_power_cards = integration.get("required_power_cards", [])
        if not isinstance(families_combined, list) or len(set(families_combined)) < 2:
            errors.append(f"integration_cards: card {integration_id} must combine at least two families")
            families_combined = []
        if not isinstance(required_power_cards, list):
            errors.append(f"integration_cards: card {integration_id} required_power_cards must be a list")
            required_power_cards = []

        for family_id in families_combined:
            if family_id not in family_ids:
                errors.append(f"integration_cards: card {integration_id} references unknown family {family_id!r}")

        required_families = set()
        for power_id in required_power_cards:
            power = power_by_id.get(power_id)
            if not power:
                errors.append(f"integration_cards: card {integration_id} requires unknown power card {power_id}")
                continue
            required_families.add(power.get("primary_family"))

        if len(required_families) < 2:
            errors.append(f"integration_cards: card {integration_id} required cards cover fewer than two families")
        if set(families_combined) != required_families:
            errors.append(
                f"integration_cards: card {integration_id} families_combined {sorted(families_combined)} does not match required card families {sorted(required_families)}"
            )


def validate_inventions(source: dict[str, Any], family_ids: set[str], errors: list[str]) -> None:
    inventions = require_list(source.get("invention_cards"), "invention_cards", errors)
    if len(inventions) != 15:
        errors.append(f"invention_cards: expected 15 cards, found {len(inventions)}")
    duplicate_ids([card for card in inventions if isinstance(card, dict)], "invention_cards", errors)

    for invention in inventions:
        if not isinstance(invention, dict):
            errors.append("invention_cards: each card must be an object")
            continue
        invention_id = invention.get("id", "<missing-id>")
        for field in missing_fields(invention, INVENTION_FIELDS):
            errors.append(f"invention_cards: card {invention_id} missing field {field}")
        if "required_power_cards" in invention or "families_combined" in invention:
            errors.append(f"invention_cards: card {invention_id} should not use fixed integration fields")
        possible_families = invention.get("possible_skill_families", [])
        if not isinstance(possible_families, list) or not possible_families:
            errors.append(f"invention_cards: card {invention_id} must list possible skill families")
            continue
        for family_id in possible_families:
            if family_id not in family_ids:
                errors.append(f"invention_cards: card {invention_id} references unknown family {family_id!r}")


def validate_assets(
    source: dict[str, Any],
    power_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    inventory = source.get("asset_inventory", {})
    if not require_object(inventory, "asset_inventory", errors):
        return
    assets = require_list(inventory.get("assets"), "asset_inventory.assets", errors)
    asset_ids = duplicate_ids([asset for asset in assets if isinstance(asset, dict)], "asset_inventory.assets", errors)
    assets_by_id = {asset.get("id"): asset for asset in assets if isinstance(asset, dict)}

    for asset in assets:
        if not isinstance(asset, dict):
            errors.append("asset_inventory.assets: each asset must be an object")
            continue
        asset_id = asset.get("id", "<missing-id>")
        path = asset.get("path")
        if not path:
            errors.append(f"asset_inventory.assets: asset {asset_id} missing path")
            continue
        if not (ROOT / path).exists():
            errors.append(f"asset_inventory.assets: asset {asset_id} path does not exist: {path}")

    physical_assets = require_list(inventory.get("physical_assets"), "asset_inventory.physical_assets", errors)
    physical_asset_ids = duplicate_ids(
        [asset for asset in physical_assets if isinstance(asset, dict)],
        "asset_inventory.physical_assets",
        errors,
    )
    kit_codes = [
        asset.get("kit_code")
        for asset in physical_assets
        if isinstance(asset, dict) and str(asset.get("kit_code", "")).strip()
    ]
    for kit_code, count in Counter(kit_codes).items():
        if count > 1:
            errors.append(f"asset_inventory.physical_assets: duplicate kit_code {kit_code}")
    physical_assets_by_id = {asset.get("id"): asset for asset in physical_assets if isinstance(asset, dict)}
    for asset in physical_assets:
        if not isinstance(asset, dict):
            errors.append("asset_inventory.physical_assets: each asset must be an object")
            continue
        asset_id = asset.get("id", "<missing-id>")
        for field in ("kit_code", "label", "category"):
            if not str(asset.get(field, "")).strip():
                errors.append(f"asset_inventory.physical_assets: asset {asset_id} missing non-empty {field}")
        if "short_label" in asset and not str(asset.get("short_label", "")).strip():
            errors.append(f"asset_inventory.physical_assets: asset {asset_id} has empty short_label")
        state = asset.get("default_preparation_state")
        if state not in PREPARATION_STATES:
            errors.append(
                f"asset_inventory.physical_assets: asset {asset_id} has invalid default_preparation_state {state!r}"
            )
        storage = asset.get("storage")
        if not isinstance(storage, dict):
            errors.append(f"asset_inventory.physical_assets: asset {asset_id} missing storage object")
        else:
            for field in ("zone", "bin_id", "bin_label", "compartment", "return_location"):
                if not str(storage.get(field, "")).strip():
                    errors.append(f"asset_inventory.physical_assets: asset {asset_id} storage missing {field}")
            if not isinstance(storage.get("pack_order"), int) or storage.get("pack_order") < 1:
                errors.append(f"asset_inventory.physical_assets: asset {asset_id} storage missing positive pack_order")
        if asset.get("category") == "programmable_board":
            programmable = asset.get("programmable")
            if not isinstance(programmable, dict):
                errors.append(f"asset_inventory.physical_assets: programmable board {asset_id} missing programmable object")
            else:
                supported_states = programmable.get("supported_states")
                if not isinstance(supported_states, list) or not set(supported_states).issubset(PROGRAMMING_STATES):
                    errors.append(
                        f"asset_inventory.physical_assets: programmable board {asset_id} has invalid supported_states"
                    )
                default_state = programmable.get("default_state")
                if default_state not in PROGRAMMING_STATES:
                    errors.append(
                        f"asset_inventory.physical_assets: programmable board {asset_id} has invalid default_state {default_state!r}"
                    )
        stock = asset.get("stock")
        if isinstance(stock, dict):
            if not isinstance(stock.get("reusable"), bool) or not isinstance(stock.get("consumable"), bool):
                errors.append(f"asset_inventory.physical_assets: asset {asset_id} stock reusable/consumable must be booleans")
            for field in ("reorder_unit", "reorder_trigger"):
                if not str(stock.get(field, "")).strip():
                    errors.append(f"asset_inventory.physical_assets: asset {asset_id} stock missing {field}")
        validate_safety_profile(asset_id, asset, errors)

    programmable_preload_profiles = require_list(
        inventory.get("programmable_preload_profiles"),
        "asset_inventory.programmable_preload_profiles",
        errors,
    )
    preload_profile_ids = duplicate_ids(
        [profile for profile in programmable_preload_profiles if isinstance(profile, dict)],
        "asset_inventory.programmable_preload_profiles",
        errors,
    )
    preload_profiles_by_id = {
        profile.get("id"): profile for profile in programmable_preload_profiles if isinstance(profile, dict)
    }
    for profile in programmable_preload_profiles:
        if not isinstance(profile, dict):
            errors.append("asset_inventory.programmable_preload_profiles: each profile must be an object")
            continue
        profile_id = profile.get("id", "<missing-id>")
        for field in ("label", "description", "adult_preparation_notes"):
            if not str(profile.get(field, "")).strip():
                errors.append(
                    f"asset_inventory.programmable_preload_profiles: profile {profile_id} missing non-empty {field}"
                )
        board_asset_id = profile.get("board_asset_id")
        if board_asset_id not in physical_asset_ids:
            errors.append(
                f"asset_inventory.programmable_preload_profiles: profile {profile_id} references unknown board asset {board_asset_id}"
            )
        elif physical_assets_by_id.get(board_asset_id, {}).get("category") != "programmable_board":
            errors.append(
                f"asset_inventory.programmable_preload_profiles: profile {profile_id} board asset {board_asset_id} is not a programmable_board"
            )
        programming_state = profile.get("programming_state")
        if programming_state not in PROGRAMMING_STATES:
            errors.append(
                f"asset_inventory.programmable_preload_profiles: profile {profile_id} has invalid programming_state {programming_state!r}"
            )
        if not str(profile.get("board_delivery_state", "")).strip():
            errors.append(
                f"asset_inventory.programmable_preload_profiles: profile {profile_id} missing board_delivery_state"
            )
        if not isinstance(profile.get("child_editable"), bool):
            errors.append(f"asset_inventory.programmable_preload_profiles: profile {profile_id} missing child_editable boolean")
        if not isinstance(profile.get("blank_board_compatible"), bool):
            errors.append(
                f"asset_inventory.programmable_preload_profiles: profile {profile_id} missing blank_board_compatible boolean"
            )
        if programming_state == "preloaded_locked":
            if profile.get("child_editable") is not False:
                errors.append(
                    f"asset_inventory.programmable_preload_profiles: profile {profile_id} preloaded_locked must not be child_editable"
                )
            if profile.get("blank_board_compatible") is not False:
                errors.append(
                    f"asset_inventory.programmable_preload_profiles: profile {profile_id} preloaded_locked must not be blank_board_compatible"
                )

    result_asset_cards = {
        asset.get("card_id")
        for asset in assets
        if isinstance(asset, dict) and asset.get("category") == "power_card_result"
    }
    for power_id, power in power_by_id.items():
        result_image = power.get("result_image")
        if result_image and not (ROOT / result_image).exists():
            errors.append(f"power_cards: card {power_id} result_image path does not exist: {result_image}")
        if power_id not in result_asset_cards:
            errors.append(f"asset_inventory: missing power_card_result asset for card {power_id}")

    assignments = require_list(inventory.get("scene_assignments"), "asset_inventory.scene_assignments", errors)
    assignments_by_card = {assignment.get("card_id"): assignment for assignment in assignments if isinstance(assignment, dict)}
    for power_id in power_by_id:
        assignment = assignments_by_card.get(power_id)
        if not assignment:
            errors.append(f"asset_inventory.scene_assignments: missing scene assignment for card {power_id}")
            continue
        if not assignment.get("template"):
            errors.append(f"asset_inventory.scene_assignments: card {power_id} missing template")

    pilot_card_ids = {card.get("id") for card in pilot_kit_cards(source)}
    for power_id, power in power_by_id.items():
        required_assets = power.get("required_assets")
        in_pilot_scope = power_id in pilot_card_ids
        if in_pilot_scope and not isinstance(required_assets, list):
            errors.append(f"power_cards: pilot card {power_id} missing required_assets list")
            continue
        if not in_pilot_scope and required_assets:
            errors.append(f"power_cards: card {power_id} has required_assets outside the current pilot scope")
        if required_assets is None:
            continue
        if not isinstance(required_assets, list):
            errors.append(f"power_cards: card {power_id} required_assets must be a list")
            continue
        if in_pilot_scope and not required_assets:
            errors.append(f"power_cards: pilot card {power_id} required_assets must not be empty")
        for index, requirement in enumerate(required_assets, start=1):
            if not isinstance(requirement, dict):
                errors.append(f"power_cards: card {power_id} required_assets[{index}] must be an object")
                continue
            asset_id = requirement.get("asset_id")
            if asset_id not in physical_asset_ids:
                errors.append(f"power_cards: card {power_id} required_assets[{index}] references unknown asset {asset_id}")
            quantity = requirement.get("quantity")
            if not isinstance(quantity, int) or quantity < 1:
                errors.append(f"power_cards: card {power_id} required_assets[{index}] missing positive integer quantity")
            quantity_basis = requirement.get("quantity_basis")
            if quantity_basis not in QUANTITY_BASES:
                errors.append(
                    f"power_cards: card {power_id} required_assets[{index}] has invalid quantity_basis {quantity_basis!r}"
                )
            state = requirement.get("preparation_state")
            if state not in PREPARATION_STATES:
                errors.append(
                    f"power_cards: card {power_id} required_assets[{index}] has invalid preparation_state {state!r}"
                )
            if not str(requirement.get("preparation_notes", "")).strip():
                errors.append(f"power_cards: card {power_id} required_assets[{index}] missing preparation_notes")
            programming_state = requirement.get("programming_state")
            asset = physical_assets_by_id.get(asset_id, {})
            if programming_state is not None:
                if programming_state not in PROGRAMMING_STATES:
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] has invalid programming_state {programming_state!r}"
                    )
                if asset.get("category") != "programmable_board":
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] sets programming_state on non-programmable asset {asset_id}"
                    )
            preload_profile_id = requirement.get("preload_profile_id")
            if preload_profile_id:
                profile = preload_profiles_by_id.get(preload_profile_id)
                if profile is None:
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] references unknown preload profile {preload_profile_id}"
                    )
                elif profile.get("board_asset_id") != asset_id:
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] preload profile {preload_profile_id} is for {profile.get('board_asset_id')}, not {asset_id}"
                    )
                elif state != "preloaded":
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] uses preload profile but preparation_state is {state!r}"
                    )
                elif programming_state != profile.get("programming_state"):
                    errors.append(
                        f"power_cards: card {power_id} required_assets[{index}] programming_state must match preload profile {preload_profile_id}"
                    )
            elif state == "preloaded":
                errors.append(
                    f"power_cards: card {power_id} required_assets[{index}] is preloaded but has no preload_profile_id"
                )
            if state == "preloaded" and programming_state != "preloaded_locked":
                errors.append(
                    f"power_cards: card {power_id} required_assets[{index}] preloaded assets must use programming_state 'preloaded_locked'"
                )

    validate_activity_flows(source, power_by_id, physical_assets_by_id, errors)

    known_assets = set(asset_ids)
    for profile in require_list(source.get("preload_profiles"), "preload_profiles", errors):
        if not isinstance(profile, dict):
            errors.append("preload_profiles: each profile must be an object")
            continue
        profile_id = profile.get("id", "<missing-id>")
        for asset_id in profile.get("asset_ids", []):
            if asset_id not in known_assets:
                errors.append(f"preload_profiles: profile {profile_id} references unknown asset {asset_id}")
        if profile_id == "homepage":
            heavy = [
                asset_id
                for asset_id in profile.get("asset_ids", [])
                if assets_by_id.get(asset_id, {}).get("category") == "power_card_result"
            ]
            if heavy:
                errors.append(f"preload_profiles: homepage should not include power card result assets: {heavy}")


def validate_profiles_and_audit(source: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    lesson_profiles = require_list(source.get("lesson_plan_profiles"), "lesson_plan_profiles", errors)
    duplicate_ids([profile for profile in lesson_profiles if isinstance(profile, dict)], "lesson_plan_profiles", errors)
    profiles_by_id = {}
    for profile in lesson_profiles:
        if not isinstance(profile, dict):
            errors.append("lesson_plan_profiles: each profile must be an object")
            continue
        profiles_by_id[profile.get("id")] = profile
        for field in ("id", "name", "output_dir", "source_card_type"):
            if not str(profile.get(field, "")).strip():
                errors.append(f"lesson_plan_profiles: profile {profile.get('id', '<missing-id>')} missing non-empty {field}")

    session_profile = profiles_by_id.get("facilitator_session_first_session")
    if not isinstance(session_profile, dict):
        errors.append("lesson_plan_profiles: missing facilitator_session_first_session profile")
    else:
        if session_profile.get("output_dir") != "curriculum/generated/session-lesson-plans":
            errors.append("lesson_plan_profiles: facilitator_session_first_session output_dir must be curriculum/generated/session-lesson-plans")
        if session_profile.get("source_card_type") != "pilot_micro_packs":
            errors.append("lesson_plan_profiles: facilitator_session_first_session source_card_type must be pilot_micro_packs")
        include = set(session_profile.get("include", []))
        missing_include = {
            "target_power_card_ids",
            "group_size_assumptions",
            "adult_ratio",
            "timing_blocks",
            "required_assets",
            "battery_count_back",
            "safety_rules",
            "activity_flow",
            "diagram_refs",
            "deferred_power_cards",
        } - include
        if missing_include:
            errors.append(
                f"lesson_plan_profiles: facilitator_session_first_session missing include fields {sorted(missing_include)}"
            )

    warning_ids = {
        warning.get("id")
        for warning in source.get("audit_warnings", [])
        if isinstance(warning, dict)
    }
    missing = sorted(WEAK_BOUNDARY_WARNING_IDS - warning_ids)
    if missing:
        errors.append(f"audit_warnings: missing required warning ids {missing}")
    else:
        warnings.append("Audit caution retained: validation reports known intent-sensitive boundaries instead of treating clean metrics as final proof.")


def card_text_section(markdown: str, power_card_id: str) -> str:
    pattern = rf"^#### {re.escape(power_card_id)} - .*$"
    match = re.search(pattern, markdown, flags=re.MULTILINE)
    if not match:
        return ""
    next_match = re.search(r"^#### r_[a-z]+_\d+ - .*$", markdown[match.end() :], flags=re.MULTILINE)
    if not next_match:
        return markdown[match.start() :]
    return markdown[match.start() : match.end() + next_match.start()]


def validate_pilot_run_card_records(records: list[dict[str, Any]], errors: list[str]) -> None:
    for record in records:
        power_id = record.get("power_card_id", "<missing-id>")
        assets = record.get("assets", [])
        for asset in assets:
            if not isinstance(asset, dict):
                errors.append(f"pilot run-card {power_id}: asset row must be an object")
                continue
            for field in ("kit_code", "short_label", "quantity", "quantity_basis", "preparation_state"):
                value = asset.get(field)
                if value is None or str(value).strip() == "":
                    errors.append(f"pilot run-card {power_id}: asset {asset.get('asset_id')} missing {field}")
            storage = asset.get("storage", {}) if isinstance(asset.get("storage"), dict) else {}
            if not str(storage.get("bin_id", "")).strip():
                errors.append(f"pilot run-card {power_id}: asset {asset.get('asset_id')} missing storage bin_id")

            needs_safety_metadata = (
                asset.get("supervision_level") in {"direct", "adult_controlled", "demo_only"}
                or asset.get("category") in RUN_CARD_SAFETY_METADATA_CATEGORIES
            )
            if needs_safety_metadata:
                if not asset.get("safety_flags"):
                    errors.append(f"pilot run-card {power_id}: asset {asset.get('asset_id')} missing safety_flags")
                if not str(asset.get("supervision_level", "")).strip():
                    errors.append(f"pilot run-card {power_id}: asset {asset.get('asset_id')} missing supervision_level")

            if asset.get("preparation_state") == "preloaded" or asset.get("preload_profile_id"):
                if not str(asset.get("preload_profile_id", "")).strip():
                    errors.append(f"pilot run-card {power_id}: preloaded asset {asset.get('asset_id')} missing preload_profile_id")
                if not str(asset.get("preload_profile_label", "")).strip():
                    errors.append(f"pilot run-card {power_id}: preloaded asset {asset.get('asset_id')} missing preload_profile_label")


def validate_pilot_run_card_pack(source: dict[str, Any], generated_dir: Path, errors: list[str]) -> None:
    run_card_path = generated_dir / "pilot-run-cards/index.md"
    if "lesson-plans" in run_card_path.parts:
        errors.append(f"pilot run-card output must not be under lesson-plans: {run_card_path}")

    records = generate_pilot_run_cards.pilot_run_card_records(source)
    validate_pilot_run_card_records(records, errors)
    expected_ids = [str(record.get("power_card_id")) for record in records]

    if not run_card_path.exists():
        errors.append(f"Missing generated pilot run-card pack: {run_card_path}")
        return

    actual = run_card_path.read_text(encoding="utf-8")
    expected = generate_pilot_run_cards.render_pilot_run_cards_markdown(records)
    if actual != expected:
        errors.append("generated pilot run-card pack does not match canonical source")

    actual_ids = re.findall(r"^#### (r_[a-z]+_\d+) - ", actual, flags=re.MULTILINE)
    if actual_ids != expected_ids:
        missing = sorted(set(expected_ids) - set(actual_ids))
        extra = sorted(set(actual_ids) - set(expected_ids))
        errors.append(
            f"generated pilot run-card pack has wrong Power Card scope/order; missing={missing}, extra={extra}"
        )

    for power_id in expected_ids:
        section = card_text_section(actual, power_id)
        if not section:
            errors.append(f"generated pilot run-card pack missing section for {power_id}")
            continue
        for heading in sorted(RUN_CARD_REQUIRED_HEADINGS):
            if heading not in section:
                errors.append(f"generated pilot run-card {power_id} missing heading {heading}")
        for snippet in ("- Success condition:", "Prep Notes", "Supervision Notes"):
            if snippet not in section:
                errors.append(f"generated pilot run-card {power_id} missing required output snippet {snippet!r}")
        if "##### Diagram Semantics" in section and "Diagram placeholder" not in section and "| Node | Asset | Role | Label |" not in section:
            errors.append(f"generated pilot run-card {power_id} missing diagram semantics table or placeholder")


def validate_pilot_micro_packs_source(
    source: dict[str, Any],
    power_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    packs = require_list(source.get("pilot_micro_packs"), "pilot_micro_packs", errors)
    duplicate_ids([pack for pack in packs if isinstance(pack, dict)], "pilot_micro_packs", errors)
    physical_asset_ids = {
        asset.get("id")
        for asset in source.get("asset_inventory", {}).get("physical_assets", [])
        if isinstance(asset, dict)
    }
    pilot_card_ids = {card.get("id") for card in pilot_kit_cards(source)}

    for pack in packs:
        if not isinstance(pack, dict):
            errors.append("pilot_micro_packs: each pack must be an object")
            continue
        pack_id = pack.get("id", "<missing-id>")
        for field in (
            "id",
            "title",
            "target_power_card_ids",
            "group_size_assumptions",
            "adult_ratio",
            "timing_blocks",
            "safety_rules",
            "packing_assumptions",
            "reset_count_back",
            "deferred_power_cards",
        ):
            if field not in pack:
                errors.append(f"pilot_micro_packs: pack {pack_id} missing {field}")

        target_ids = pack.get("target_power_card_ids", [])
        if not isinstance(target_ids, list) or not target_ids:
            errors.append(f"pilot_micro_packs: pack {pack_id} target_power_card_ids must be a non-empty list")
            target_ids = []
        target_id_set = set()
        for power_id in target_ids:
            if power_id not in power_by_id:
                errors.append(f"pilot_micro_packs: pack {pack_id} references unknown target Power Card {power_id}")
            elif power_id not in pilot_card_ids:
                errors.append(f"pilot_micro_packs: pack {pack_id} target {power_id} is outside the pilot kit scope")
            target_id_set.add(power_id)

        assumptions = pack.get("group_size_assumptions")
        if not isinstance(assumptions, dict):
            errors.append(f"pilot_micro_packs: pack {pack_id} group_size_assumptions must be an object")
            assumptions = {}
        child_counts = assumptions.get("child_counts")
        if child_counts != [4, 5, 6]:
            errors.append(f"pilot_micro_packs: pack {pack_id} child_counts must be exactly [4, 5, 6]")
        session_minutes = assumptions.get("session_minutes")
        if not isinstance(session_minutes, dict) or session_minutes.get("min") != 45 or session_minutes.get("max") != 60:
            errors.append(f"pilot_micro_packs: pack {pack_id} session_minutes must cover 45-60 minutes")
        pair_counts = assumptions.get("pair_counts_by_child_count")
        if not isinstance(pair_counts, dict) or pair_counts.get("4") != 2 or pair_counts.get("5") != 3 or pair_counts.get("6") != 3:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include pair counts for 4, 5, and 6 children")
        if not isinstance(assumptions.get("table_count"), int) or assumptions.get("table_count") < 1:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include a positive table_count")

        adult_ratio = pack.get("adult_ratio")
        if not isinstance(adult_ratio, dict):
            errors.append(f"pilot_micro_packs: pack {pack_id} adult_ratio must be an object")
        else:
            if adult_ratio.get("required_facilitators") != 1:
                errors.append(f"pilot_micro_packs: pack {pack_id} must require 1 facilitator")
            if adult_ratio.get("recommended_helpers") != 1:
                errors.append(f"pilot_micro_packs: pack {pack_id} must recommend 1 helper")

        timing_blocks = pack.get("timing_blocks")
        if not isinstance(timing_blocks, list) or not timing_blocks:
            errors.append(f"pilot_micro_packs: pack {pack_id} timing_blocks must be a non-empty list")
            timing_blocks = []
        timing_card_ids: set[str] = set()
        for index, block in enumerate(timing_blocks, start=1):
            if not isinstance(block, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} timing_blocks[{index}] must be an object")
                continue
            for field in ("minutes", "title", "facilitator_script"):
                if not str(block.get(field, "")).strip():
                    errors.append(f"pilot_micro_packs: pack {pack_id} timing_blocks[{index}] missing {field}")
            for power_id in block.get("target_power_card_ids", []):
                if power_id not in power_by_id:
                    errors.append(f"pilot_micro_packs: pack {pack_id} timing block references unknown Power Card {power_id}")
                if power_id not in target_id_set:
                    errors.append(f"pilot_micro_packs: pack {pack_id} timing block includes non-target card {power_id}")
                timing_card_ids.add(power_id)
        if target_id_set - timing_card_ids:
            errors.append(
                f"pilot_micro_packs: pack {pack_id} timing blocks do not include targets {sorted(target_id_set - timing_card_ids)}"
            )

        for list_field in ("safety_rules", "packing_assumptions", "adult_setup_checklist", "pilot_observation_focus"):
            value = pack.get(list_field)
            if not isinstance(value, list) or not value or any(not str(item).strip() for item in value):
                errors.append(f"pilot_micro_packs: pack {pack_id} {list_field} must be a non-empty string list")

        if pack_id in generate_lesson_plans.SESSION_LESSON_PACK_IDS:
            target_support = pack.get("target_age_support_assumptions")
            if not isinstance(target_support, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} target_age_support_assumptions must be an object")
                target_support = {}
            for field in ("target_age", "support_level", "access_note"):
                if not str(target_support.get(field, "")).strip():
                    errors.append(
                        f"pilot_micro_packs: pack {pack_id} target_age_support_assumptions missing {field}"
                    )

            differentiation = pack.get("lesson_differentiation")
            if not isinstance(differentiation, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} lesson_differentiation must be an object")
                differentiation = {}
            for field in ("simplify", "repeat", "stretch", "stop_condition"):
                if not str(differentiation.get(field, "")).strip():
                    errors.append(f"pilot_micro_packs: pack {pack_id} lesson_differentiation missing {field}")

            follow_up = pack.get("follow_up_recommendations")
            if not isinstance(follow_up, list) or not follow_up or any(not str(item).strip() for item in follow_up):
                errors.append(f"pilot_micro_packs: pack {pack_id} follow_up_recommendations must be a non-empty string list")

        reset_count_back = pack.get("reset_count_back")
        if not isinstance(reset_count_back, dict):
            errors.append(f"pilot_micro_packs: pack {pack_id} reset_count_back must be an object")
            reset_count_back = {}
        battery_count_back = reset_count_back.get("battery_count_back")
        if not isinstance(battery_count_back, list) or not battery_count_back:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include battery_count_back entries")
            battery_count_back = []
        for index, item in enumerate(battery_count_back, start=1):
            if not isinstance(item, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} battery_count_back[{index}] must be an object")
                continue
            asset_ids = item.get("asset_ids")
            if not isinstance(asset_ids, list) or not asset_ids:
                errors.append(f"pilot_micro_packs: pack {pack_id} battery_count_back[{index}] must include asset_ids")
                continue
            for asset_id in asset_ids:
                if asset_id not in physical_asset_ids:
                    errors.append(f"pilot_micro_packs: pack {pack_id} battery_count_back references unknown asset {asset_id}")
            if not str(item.get("note", "")).strip():
                errors.append(f"pilot_micro_packs: pack {pack_id} battery_count_back[{index}] missing note")
        pack_away_steps = reset_count_back.get("pack_away_steps")
        if not isinstance(pack_away_steps, list) or not pack_away_steps:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include reset/pack-away steps")

        card_sequence = pack.get("card_sequence")
        if not isinstance(card_sequence, list) or not card_sequence:
            errors.append(f"pilot_micro_packs: pack {pack_id} card_sequence must be a non-empty list")
            card_sequence = []
        sequence_ids = []
        for index, item in enumerate(card_sequence, start=1):
            if not isinstance(item, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} card_sequence[{index}] must be an object")
                continue
            power_id = item.get("power_card_id")
            if power_id not in target_id_set:
                errors.append(f"pilot_micro_packs: pack {pack_id} card_sequence includes non-target card {power_id}")
            sequence_ids.append(power_id)
            for field in ("purpose", "stop_condition", "handoff_cue"):
                if not str(item.get(field, "")).strip():
                    errors.append(f"pilot_micro_packs: pack {pack_id} card_sequence[{index}] missing {field}")
        if sequence_ids != target_ids:
            errors.append(f"pilot_micro_packs: pack {pack_id} card_sequence must match target_power_card_ids order")

        for exclusion in pack.get("asset_exclusions", []):
            if not isinstance(exclusion, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} asset_exclusions entries must be objects")
                continue
            power_id = exclusion.get("power_card_id")
            asset_id = exclusion.get("asset_id")
            if power_id not in target_id_set:
                errors.append(f"pilot_micro_packs: pack {pack_id} asset exclusion references non-target card {power_id}")
                continue
            required_asset_ids = {
                requirement.get("asset_id")
                for requirement in power_by_id.get(power_id, {}).get("required_assets", [])
                if isinstance(requirement, dict)
            }
            if asset_id not in required_asset_ids:
                errors.append(
                    f"pilot_micro_packs: pack {pack_id} asset exclusion references asset {asset_id} not required by {power_id}"
                )
            if asset_id not in physical_asset_ids:
                errors.append(f"pilot_micro_packs: pack {pack_id} asset exclusion references unknown asset {asset_id}")
            if not str(exclusion.get("reason", "")).strip():
                errors.append(f"pilot_micro_packs: pack {pack_id} asset exclusion missing reason")

        diagram_refs = pack.get("diagram_refs")
        if not isinstance(diagram_refs, list) or not diagram_refs:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include diagram_refs")
            diagram_refs = []
        has_r_pow_02_safe_diagram = False
        for index, ref in enumerate(diagram_refs, start=1):
            if not isinstance(ref, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} diagram_refs[{index}] must be an object")
                continue
            power_id = ref.get("power_card_id")
            if power_id not in target_id_set:
                errors.append(f"pilot_micro_packs: pack {pack_id} diagram ref includes non-target card {power_id}")
            if power_id == "r_pow_02" and ref.get("kind") == "static_svg" and str(ref.get("output_filename", "")).endswith(".svg"):
                has_r_pow_02_safe_diagram = True
            for field in ("id", "kind", "output_filename", "description"):
                if not str(ref.get(field, "")).strip():
                    errors.append(f"pilot_micro_packs: pack {pack_id} diagram_refs[{index}] missing {field}")
        if "r_pow_02" in target_id_set and not has_r_pow_02_safe_diagram:
            errors.append(f"pilot_micro_packs: pack {pack_id} must include a static safe-circuit diagram reference for r_pow_02")

        deferred_items = pack.get("deferred_power_cards")
        if not isinstance(deferred_items, list):
            errors.append(f"pilot_micro_packs: pack {pack_id} deferred_power_cards must be a list")
            deferred_items = []
        deferred_ids = set()
        for index, item in enumerate(deferred_items, start=1):
            if not isinstance(item, dict):
                errors.append(f"pilot_micro_packs: pack {pack_id} deferred_power_cards[{index}] must be an object")
                continue
            power_id = item.get("power_card_id")
            if power_id not in power_by_id:
                errors.append(f"pilot_micro_packs: pack {pack_id} defers unknown Power Card {power_id}")
            if power_id in target_id_set:
                errors.append(f"pilot_micro_packs: pack {pack_id} deferred card {power_id} is also a target")
            if not str(item.get("reason", "")).strip():
                errors.append(f"pilot_micro_packs: pack {pack_id} deferred card {power_id} missing reason")
            deferred_ids.add(power_id)
        if "r_pow_10" in target_id_set or "r_pow_10" in timing_card_ids or "r_pow_10" in sequence_ids:
            errors.append(f"pilot_micro_packs: pack {pack_id} must not include deferred card r_pow_10")
        if "r_pow_10" not in deferred_ids:
            errors.append(f"pilot_micro_packs: pack {pack_id} must explicitly defer r_pow_10")
        if pack_id == "first_session":
            expected_deferred = pilot_card_ids - target_id_set
            if deferred_ids != expected_deferred:
                errors.append(
                    f"pilot_micro_packs: first_session deferred cards must equal non-target pilot cards; "
                    f"missing={sorted(expected_deferred - deferred_ids)}, extra={sorted(deferred_ids - expected_deferred)}"
                )


def validate_pilot_micro_pack_outputs(source: dict[str, Any], generated_dir: Path, errors: list[str]) -> None:
    output_dir = generated_dir / "pilot-micro-packs"
    packs = source.get("pilot_micro_packs", [])
    for pack in packs:
        if not isinstance(pack, dict):
            continue
        pack_id = str(pack.get("id", "pilot-micro-pack"))
        slug = generate_pilot_micro_packs.slugify(pack_id)
        markdown_path = output_dir / f"{slug}.md"
        if not markdown_path.exists():
            errors.append(f"Missing generated pilot micro-pack: {markdown_path}")
            continue
        actual = markdown_path.read_text(encoding="utf-8")
        expected = generate_pilot_micro_packs.render_micro_pack_markdown(source, pack)
        if actual != expected:
            errors.append(f"generated pilot micro-pack {pack_id} does not match canonical source")
        for snippet in (
            "## One-Page Facilitator Timing Script",
            "## Kit Pick List By Bin",
            "## Battery Count-Back Sheet",
            "## Reset And Pack-Away Checklist",
            "r_pow_02 Safe-Circuit Diagram",
        ):
            if snippet not in actual:
                errors.append(f"generated pilot micro-pack {pack_id} missing section {snippet!r}")

        if any(isinstance(ref, dict) and ref.get("power_card_id") == "r_pow_02" for ref in pack.get("diagram_refs", [])):
            diagram_filename = generate_pilot_micro_packs.r_pow_02_diagram_filename(pack)
            diagram_path = output_dir / diagram_filename
            if not diagram_path.exists():
                errors.append(f"Missing generated r_pow_02 safe-circuit diagram: {diagram_path}")
            else:
                expected_svg = generate_pilot_micro_packs.render_r_pow_02_safe_circuit_svg(source)
                actual_svg = diagram_path.read_text(encoding="utf-8")
                if actual_svg != expected_svg:
                    errors.append(f"generated r_pow_02 safe-circuit diagram {diagram_filename} does not match canonical source")
                for snippet in ("A034", "A037", "positive lead", "negative return", "ADULT CHECK", "No loose AA cells"):
                    if snippet not in actual_svg:
                        errors.append(f"generated r_pow_02 safe-circuit diagram missing {snippet!r}")


def validate_session_lesson_plan_outputs(source: dict[str, Any], generated_dir: Path, errors: list[str]) -> None:
    output_dir = generated_dir / "session-lesson-plans"
    index_path = output_dir / "index.md"
    if not index_path.exists():
        errors.append(f"Missing generated session lesson-plan index: {index_path}")

    power_by_id = {
        card.get("id"): card
        for card in source.get("power_cards", [])
        if isinstance(card, dict) and card.get("id")
    }
    family_by_id = {
        family.get("id"): family
        for family in source.get("skill_cards", [])
        if isinstance(family, dict) and family.get("id")
    }
    level_by_id = {
        level.get("id"): level
        for level in source.get("levels", [])
        if isinstance(level, dict) and level.get("id")
    }
    physical_asset_ids = {
        asset.get("id")
        for asset in source.get("asset_inventory", {}).get("physical_assets", [])
        if isinstance(asset, dict) and asset.get("id")
    }

    for pack in source.get("pilot_micro_packs", []):
        if not isinstance(pack, dict) or pack.get("id") not in generate_lesson_plans.SESSION_LESSON_PACK_IDS:
            continue

        pack_id = str(pack.get("id"))
        target_ids = [str(card_id) for card_id in pack.get("target_power_card_ids", [])]
        for card_id in target_ids:
            card = power_by_id.get(card_id)
            if not card:
                errors.append(f"session lesson plan {pack_id}: target card {card_id} does not exist")
                continue
            if not isinstance(card.get("activity_flow"), dict):
                errors.append(f"session lesson plan {pack_id}: target card {card_id} missing activity_flow")
            for requirement in card.get("required_assets", []):
                if not isinstance(requirement, dict):
                    continue
                asset_id = requirement.get("asset_id")
                if asset_id not in physical_asset_ids:
                    errors.append(
                        f"session lesson plan {pack_id}: target card {card_id} references unknown required asset {asset_id}"
                    )

        child_counts = [str(count) for count in pack.get("group_size_assumptions", {}).get("child_counts", [])]
        asset_rows = generate_pilot_micro_packs.micro_pack_asset_rows(source, pack)
        for row in asset_rows:
            quantities = row.get("quantity_by_child_count", {})
            missing_counts = [count for count in child_counts if count not in quantities or not isinstance(quantities[count], int)]
            if missing_counts:
                errors.append(
                    f"session lesson plan {pack_id}: asset {row.get('asset_id')} missing quantities for child counts {missing_counts}"
                )

        slug = generate_pilot_micro_packs.slugify(pack_id)
        markdown_path = output_dir / f"{slug}.md"
        if not markdown_path.exists():
            errors.append(f"Missing generated session lesson plan: {markdown_path}")
            continue

        actual = markdown_path.read_text(encoding="utf-8")
        expected = generate_lesson_plans.render_session_lesson_plan(
            pack,
            source,
            power_by_id,
            family_by_id,
            level_by_id,
        )
        if actual != expected:
            errors.append(f"generated session lesson plan {pack_id} does not match canonical source")

        for section in sorted(SESSION_LESSON_REQUIRED_SECTIONS):
            if section not in actual:
                errors.append(f"generated session lesson plan {pack_id} missing section {section!r}")

        for card_id in target_ids:
            if f"### {card_id} - " not in actual:
                errors.append(f"generated session lesson plan {pack_id} missing activity sequence for {card_id}")

        required_snippets = [
            "No child-authored code in this session.",
            "## Battery Count-Back Sheet",
            "## Safety Rules",
            "## Reset And Pack-Away Checklist",
            "## Deliberately Deferred Cards",
            "r_pow_02 safe circuit: `../pilot-micro-packs/",
        ]
        for snippet in required_snippets:
            if snippet not in actual:
                errors.append(f"generated session lesson plan {pack_id} missing required snippet {snippet!r}")

        if "r_pow_02" in target_ids:
            diagram_filename = generate_pilot_micro_packs.r_pow_02_diagram_filename(pack)
            if f"../pilot-micro-packs/{diagram_filename}" not in actual:
                errors.append(f"generated session lesson plan {pack_id} missing r_pow_02 diagram reference")

        deferred_ids = {
            item.get("power_card_id")
            for item in pack.get("deferred_power_cards", [])
            if isinstance(item, dict)
        }
        for deferred_id in deferred_ids:
            if str(deferred_id) not in actual:
                errors.append(f"generated session lesson plan {pack_id} missing deferred card {deferred_id}")


def validate_generated_outputs(source: dict[str, Any], generated_dir: Path, errors: list[str]) -> None:
    browser_curriculum = extract_window_json(
        generated_dir / "browser/curriculum-data.js",
        "INVENTION_CLUB_CURRICULUM",
        errors,
    )
    expected_browser = expected_browser_curriculum_payload(source)
    if browser_curriculum:
        expected_keys = set(expected_browser)
        missing = sorted(expected_keys - set(browser_curriculum))
        if missing:
            errors.append(f"generated browser curriculum: missing keys {missing}")
        if browser_curriculum != expected_browser:
            errors.append("generated browser curriculum-data.js payload does not structurally match canonical source")

    root_curriculum = extract_window_json(ROOT / "curriculum-data.js", "INVENTION_CLUB_CURRICULUM", errors)
    if root_curriculum and browser_curriculum and root_curriculum != browser_curriculum:
        errors.append("root curriculum-data.js does not match generated browser curriculum-data.js")

    scene_bundle = generated_dir / "browser/power-card-scenes.js"
    root_scene = ROOT / "power-card-scenes.js"
    if not scene_bundle.exists():
        errors.append(f"Missing generated browser scene bundle: {scene_bundle}")
    elif root_scene.exists() and scene_bundle.read_text(encoding="utf-8") != root_scene.read_text(encoding="utf-8"):
        errors.append("generated browser power-card-scenes.js does not match root power-card-scenes.js baseline")

    expected_generated_payloads = {
        "families.yaml": {"realistic": source.get("skill_cards", [])},
        "power_cards.yaml": {"realistic": source.get("power_cards", [])},
        "integration_cards.yaml": {"realistic": source.get("integration_cards", [])},
        "invention_cards.yaml": {"realistic": source.get("invention_cards", [])},
        "red_team_cases.yaml": {"cases": source.get("red_team_cases", [])},
        "asset-inventory.json": source.get("asset_inventory", {}),
        "preload-manifest.json": {"profiles": source.get("preload_profiles", [])},
        "pilot-kit-list.json": expected_pilot_kit_list(source),
    }
    for filename, expected_payload in expected_generated_payloads.items():
        path = generated_dir / filename
        if not path.exists():
            errors.append(f"Missing generated artefact: {path}")
            continue
        payload = load_json(path, errors)
        if payload and payload != expected_payload:
            errors.append(f"generated artefact {filename} does not structurally match canonical source")

    validate_pilot_run_card_pack(source, generated_dir, errors)
    validate_pilot_micro_pack_outputs(source, generated_dir, errors)
    validate_session_lesson_plan_outputs(source, generated_dir, errors)


def compute_metrics(source: dict[str, Any], power_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    powers = list(power_by_id.values())
    families = source.get("skill_cards", [])
    integrations = source.get("integration_cards", [])
    level_counts: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for power in powers:
        level_counts[power.get("primary_family")][power.get("level")] += 1

    return {
        "counts": {
            "skill_cards": len(families),
            "power_cards": len(powers),
            "integration_cards": len(source.get("integration_cards", [])),
            "invention_cards": len(source.get("invention_cards", [])),
            "red_team_cases": len(source.get("red_team_cases", [])),
            "assets": len(source.get("asset_inventory", {}).get("assets", [])),
            "physical_assets": len(source.get("asset_inventory", {}).get("physical_assets", [])),
            "programmable_preload_profiles": len(
                source.get("asset_inventory", {}).get("programmable_preload_profiles", [])
            ),
            "pilot_cards_with_required_assets": sum(1 for power in powers if power.get("required_assets")),
            "pilot_cards_with_activity_flow": sum(1 for power in powers if power.get("activity_flow")),
            "pilot_micro_packs": len(source.get("pilot_micro_packs", [])),
            "session_lesson_plans": sum(
                1
                for pack in source.get("pilot_micro_packs", [])
                if isinstance(pack, dict) and pack.get("id") in generate_lesson_plans.SESSION_LESSON_PACK_IDS
            ),
            "preload_profiles": len(source.get("preload_profiles", [])),
        },
        "power_cards_by_family_level": {
            family_id: {str(level): counts.get(level, 0) for level in range(1, 7)}
            for family_id, counts in sorted(level_counts.items())
        },
        "power_cards_with_supporting_families": sum(1 for power in powers if power.get("supporting_families")),
        "power_cards_with_classification_rationale": sum(
            1 for power in powers if str(power.get("classification_rationale", "")).strip()
        ),
        "integration_to_power_ratio": len(integrations) / len(powers) if powers else 0,
        "red_team_classifications": dict(Counter(case.get("classification") for case in source.get("red_team_cases", []))),
    }


def validate_source(source_path: Path, generated_dir: Path, validate_generated: bool) -> tuple[dict[str, Any], int]:
    errors: list[str] = []
    warnings: list[str] = []
    source = load_json(source_path, errors)
    if errors or not require_object(source, "source", errors):
        result = {"mechanical_valid": False, "errors": errors, "warnings": warnings}
        return result, 1

    validate_top_level(source, errors)
    validation_strategy = validate_schema_contract(source, errors, warnings)
    level_ids = validate_levels(source, errors)
    family_ids = validate_skill_cards(source, level_ids, errors)
    power_by_id = validate_power_cards(source, family_ids, level_ids, errors)
    level_audit = audit_power_card_levels(power_by_id)
    add_level_audit_warnings(level_audit, warnings)
    validate_integrations(source, family_ids, power_by_id, errors)
    validate_inventions(source, family_ids, errors)
    validate_assets(source, power_by_id, errors)
    validate_pilot_micro_packs_source(source, power_by_id, errors)
    validate_profiles_and_audit(source, errors, warnings)
    if validate_generated:
        validate_generated_outputs(source, generated_dir, errors)

    result = {
        "mechanical_valid": not errors,
        "source": str(source_path.relative_to(ROOT) if source_path.is_relative_to(ROOT) else source_path),
        "generated_dir": str(generated_dir.relative_to(ROOT) if generated_dir.is_relative_to(ROOT) else generated_dir),
        "validation_strategy": validation_strategy,
        "metrics": compute_metrics(source, power_by_id),
        "level_audit": level_audit,
        "errors": errors,
        "warnings": warnings,
    }
    return result, 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--curriculum-dir", default=str(DEFAULT_GENERATED_DIR))
    parser.add_argument("--output", required=True)
    parser.add_argument("--level-audit-output", default=str(DEFAULT_LEVEL_AUDIT_OUTPUT))
    parser.add_argument("--skip-generated", action="store_true")
    args = parser.parse_args()

    result, exit_code = validate_source(Path(args.source), Path(args.curriculum_dir), not args.skip_generated)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.level_audit_output:
        write_level_audit_report(Path(args.level_audit_output), result.get("level_audit", {"items": [], "rules": []}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
