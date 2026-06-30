from __future__ import annotations

from inspect import cleandoc
import json

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        BOOLEAN = "BOOLEAN"
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_dynamic_input import ContainsDynamicDict
from .oc_types import OC_BLOCK_TYPE, PROMPT_ORDER


def first_value(value, default=None):
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default


def flatten_connected_blocks(kwargs: dict) -> list[dict]:
    def flatten_item(item):
        if isinstance(item, dict) and item.get("block_type") == "merge_bundle":
            flattened_items = []
            for child in item.get("items", []):
                flattened_items.extend(flatten_item(child))
            return flattened_items
        if isinstance(item, dict):
            return [item]
        if isinstance(item, str) and item.strip():
            return [
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
            ]
        return []

    flattened = []
    for key, value in kwargs.items():
        if not key.startswith("oc_block_"):
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            flattened.extend(flatten_item(item))
    return flattened


class OCGeneratorNode(ComfyNodeABC):
    """Aggregate multiple OC blocks into one positive prompt string."""

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator"
    FUNCTION = "generate_prompt"
    RETURN_TYPES = (IO.STRING, IO.STRING, IO.STRING)
    RETURN_NAMES = ("positive_prompt", "blocks_json", "debug_text")
    OUTPUT_TOOLTIPS = (
        "The final positive prompt assembled from prefix, OC blocks, and suffix.",
        "JSON dump of all received OC blocks after sorting, useful for inspection or future export.",
        "Readable execution summary for each connected block.",
    )
    INPUT_IS_LIST = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prefix_prompt": (
                    IO.STRING,
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Static prompt text inserted before all OC block fragments.",
                    },
                ),
                "suffix_prompt": (
                    IO.STRING,
                    {
                        "default": "",
                        "multiline": True,
                        "tooltip": "Static prompt text appended after all OC block fragments.",
                    },
                ),
                "separator": (
                    IO.STRING,
                    {
                        "default": ", ",
                        "tooltip": "String used to join prefix, block prompts, and suffix.",
                    },
                ),
                "dedupe": (
                    IO.BOOLEAN,
                    {
                        "default": True,
                        "tooltip": "Remove duplicated prompt fragments after block aggregation.",
                    },
                ),
            },
            "optional": ContainsDynamicDict(
                {
                    "oc_block_0": (
                        OC_BLOCK_TYPE,
                        {
                            "forceInput": True,
                            "_dynamic": "number",
                            "widgetType": "STRING",
                            "tooltip": "Connect one OC block per socket. Additional sockets can be added dynamically in the UI.",
                        },
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
        prefix_prompt = str(first_value(prefix_prompt, "")).strip()
        suffix_prompt = str(first_value(suffix_prompt, "")).strip()
        separator = str(first_value(separator, ", "))
        dedupe = bool(first_value(dedupe, True))

        blocks = self._sort_blocks(flatten_connected_blocks(kwargs))
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
