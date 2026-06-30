from __future__ import annotations

from hashlib import sha256
import json

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_data import BlockCatalog, PromptOption, get_catalog
from .oc_dynamic_input import ContainsDynamicDict


OC_BLOCK_TYPE = "OC_BLOCK"
ALL_GROUPS = "__all_groups__"
PROMPT_ORDER = [
    "Theme",
    "Species",
    "Body",
    "Face",
    "Hair",
    "Outfit",
    "Accessories",
    "Personality",
    "Color",
    "Pose",
    "Camera",
    "Rendering",
]


def _stable_seed(*parts) -> int:
    payload = "|".join(str(part) for part in parts)
    return int(sha256(payload.encode("utf-8")).hexdigest()[:16], 16)


def _normalize_step(step: int) -> int:
    return max(1, int(step))


def _empty_block(block_type: str, category: str) -> dict:
    return {
        "block_type": block_type,
        "category": category,
        "group": "",
        "label": "",
        "prompt": "",
        "mode": "fixed",
        "index": -1,
        "pool_size": 0,
        "top_category": "",
        "subcategory": "",
        "child_category": "",
        "option_id": "",
        "note": "",
    }


def _flatten_connected_blocks(kwargs: dict) -> list[dict]:
    flattened = []
    for key, value in kwargs.items():
        if not key.startswith("oc_block_"):
            continue

        values = value if isinstance(value, list) else [value]
        for item in values:
            if isinstance(item, dict):
                flattened.append(item)
            elif isinstance(item, str) and item.strip():
                flattened.append(
                    {
                        "block_type": "raw",
                        "category": "Raw",
                        "group": "",
                        "label": item.strip(),
                        "prompt": item.strip(),
                        "mode": "fixed",
                        "index": 0,
                        "pool_size": 1,
                        "top_category": "",
                        "subcategory": "",
                        "child_category": "",
                        "option_id": "",
                        "note": "",
                    }
                )
    return flattened


def _first_value(value, default=None):
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default


class BaseOCBlockNode(ComfyNodeABC):
    CATEGORY = "OC Generator/Blocks"
    FUNCTION = "build_block"
    RETURN_TYPES = (OC_BLOCK_TYPE, IO.STRING, IO.STRING)
    RETURN_NAMES = ("oc_block", "prompt_preview", "debug_text")

    BLOCK_KEY = "base"
    BLOCK_CATEGORY = "Base"
    TOP_CATEGORY_NAMES: tuple[str, ...] = ()

    @classmethod
    def _catalog(cls) -> BlockCatalog:
        return get_catalog(cls.BLOCK_KEY, tuple(cls.TOP_CATEGORY_NAMES))

    @classmethod
    def INPUT_TYPES(cls):
        catalog = cls._catalog()
        group_choices = [ALL_GROUPS, *catalog.group_labels] or [ALL_GROUPS]
        option_choices = [option.display_label for option in catalog.options] or ["No options available"]
        return {
            "required": {
                "group": (group_choices, {"default": group_choices[0]}),
                "mode": (["fixed", "randomize", "increment", "decrement"], {"default": "fixed"}),
                "option": (option_choices, {"default": option_choices[0]}),
            },
            "optional": {
                "enabled": (IO.BOOLEAN, {"default": True}),
                "seed": (IO.INT, {"default": 0, "min": 0, "max": 0xFFFFFFFF}),
                "step": (IO.INT, {"default": 1, "min": 1, "max": 1024}),
            },
        }

    @classmethod
    def _select_pool(cls, catalog: BlockCatalog, group: str) -> list[PromptOption]:
        if group == ALL_GROUPS:
            return list(catalog.options)

        filtered = [option for option in catalog.options if option.group_label == group]
        return filtered or list(catalog.options)

    @classmethod
    def _find_current_index(cls, pool: list[PromptOption], option_label: str) -> int:
        for index, option in enumerate(pool):
            if option.display_label == option_label:
                return index
        return 0

    @classmethod
    def _resolve_selection(
        cls,
        pool: list[PromptOption],
        option_label: str,
        mode: str,
        seed: int,
        step: int,
        group: str,
    ) -> tuple[int, PromptOption]:
        current_index = cls._find_current_index(pool, option_label)
        if mode == "fixed":
            return current_index, pool[current_index]

        if mode == "randomize":
            random_index = _stable_seed(cls.BLOCK_KEY, group, option_label, seed) % len(pool)
            return random_index, pool[random_index]

        delta = _normalize_step(step)
        if mode == "decrement":
            delta = -delta
        next_index = (current_index + delta) % len(pool)
        return next_index, pool[next_index]

    def build_block(self, group, mode, option, enabled=True, seed=0, step=1):
        if not enabled:
            empty = _empty_block(self.BLOCK_KEY, self.BLOCK_CATEGORY)
            return (empty, "", f"{self.BLOCK_CATEGORY}: disabled")

        catalog = self._catalog()
        pool = self._select_pool(catalog, group)
        if not pool:
            empty = _empty_block(self.BLOCK_KEY, self.BLOCK_CATEGORY)
            return (empty, "", f"{self.BLOCK_CATEGORY}: no options loaded")

        selected_index, selected = self._resolve_selection(pool, option, mode, seed, step, group)
        block = {
            "block_type": self.BLOCK_KEY,
            "category": self.BLOCK_CATEGORY,
            "group": selected.group_label,
            "label": selected.zh_label or selected.prompt,
            "prompt": selected.prompt,
            "mode": mode,
            "index": selected_index,
            "pool_size": len(pool),
            "top_category": selected.top_category_name,
            "subcategory": selected.subcategory_name,
            "child_category": selected.child_category_name,
            "option_id": selected.option_id,
            "note": selected.note,
        }
        debug_text = (
            f"{self.BLOCK_CATEGORY}: {selected.prompt} "
            f"[group={selected.group_label}, mode={mode}, index={selected_index}/{len(pool)}]"
        )
        return (block, selected.prompt, debug_text)


