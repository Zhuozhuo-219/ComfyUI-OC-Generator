from __future__ import annotations

from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_types import OC_BLOCK_TYPE


class OCBlockMergeNode(ComfyNodeABC):
    """Merge several OC blocks into one bundle so OC Generator can consume them through a single link."""

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator"
    FUNCTION = "merge_blocks"
    RETURN_TYPES = (OC_BLOCK_TYPE, IO.STRING)
    RETURN_NAMES = ("oc_block", "debug_text")
    OUTPUT_TOOLTIPS = (
        "Merged OC block bundle. Connect this to OC Generator or another merge node.",
        "Readable summary of which block inputs were merged.",
    )

    MERGE_INPUTS = (
        ("block_a", "First OC block input."),
        ("block_b", "Second OC block input."),
        ("block_c", "Third OC block input."),
        ("block_d", "Fourth OC block input."),
        ("block_e", "Fifth OC block input."),
        ("block_f", "Sixth OC block input."),
        ("block_g", "Seventh OC block input."),
        ("block_h", "Eighth OC block input."),
    )

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for input_name, tooltip in cls.MERGE_INPUTS:
            optional_inputs[input_name] = (
                OC_BLOCK_TYPE,
                {
                    "forceInput": True,
                    "tooltip": tooltip,
                },
            )

        return {"optional": optional_inputs}

    @staticmethod
    def _extract_blocks(value) -> list[dict]:
        if not isinstance(value, dict):
            return []
        if value.get("block_type") == "merge_bundle":
            items = value.get("items", [])
            return [item for item in items if isinstance(item, dict)]
        return [value]

    def merge_blocks(self, **kwargs):
        merged_items = []
        debug_lines = []
        for input_name, _tooltip in self.MERGE_INPUTS:
            value = kwargs.get(input_name)
            blocks = self._extract_blocks(value)
            if not blocks:
                continue
            merged_items.extend(blocks)
            debug_lines.append(f"{input_name}: {len(blocks)} block(s)")

        bundle = {
            "block_type": "merge_bundle",
            "category": "Merged",
            "group": "Merged",
            "label": "Merged Blocks",
            "prompt": "",
            "mode": "merged",
            "index": len(merged_items),
            "pool_size": len(merged_items),
            "top_category": "",
            "subcategory": "",
            "child_category": "",
            "option_id": "",
            "note": "",
            "items": merged_items,
        }
        return (bundle, "\n".join(debug_lines) if debug_lines else "Merge: no connected blocks")
