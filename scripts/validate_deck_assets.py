#!/usr/bin/env python3
"""Validate deck artifact consistency and coverage."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

PML_NAMESPACE = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
URL_PATTERN = re.compile(r"^https?://\S+$")
SPEAKER_SLIDE_PATTERN = re.compile(r"^## Slide (\d+)\s+-\s+", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[1]

    parser = argparse.ArgumentParser(
        description=(
            "Validate deck slide-count alignment, image coverage, and reference coverage "
            "across deck artifacts."
        )
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root,
        help="Repository root directory (default: inferred from script path).",
    )
    parser.add_argument(
        "--deck",
        type=Path,
        default=Path("agents.pptx"),
        help="Path to deck .pptx file (default: agents.pptx).",
    )
    parser.add_argument(
        "--image-map",
        type=Path,
        default=Path("presentation_assets/slide_image_map.json"),
        help="Path to slide image mapping JSON.",
    )
    parser.add_argument(
        "--references-map",
        type=Path,
        default=Path("presentation_assets/slide_references.json"),
        help="Path to slide reference mapping JSON.",
    )
    parser.add_argument(
        "--speaker-notes",
        type=Path,
        default=Path("presentation_assets/speaker_notes.md"),
        help="Path to speaker notes markdown.",
    )
    parser.add_argument(
        "--expected-references-per-slide",
        type=int,
        default=3,
        help="Expected number of references per slide (default: 3).",
    )
    return parser.parse_args()


def resolve_path(repo_root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def load_slide_count_from_pptx(deck_path: Path) -> int:
    if not deck_path.is_file():
        raise ValueError(f"deck file not found: {deck_path}")
    if not zipfile.is_zipfile(deck_path):
        raise ValueError(f"deck file is not a valid .pptx archive: {deck_path}")

    with zipfile.ZipFile(deck_path) as archive:
        try:
            presentation_xml = archive.read("ppt/presentation.xml")
        except KeyError as exc:
            raise ValueError("ppt/presentation.xml missing in deck archive") from exc

    root = ElementTree.fromstring(presentation_xml)
    slide_id_list = root.find("p:sldIdLst", PML_NAMESPACE)
    if slide_id_list is None:
        return 0
    return len(slide_id_list.findall("p:sldId", PML_NAMESPACE))


def load_slide_keyed_map(path: Path, label: str) -> tuple[dict[int, Any], list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, [f"{label}: file not found ({path})"]
    except json.JSONDecodeError as exc:
        return {}, [f"{label}: invalid JSON at {path}: {exc}"]

    if not isinstance(data, Mapping):
        return {}, [f"{label}: expected top-level JSON object in {path}"]

    normalized: dict[int, Any] = {}
    for raw_key, value in data.items():
        if not isinstance(raw_key, str):
            errors.append(f"{label}: non-string key {raw_key!r}")
            continue
        try:
            slide_number = int(raw_key)
        except ValueError:
            errors.append(f"{label}: key is not an integer slide number: {raw_key!r}")
            continue
        if slide_number < 1:
            errors.append(f"{label}: key must be >= 1: {raw_key!r}")
            continue
        if slide_number in normalized:
            errors.append(
                f"{label}: duplicate slide key after normalization: {slide_number}"
            )
            continue
        normalized[slide_number] = value

    return normalized, errors


def validate_contiguous_keys(
    keys: Sequence[int], label: str, expected_end: int | None = None
) -> list[str]:
    errors: list[str] = []
    if not keys:
        return [f"{label}: no slide keys found"]

    sorted_keys = sorted(keys)
    if sorted_keys[0] != 1:
        errors.append(f"{label}: first key must be 1, got {sorted_keys[0]}")

    expected_last = expected_end if expected_end is not None else sorted_keys[-1]
    expected = list(range(1, expected_last + 1))
    if sorted_keys != expected:
        missing = sorted(set(expected) - set(sorted_keys))
        extras = sorted(set(sorted_keys) - set(expected))
        if missing:
            errors.append(f"{label}: missing slide keys: {missing}")
        if extras:
            errors.append(f"{label}: out-of-range slide keys: {extras}")
    return errors


def load_speaker_notes_slides(path: Path) -> tuple[list[int], list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [], [f"speaker_notes: file not found ({path})"]

    slide_numbers = [int(match.group(1)) for match in SPEAKER_SLIDE_PATTERN.finditer(text)]
    if not slide_numbers:
        return [], [f"speaker_notes: no slide headers found in {path}"]
    return slide_numbers, []


def path_exists_for_image(repo_root: Path, raw_path: str) -> bool:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = repo_root / candidate
    candidate = candidate.resolve()
    if candidate.exists():
        return True
    if candidate.suffix.lower() == ".svg":
        return candidate.with_suffix(".png").exists()
    return False


def validate_image_coverage(
    repo_root: Path, image_map: dict[int, Any], expected_slide_count: int
) -> list[str]:
    errors: list[str] = []
    errors.extend(
        validate_contiguous_keys(
            keys=list(image_map.keys()),
            label="slide_image_map",
            expected_end=expected_slide_count,
        )
    )

    expected_slides = set(range(1, expected_slide_count + 1))
    for slide in sorted(expected_slides):
        entries = image_map.get(slide)
        if not isinstance(entries, list) or not entries:
            errors.append(f"slide_image_map: slide {slide} must have at least one image")
            continue
        for raw_entry in entries:
            if not isinstance(raw_entry, str) or not raw_entry.strip():
                errors.append(
                    f"slide_image_map: slide {slide} has invalid image path value {raw_entry!r}"
                )
                continue
            if not path_exists_for_image(repo_root, raw_entry):
                errors.append(
                    f"slide_image_map: slide {slide} image path not found: {raw_entry}"
                )
    return errors


def validate_reference_coverage(
    references_map: dict[int, Any], expected_slide_count: int, expected_ref_count: int
) -> list[str]:
    errors: list[str] = []
    errors.extend(
        validate_contiguous_keys(
            keys=list(references_map.keys()),
            label="slide_references",
            expected_end=expected_slide_count,
        )
    )

    expected_slides = set(range(1, expected_slide_count + 1))
    for slide in sorted(expected_slides):
        refs = references_map.get(slide)
        if not isinstance(refs, list):
            errors.append(f"slide_references: slide {slide} references must be a list")
            continue
        if len(refs) != expected_ref_count:
            errors.append(
                f"slide_references: slide {slide} expected {expected_ref_count} "
                f"refs, found {len(refs)}"
            )
        for ref in refs:
            if not isinstance(ref, str) or not URL_PATTERN.match(ref):
                errors.append(
                    f"slide_references: slide {slide} has invalid URL value {ref!r}"
                )
    return errors


def print_summary(
    *,
    deck_slides: int | None,
    speaker_slide_count: int | None,
    image_map_slides: int,
    image_entries: int,
    reference_map_slides: int,
    reference_entries: int,
    alignment_errors: list[str],
    image_errors: list[str],
    reference_errors: list[str],
) -> None:
    print("deck_asset_validator")
    print(f"deck_slide_count={deck_slides if deck_slides is not None else 'N/A'}")
    print(
        f"speaker_notes_slide_count="
        f"{speaker_slide_count if speaker_slide_count is not None else 'N/A'}"
    )
    print(f"image_map_slide_keys={image_map_slides}")
    print(f"image_map_entries={image_entries}")
    print(f"references_map_slide_keys={reference_map_slides}")
    print(f"references_map_entries={reference_entries}")
    print(f"slide_count_alignment={'PASS' if not alignment_errors else 'FAIL'}")
    print(f"image_coverage={'PASS' if not image_errors else 'FAIL'}")
    print(f"reference_coverage={'PASS' if not reference_errors else 'FAIL'}")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()

    deck_path = resolve_path(repo_root, args.deck)
    image_map_path = resolve_path(repo_root, args.image_map)
    references_map_path = resolve_path(repo_root, args.references_map)
    speaker_notes_path = resolve_path(repo_root, args.speaker_notes)

    input_errors: list[str] = []
    alignment_errors: list[str] = []
    image_errors: list[str] = []
    reference_errors: list[str] = []

    try:
        deck_slide_count = load_slide_count_from_pptx(deck_path)
    except ValueError as exc:
        deck_slide_count = None
        input_errors.append(f"deck: {exc}")

    image_map, image_map_load_errors = load_slide_keyed_map(
        image_map_path, "slide_image_map"
    )
    input_errors.extend(image_map_load_errors)

    references_map, references_map_load_errors = load_slide_keyed_map(
        references_map_path, "slide_references"
    )
    input_errors.extend(references_map_load_errors)

    speaker_numbers, speaker_load_errors = load_speaker_notes_slides(speaker_notes_path)
    input_errors.extend(speaker_load_errors)

    speaker_slide_count: int | None = None
    if speaker_numbers:
        speaker_slide_count = len(speaker_numbers)
        alignment_errors.extend(
            validate_contiguous_keys(speaker_numbers, "speaker_notes_sections")
        )

    image_map_slide_count = len(image_map)
    image_entries = sum(len(v) for v in image_map.values() if isinstance(v, list))
    reference_map_slide_count = len(references_map)
    reference_entries = sum(len(v) for v in references_map.values() if isinstance(v, list))

    if deck_slide_count is not None:
        if speaker_slide_count is not None and speaker_slide_count != deck_slide_count:
            alignment_errors.append(
                "slide_count_mismatch: "
                f"deck={deck_slide_count}, speaker_notes={speaker_slide_count}"
            )
        if image_map_slide_count != deck_slide_count:
            alignment_errors.append(
                "slide_count_mismatch: "
                f"deck={deck_slide_count}, slide_image_map={image_map_slide_count}"
            )
        if reference_map_slide_count != deck_slide_count:
            alignment_errors.append(
                "slide_count_mismatch: "
                f"deck={deck_slide_count}, slide_references={reference_map_slide_count}"
            )

    expected_slide_count = deck_slide_count
    if expected_slide_count is None:
        discovered_counts = [
            count for count in [speaker_slide_count, image_map_slide_count, reference_map_slide_count] if count
        ]
        expected_slide_count = max(discovered_counts, default=0)
        if expected_slide_count == 0:
            input_errors.append("unable to infer expected slide count from any artifact")

    if expected_slide_count > 0:
        image_errors.extend(
            validate_image_coverage(repo_root, image_map, expected_slide_count)
        )
        reference_errors.extend(
            validate_reference_coverage(
                references_map,
                expected_slide_count,
                args.expected_references_per_slide,
            )
        )

    print_summary(
        deck_slides=deck_slide_count,
        speaker_slide_count=speaker_slide_count,
        image_map_slides=image_map_slide_count,
        image_entries=image_entries,
        reference_map_slides=reference_map_slide_count,
        reference_entries=reference_entries,
        alignment_errors=alignment_errors + input_errors,
        image_errors=image_errors,
        reference_errors=reference_errors,
    )

    all_errors = input_errors + alignment_errors + image_errors + reference_errors
    if all_errors:
        print("status=FAIL")
        for issue in all_errors:
            print(f"- {issue}")
        return 1

    print("status=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