class OCThemeBlockNode(BaseOCBlockNode):
    BLOCK_KEY = "theme"
    BLOCK_CATEGORY = "Theme"
    TOP_CATEGORY_NAMES = ("场景", "画面")


class OCGeneratorNode(ComfyNodeABC):
    CATEGORY = "OC Generator"
    FUNCTION = "generate_prompt"
    RETURN_TYPES = (IO.STRING, IO.STRING, IO.STRING)
    RETURN_NAMES = ("positive_prompt", "blocks_json", "debug_text")
    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prefix_prompt": (IO.STRING, {"default": "", "multiline": True}),
                "suffix_prompt": (IO.STRING, {"default": "", "multiline": True}),
                "separator": (IO.STRING, {"default": ", "}),
                "dedupe": (IO.BOOLEAN, {"default": True}),
            },
            "optional": ContainsDynamicDict(
                {
                    "oc_block_0": (
                        OC_BLOCK_TYPE,
                        {"forceInput": True, "_dynamic": "number", "widgetType": "STRING"},
                    )
                }
            ),
        }

    @staticmethod
    def _sort_blocks(blocks: list[dict]) -> list[dict]:
        order_map = {name: index for index, name in enumerate(PROMPT_ORDER)}
        return sorted(blocks, key=lambda block: (order_map.get(block.get("category", ""), 999), block.get("group", "")))

    @staticmethod
    def _collect_prompt_parts(blocks: list[dict], dedupe: bool) -> list[str]:
        parts = []
        seen = set()
        for block in blocks:
            prompt = str(block.get("prompt", "")).strip()
            if not prompt:
                continue
            if dedupe and prompt in seen:
                continue
            seen.add(prompt)
            parts.append(prompt)
        return parts

    def generate_prompt(self, prefix_prompt, suffix_prompt, separator, dedupe, **kwargs):
        prefix_prompt = str(_first_value(prefix_prompt, "")).strip()
        suffix_prompt = str(_first_value(suffix_prompt, "")).strip()
        separator = str(_first_value(separator, ", "))
        dedupe = bool(_first_value(dedupe, True))

        blocks = self._sort_blocks(_flatten_connected_blocks(kwargs))
        prompt_parts = self._collect_prompt_parts(blocks, dedupe)

        final_parts = [prefix_prompt, *prompt_parts, suffix_prompt]
        final_prompt = separator.join(part for part in final_parts if part)

        debug_lines = [
            f"{block['category']}: {block.get('prompt', '')} [{block.get('mode', 'fixed')}]"
            for block in blocks
            if block.get("prompt")
        ]
        blocks_json = json.dumps(blocks, ensure_ascii=False, indent=2)
        debug_text = "\n".join(debug_lines)
        return (final_prompt, blocks_json, debug_text)


NODE_CLASS_MAPPINGS = {
    "OCGeneratorNode": OCGeneratorNode,
    "OCThemeBlockNode": OCThemeBlockNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OCGeneratorNode": "OC Generator",
    "OCThemeBlockNode": "OC Theme Block",
}
