from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
RAWDATA_DIR = ROOT_DIR / "rawdata"
DATA_JSON = RAWDATA_DIR / "data.json"
TAGS_JSON = RAWDATA_DIR / "tags.json"


@dataclass(frozen=True)
class PromptOption:
    option_id: str
    top_category_id: str
    top_category_name: str
    subcategory_id: str
    subcategory_name: str
    child_category_id: str
    child_category_name: str
    zh_label: str
    prompt: str
    note: str
    display_label: str
    group_label: str


@dataclass(frozen=True)
class BlockCatalog:
    block_key: str
    top_categories: tuple[str, ...]
    group_labels: tuple[str, ...]
    options: tuple[PromptOption, ...]


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_category_tree() -> dict:
    return _load_json(DATA_JSON)


@lru_cache(maxsize=1)
def load_tag_templates() -> dict:
    return _load_json(TAGS_JSON)


@lru_cache(maxsize=1)
def build_category_indexes() -> dict:
    tree = load_category_tree()
    top_by_name = {}
    subcategories_by_top = {}
    child_names_by_subcategory = {}

    for top_category in tree.get("categories", []):
        top_by_name[top_category["name"]] = top_category
        subcategory_name_map = {}
        for subcategory in top_category.get("subcategories", []):
            subcategory_name_map[subcategory["id"]] = subcategory["name"]
            child_names_by_subcategory[subcategory["id"]] = {
                child["id"]: child["name"] for child in subcategory.get("children", [])
            }
        subcategories_by_top[top_category["id"]] = subcategory_name_map

    return {
        "top_by_name": top_by_name,
        "subcategories_by_top": subcategories_by_top,
        "child_names_by_subcategory": child_names_by_subcategory,
    }


def _make_group_label(subcategory_name: str, child_name: str) -> str:
    return f"{subcategory_name} / {child_name}" if child_name else subcategory_name


def _make_display_label(group_label: str, zh_label: str, prompt: str) -> str:
    if zh_label and zh_label != prompt:
        return f"{group_label} | {zh_label} -> {prompt}"
    return f"{group_label} | {prompt}"


def _dedupe_display_labels(options: list[PromptOption]) -> list[PromptOption]:
    counts = {}
    deduped_options = []
    for option in options:
        counts[option.display_label] = counts.get(option.display_label, 0) + 1
        if counts[option.display_label] == 1:
            deduped_options.append(option)
            continue

        display_label = f"{option.display_label} ({counts[option.display_label]})"
        deduped_options.append(
            PromptOption(
                option_id=option.option_id,
                top_category_id=option.top_category_id,
                top_category_name=option.top_category_name,
                subcategory_id=option.subcategory_id,
                subcategory_name=option.subcategory_name,
                child_category_id=option.child_category_id,
                child_category_name=option.child_category_name,
                zh_label=option.zh_label,
                prompt=option.prompt,
                note=option.note,
                display_label=display_label,
                group_label=option.group_label,
            )
        )
    return deduped_options


@lru_cache(maxsize=32)
def get_catalog(block_key: str, top_category_names: tuple[str, ...]) -> BlockCatalog:
    indexes = build_category_indexes()
    tags_data = load_tag_templates().get("categoryTemplates", {})

    options: list[PromptOption] = []
    group_labels = set()

    for top_category_name in top_category_names:
        top_category = indexes["top_by_name"].get(top_category_name)
        if not top_category:
            continue

        top_id = top_category["id"]
        subcategory_names = indexes["subcategories_by_top"].get(top_id, {})

        for tag in tags_data.get(top_id, []):
            prompt = (tag.get("en") or tag.get("zh") or "").strip()
            if not prompt:
                continue

            subcategory_id = tag.get("subcategoryId", "")
            child_category_id = tag.get("childCategoryId", "")
            subcategory_name = subcategory_names.get(subcategory_id, "未分类")
            child_name = indexes["child_names_by_subcategory"].get(subcategory_id, {}).get(child_category_id, "")
            group_label = _make_group_label(subcategory_name, child_name)
            display_label = _make_display_label(group_label, tag.get("zh", "").strip(), prompt)

            group_labels.add(group_label)
            options.append(
                PromptOption(
                    option_id=tag.get("id", ""),
                    top_category_id=top_id,
                    top_category_name=top_category_name,
                    subcategory_id=subcategory_id,
                    subcategory_name=subcategory_name,
                    child_category_id=child_category_id,
                    child_category_name=child_name,
                    zh_label=tag.get("zh", "").strip(),
                    prompt=prompt,
                    note=tag.get("note", "").strip(),
                    display_label=display_label,
                    group_label=group_label,
                )
            )

    deduped_options = tuple(_dedupe_display_labels(options))
    ordered_groups = tuple(sorted(group_labels))
    return BlockCatalog(
        block_key=block_key,
        top_categories=top_category_names,
        group_labels=ordered_groups,
        options=deduped_options,
    )


@lru_cache(maxsize=128)
def get_filtered_catalog(
    block_key: str,
    top_category_names: tuple[str, ...],
    allowed_subcategory_names: tuple[str, ...] = (),
    excluded_subcategory_names: tuple[str, ...] = (),
) -> BlockCatalog:
    base_catalog = get_catalog(block_key, top_category_names)
    allowed = set(allowed_subcategory_names)
    excluded = set(excluded_subcategory_names)

    filtered_options = []
    filtered_groups = set()

    for option in base_catalog.options:
        if allowed and option.subcategory_name not in allowed:
            continue
        if excluded and option.subcategory_name in excluded:
            continue
        filtered_options.append(option)
        filtered_groups.add(option.group_label)

    return BlockCatalog(
        block_key=block_key,
        top_categories=top_category_names,
        group_labels=tuple(sorted(filtered_groups)),
        options=tuple(filtered_options),
    )


@lru_cache(maxsize=1)
def get_color_catalog() -> BlockCatalog:
    return get_filtered_catalog(
        "palette_colors",
        ("画面",),
        ("颜色",),
        (),
    )
