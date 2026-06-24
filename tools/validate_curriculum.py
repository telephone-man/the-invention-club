#!/usr/bin/env python3
"""Validate the canonical curriculum source and generated artefacts."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "curriculum/source/curriculum.v1.json"
DEFAULT_GENERATED_DIR = ROOT / "curriculum/generated"
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
    for profile in lesson_profiles:
        if not isinstance(profile, dict):
            errors.append("lesson_plan_profiles: each profile must be an object")
            continue
        for field in ("id", "name", "output_dir", "source_card_type"):
            if not str(profile.get(field, "")).strip():
                errors.append(f"lesson_plan_profiles: profile {profile.get('id', '<missing-id>')} missing non-empty {field}")

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
    }
    for filename, expected_payload in expected_generated_payloads.items():
        path = generated_dir / filename
        if not path.exists():
            errors.append(f"Missing generated artefact: {path}")
            continue
        payload = load_json(path, errors)
        if payload and payload != expected_payload:
            errors.append(f"generated artefact {filename} does not structurally match canonical source")


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
    validate_integrations(source, family_ids, power_by_id, errors)
    validate_inventions(source, family_ids, errors)
    validate_assets(source, power_by_id, errors)
    validate_profiles_and_audit(source, errors, warnings)
    if validate_generated:
        validate_generated_outputs(source, generated_dir, errors)

    result = {
        "mechanical_valid": not errors,
        "source": str(source_path.relative_to(ROOT) if source_path.is_relative_to(ROOT) else source_path),
        "generated_dir": str(generated_dir.relative_to(ROOT) if generated_dir.is_relative_to(ROOT) else generated_dir),
        "validation_strategy": validation_strategy,
        "metrics": compute_metrics(source, power_by_id),
        "errors": errors,
        "warnings": warnings,
    }
    return result, 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--curriculum-dir", default=str(DEFAULT_GENERATED_DIR))
    parser.add_argument("--output", required=True)
    parser.add_argument("--skip-generated", action="store_true")
    args = parser.parse_args()

    result, exit_code = validate_source(Path(args.source), Path(args.curriculum_dir), not args.skip_generated)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
