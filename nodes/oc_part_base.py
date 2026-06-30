from __future__ import annotations

from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        INT = "INT"
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_block_base import stable_seed
from .oc_data import BlockCatalog, PromptOption, get_filtered_catalog
from .oc_types import ALL_GROUPS, OC_PART_TYPE, empty_part


class BaseOCPartNode(ComfyNodeABC):
    """Template node for a local design part such as upper clothing or footwear."""

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator/Parts"
    FUNCTION = "build_part"
    RETURN_NAMES = ("oc_part", "prompt_preview", "debug_text")
    OUTPUT_TOOLTIPS = (
        "Structured local part data for Character Outfit Block.",
        "The prompt fragment resolved by this part node.",
        "Execution details for slot filtering and random selection.",
    )

    PART_KIND = "generic"
    PART_SLOT = "generic"
    PART_CATEGORY = "Generic Part"
    PART_OUTPUT_TYPE = OC_PART_TYPE
    TOP_CATEGORY_NAMES: tuple[str, ...] = ()
    ALLOWED_SUBCATEGORY_NAMES: tuple[str, ...] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.RETURN_TYPES = (cls.PART_OUTPUT_TYPE, IO.STRING, IO.STRING)

    RETURN_TYPES = (OC_PART_TYPE, IO.STRING, IO.STRING)

    @classmethod
    def _catalog(cls) -> BlockCatalog:
        return get_filtered_catalog(
            cls.PART_KIND,
            tuple(cls.TOP_CATEGORY_NAMES),
            tuple(cls.ALLOWED_SUBCATEGORY_NAMES),
            (),
        )

    @classmethod
    def INPUT_TYPES(cls):
        catalog = cls._catalog()
        group_choices = [ALL_GROUPS, *catalog.group_labels] or [ALL_GROUPS]
        option_choices = [option.display_label for option in catalog.options] or ["No options available"]
        return {
            "required": {
                "group": (
                    group_choices,
                    {
                        "default": group_choices[0],
                        "tooltip": "Limit the part to one subgroup inside this slot. The option dropdown is still static in the UI.",
                    },
                ),
                "mode": (
                    ["unset", "fixed", "randomize"],
                    {
                        "default": "unset",
                        "tooltip": "unset emits no prompt. fixed keeps the selected option. randomize samples within the current slot pool.",
                    },
                ),
                "option": (
                    option_choices,
                    {
                        "default": option_choices[0],
                        "tooltip": "Static dropdown for all options in this part node. If the selected option is outside the current group, execution falls back to the first valid item in that group.",
                    },
                ),
            },
            "optional": {
                "seed": (
                    IO.INT,
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFF,
                        "tooltip": "Seed used by randomize mode for reproducible part selection.",
                    },
                ),
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
        return -1

    def build_part(self, group, mode, option, seed=0):
        if mode == "unset":
            empty = empty_part(self.PART_SLOT, self.PART_CATEGORY)
            empty["part_type"] = self.PART_KIND
            return (empty, "", f"{self.PART_CATEGORY}: unset")

        catalog = self._catalog()
        pool = self._select_pool(catalog, group)
        if not pool:
            empty = empty_part(self.PART_SLOT, self.PART_CATEGORY)
            empty["part_type"] = self.PART_KIND
            return (empty, "", f"{self.PART_CATEGORY}: no options loaded")

        current_index = self._find_current_index(pool, option)
        option_in_group = current_index >= 0
        if mode == "fixed":
            selected_index = current_index if current_index >= 0 else 0
        else:
            selected_index = stable_seed(self.PART_KIND, self.PART_SLOT, group, option, seed) % len(pool)
        selected = pool[selected_index]

        part = {
            "part_type": self.PART_KIND,
            "part_slot": self.PART_SLOT,
            "part_category": self.PART_CATEGORY,
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
            "requested_group": group,
            "requested_option": option,
            "requested_option_in_group": option_in_group,
        }
        mismatch_note = ""
        if not option_in_group:
            mismatch_note = " requested option not in current group; fallback applied."
        debug_text = (
            f"{self.PART_CATEGORY}: {selected.prompt} "
            f"[slot={self.PART_SLOT}, group={selected.group_label}, mode={mode}, index={selected_index}/{len(pool)}, option_in_group={option_in_group}]"
            f"{mismatch_note}"
        )
        return (part, selected.prompt, debug_text)
