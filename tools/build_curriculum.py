#!/usr/bin/env python3
"""Build generated curriculum artefacts from the canonical source.

The initial migration can also bootstrap the canonical source from the current
website data and schema stress-test files. After that, generated artefacts
should come from ``curriculum/source/curriculum.v1.json``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "curriculum/source/curriculum.v1.json"
GENERATED_DIR = ROOT / "curriculum/generated"
BROWSER_DIR = GENERATED_DIR / "browser"
LESSON_DIR = GENERATED_DIR / "lesson-plans"

SKILL_ICON_BY_FAMILY = {
    "movement": "assets/skill-icons/make-it-move.jpg",
    "control_input": "assets/skill-icons/make-it-obey.jpg",
    "sensing": "assets/skill-icons/make-it-notice.jpg",
    "structures": "assets/skill-icons/make-it-strong.jpg",
    "power": "assets/skill-icons/make-it-run-safely.jpg",
    "materials_fabrication": "assets/skill-icons/make-it-real.jpg",
    "logic_sequencing": "assets/skill-icons/make-it-decide.jpg",
    "communication": "assets/skill-icons/make-it-signal.jpg",
    "debugging_testing": "assets/skill-icons/make-it-work-again.jpg",
    "design_iteration": "assets/skill-icons/make-it-better.jpg",
}

FAMILY_SUMMARIES = {
    "movement": "Motors, servos, wheels and mechanisms.",
    "control_input": "Buttons, switches, knobs and controllers.",
    "sensing": "Sensors for light, tilt, distance or touch.",
    "structures": "Frames, hinges, mounts and stable builds.",
    "power": "Batteries, polarity, loads and safe choices.",
    "materials_fabrication": "Materials, fabrication, joins and enclosures.",
    "logic_sequencing": "Sequences, rules, timing and simple logic.",
    "communication": "Messages, radio links, alerts and displays.",
    "debugging_testing": "Testing, debugging, repair and evidence.",
    "design_iteration": "User needs, criteria, feedback and iteration.",
}

GLOBAL_LEVELS = [
    {
        "id": 1,
        "name": "Encounter",
        "child_facing_summary": "Recognise it and use it safely.",
        "facilitator_definition": "Recognise parts, signals, inputs, materials, expected behaviour, and safe setup before trying to control or alter them.",
        "coding_expectation": "No code required; children recognise parts, signals, inputs, and safe setup.",
    },
    {
        "id": 2,
        "name": "Activate",
        "child_facing_summary": "Make the basic thing happen.",
        "facilitator_definition": "Make one simple output, input, sequence, message, test, or design move work in a controlled setup.",
        "coding_expectation": "Use direct wiring, unplugged logic, or a provided starter program without needing to edit code.",
    },
    {
        "id": 3,
        "name": "Adjust",
        "child_facing_summary": "Change how it behaves.",
        "facilitator_definition": "Change one variable such as speed, range, threshold, timing, mapping, material fit, test method, or criterion.",
        "coding_expectation": "Adjust one parameter, threshold, timing value, mapping, or condition in a known pattern.",
    },
    {
        "id": 4,
        "name": "Apply",
        "child_facing_summary": "Use it in a new context.",
        "facilitator_definition": "Transfer a known skill to a different build, user, material, environment, subsystem, or constraint.",
        "coding_expectation": "Adapt a known code or logic pattern to a new physical context with facilitator support.",
    },
    {
        "id": 5,
        "name": "Coordinate",
        "child_facing_summary": "Make related things work together.",
        "facilitator_definition": "Coordinate multiple related elements inside the same primary family, while keeping other families supporting rather than primary.",
        "coding_expectation": "Coordinate multiple inputs, outputs, states, messages, or subsystems; child can explain event or state flow.",
    },
    {
        "id": 6,
        "name": "Improve",
        "child_facing_summary": "Test, refine and explain trade-offs.",
        "facilitator_definition": "Debug, refine, optimise, or explain trade-offs in the family object of study; only make Debugging/Testing primary when the diagnostic method is the learning target.",
        "coding_expectation": "Debug, simplify, compare, or justify code, logic, and physical trade-offs; older learners may write short programs, but coding is not the only route.",
    },
]

WEAK_BOUNDARY_WARNINGS = [
    {
        "id": "human_facing_design_boundaries",
        "source": "reports/amendment-audit.md",
        "summary": "Comfort, feedback, aesthetics, repairability and planning remain intent-sensitive and should keep explicit rationales when used as power cards.",
    },
    {
        "id": "metrics_overstate_certainty",
        "source": "reports/amendment-audit.md",
        "summary": "Validation metrics are useful but should not be treated as proof that all ambiguity disappeared.",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_window_json(path: Path, global_name: str) -> Any:
    text = path.read_text(encoding="utf-8")
    prefix = f"window.{global_name} = "
    start = text.index(prefix) + len(prefix)
    payload = text[start:].strip()
    if payload.endswith(";"):
        payload = payload[:-1]
    return json.loads(payload)


def block_after(text: str, marker: str) -> str:
    start = text.index(marker)
    brace_start = text.index("{", start)
    depth = 0
    for index in range(brace_start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start : index + 1]
    raise ValueError(f"Could not parse block after {marker!r}")


def parse_js_string_arrays(block: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for match in re.finditer(r"(\w+):\s*\[(.*?)\]", block, flags=re.S):
        key = match.group(1)
        values = re.findall(r'"([^"]+)"', match.group(2))
        result[key] = values
    return result


def parse_js_string_map(block: str) -> dict[str, str]:
    return dict(re.findall(r"(\w+):\s*\"([^\"]+)\"", block))


def scene_assignments(scene_path: Path) -> list[dict[str, Any]]:
    text = scene_path.read_text(encoding="utf-8")
    accents = parse_js_string_map(block_after(text, "const familyAccents"))
    cards = parse_js_string_arrays(block_after(text, "const familyCards"))
    templates = parse_js_string_arrays(block_after(text, "const familyTemplates"))
    assignments: list[dict[str, Any]] = []
    for family_id, card_ids in cards.items():
        family_templates = templates.get(family_id, [])
        for index, card_id in enumerate(card_ids):
            assignments.append(
                {
                    "card_id": card_id,
                    "family": family_id,
                    "template": family_templates[index] if index < len(family_templates) else None,
                    "accent": accents.get(family_id),
                }
            )
    return assignments


def asset_entry(asset_id: str, category: str, path: str, **extra: Any) -> dict[str, Any]:
    entry = {"id": asset_id, "category": category, "path": path}
    entry.update(extra)
    return entry


def build_asset_inventory(
    families: list[dict[str, Any]],
    power_cards: list[dict[str, Any]],
    assignments: list[dict[str, Any]],
) -> dict[str, Any]:
    assets: list[dict[str, Any]] = [
        asset_entry("hero_workshop", "hero_image", "assets/invention-workshop-hero.png"),
        asset_entry("parts_tray_workbench", "background_image", "assets/parts-tray-workbench.png"),
        asset_entry("integration_card_icon", "card_type_icon", "assets/card-icons/integration-card.jpg"),
        asset_entry("invention_card_icon", "card_type_icon", "assets/card-icons/invention-card.jpg"),
        asset_entry(
            "integration_sample_button_controlled_wheel",
            "integration_sample",
            "assets/integration-samples/button-controlled-wheel.png",
        ),
        asset_entry(
            "integration_sample_light_sensitive_sign",
            "integration_sample",
            "assets/integration-samples/light-sensitive-sign.png",
        ),
        asset_entry(
            "integration_sample_servo_greeting_sign",
            "integration_sample",
            "assets/integration-samples/servo-greeting-sign.png",
        ),
    ]

    for family in families:
        icon_asset = family.get("icon_asset")
        if icon_asset:
            assets.append(
                asset_entry(
                    f"skill_icon_{family['id']}",
                    "skill_icon",
                    icon_asset,
                    family_id=family["id"],
                )
            )

    seen_result_paths: set[str] = set()
    for card in power_cards:
        result_image = card.get("result_image")
        if result_image and result_image not in seen_result_paths:
            seen_result_paths.add(result_image)
            assets.append(
                asset_entry(
                    f"power_result_{card['id']}",
                    "power_card_result",
                    result_image,
                    card_id=card["id"],
                )
            )

    return {
        "version": 1,
        "assets": assets,
        "scene_assignments": assignments,
        "scene_runtime": {
            "source_file": "power-card-scenes.js",
            "generated_file": "curriculum/generated/browser/power-card-scenes.js",
            "status": "preserved_baseline_runtime_no_svg_generation",
        },
        "future_svg_generation": {
            "status": "prepared_not_implemented",
            "notes": [
                "Existing SVG result assets remain the rendered baseline.",
                "Scene assignments are validated so a future renderer can be introduced without changing card content.",
            ],
        },
    }


def build_preload_profiles(asset_inventory: dict[str, Any]) -> list[dict[str, Any]]:
    assets = asset_inventory["assets"]

    def ids_for(category: str) -> list[str]:
        return [asset["id"] for asset in assets if asset["category"] == category]

    return [
        {
            "id": "homepage",
            "description": "Assets needed for the parent-facing homepage.",
            "asset_ids": [
                "hero_workshop",
                "integration_sample_button_controlled_wheel",
                "integration_sample_light_sensitive_sign",
                "integration_sample_servo_greeting_sign",
            ],
        },
        {
            "id": "curriculum_initial",
            "description": "Assets needed before a family/level selection on the sessions page.",
            "asset_ids": ids_for("skill_icon") + ["integration_card_icon", "invention_card_icon"],
        },
        {
            "id": "curriculum_power_cards",
            "description": "Generated Power Card result assets and browser data bundles.",
            "asset_ids": ids_for("power_card_result"),
            "generated_files": [
                "curriculum/generated/browser/curriculum-data.js",
                "curriculum/generated/browser/power-card-scenes.js",
            ],
        },
        {
            "id": "print_preview",
            "description": "Full visual deck preview asset set.",
            "asset_ids": ids_for("skill_icon") + ids_for("card_type_icon") + ids_for("power_card_result"),
        },
    ]


def lesson_plan_profiles() -> list[dict[str, Any]]:
    return [
        {
            "id": "facilitator_integration_cards",
            "name": "Facilitator Integration Card Plans",
            "output_dir": "curriculum/generated/lesson-plans",
            "source_card_type": "integration_cards",
            "include": [
                "required_power_cards",
                "dependency_chain",
                "materials",
                "safety_notes",
                "debug_prompts",
                "stretch_and_invention_follow_ons",
            ],
        }
    ]


def bootstrap_source() -> dict[str, Any]:
    website_data = extract_window_json(ROOT / "curriculum-data.js", "INVENTION_CLUB_CURRICULUM")
    generated_dir = ROOT / "curriculum/generated"
    integrations = load_json(generated_dir / "integration_cards.yaml")["realistic"]
    inventions = load_json(generated_dir / "invention_cards.yaml")["realistic"]
    red_team_cases = load_json(generated_dir / "red_team_cases.yaml")["cases"]

    families = []
    for family in website_data["families"]:
        family = dict(family)
        family["icon_asset"] = SKILL_ICON_BY_FAMILY.get(family["id"], "")
        family["summary"] = FAMILY_SUMMARIES.get(family["id"], "")
        families.append(family)

    assignments = scene_assignments(ROOT / "power-card-scenes.js")
    asset_inventory = build_asset_inventory(families, website_data["powerCards"], assignments)

    return {
        "meta": {
            "schema_version": "curriculum.v1",
            "source_status": "canonical_bootstrapped_from_current_website_and_generated_curriculum",
            "generation_timestamp_policy": "Do not store volatile timestamps in generated artefacts; use stable deterministic output for reviewable diffs.",
            "baseline_note": "Uses the 120-card website Power Card set as the operational baseline; the previous 80-card realistic generated set remains historical validation evidence.",
        },
        "levels": GLOBAL_LEVELS,
        "skill_cards": families,
        "power_cards": website_data["powerCards"],
        "integration_cards": integrations,
        "invention_cards": inventions,
        "asset_inventory": asset_inventory,
        "preload_profiles": build_preload_profiles(asset_inventory),
        "lesson_plan_profiles": lesson_plan_profiles(),
        "red_team_cases": red_team_cases,
        "audit_warnings": WEAK_BOUNDARY_WARNINGS,
    }


def browser_curriculum_payload(source: dict[str, Any]) -> dict[str, Any]:
    families = []
    for family in source["skill_cards"]:
        browser_family = {key: value for key, value in family.items() if key not in {"icon_asset", "summary"}}
        families.append(browser_family)

    return {
        "levels": source["levels"],
        "families": families,
        "powerCards": source["power_cards"],
        "integrationCards": source["integration_cards"],
        "inventionCards": source["invention_cards"],
        "assetInventory": source["asset_inventory"],
        "preloadProfiles": source["preload_profiles"],
    }


def write_browser_bundle(path: Path, global_name: str, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"window.{global_name} = {json.dumps(payload, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


def build_outputs(source: dict[str, Any], *, mirror_root: bool = True) -> None:
    BROWSER_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    browser_payload = browser_curriculum_payload(source)
    browser_curriculum_path = BROWSER_DIR / "curriculum-data.js"
    write_browser_bundle(browser_curriculum_path, "INVENTION_CLUB_CURRICULUM", browser_payload)
    if mirror_root:
        write_browser_bundle(ROOT / "curriculum-data.js", "INVENTION_CLUB_CURRICULUM", browser_payload)

    scene_source = ROOT / "power-card-scenes.js"
    scene_output = BROWSER_DIR / "power-card-scenes.js"
    if scene_source.exists():
        shutil.copyfile(scene_source, scene_output)
    if mirror_root and scene_output.exists() and not scene_source.exists():
        shutil.copyfile(scene_output, scene_source)

    write_json(GENERATED_DIR / "families.yaml", {"realistic": source["skill_cards"]})
    write_json(GENERATED_DIR / "power_cards.yaml", {"realistic": source["power_cards"]})
    write_json(GENERATED_DIR / "integration_cards.yaml", {"realistic": source["integration_cards"]})
    write_json(GENERATED_DIR / "invention_cards.yaml", {"realistic": source["invention_cards"]})
    write_json(GENERATED_DIR / "red_team_cases.yaml", {"cases": source["red_team_cases"]})
    write_json(GENERATED_DIR / "asset-inventory.json", source["asset_inventory"])
    write_json(GENERATED_DIR / "preload-manifest.json", {"profiles": source["preload_profiles"]})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(SOURCE_PATH))
    parser.add_argument("--bootstrap-from-current", action="store_true")
    parser.add_argument("--no-root-mirror", action="store_true")
    args = parser.parse_args()

    source_path = Path(args.source)
    if args.bootstrap_from_current:
        source = bootstrap_source()
        write_json(source_path, source)
    else:
        source = load_json(source_path)

    build_outputs(source, mirror_root=not args.no_root_mirror)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
