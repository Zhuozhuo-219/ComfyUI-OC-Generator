from __future__ import annotations

from hashlib import sha256
from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        BOOLEAN = "BOOLEAN"
        INT = "INT"
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_data import BlockCatalog, PromptOption, get_filtered_catalog
from .oc_types import ALL_GROUPS, OC_BLOCK_TYPE, empty_block


def stable_seed(*parts) -> int:
    payload = "|".join(str(part) for part in parts)
    return int(sha256(payload.encode("utf-8")).hexdigest()[:16], 16)


def normalize_step(step: int) -> int:
    return max(1, int(step))


class BaseOCBlockNode(ComfyNodeABC):
    """Template block node for one OC design dimension.

    The UI currently exposes a static `option` dropdown for the whole catalog.
    `group` is still enforced at execution time, but it does not dynamically shrink
    the visible option list in the ComfyUI widget without additional frontend code.
    """

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator/Blocks"
    FUNCTION = "build_block"
    RETURN_TYPES = (OC_BLOCK_TYPE, IO.STRING, IO.STRING)
    RETURN_NAMES = ("oc_block", "prompt_preview", "debug_text")
    OUTPUT_TOOLTIPS = (
        "Structured OC block data for downstream aggregation in OC Generator.",
        "The prompt fragment resolved by this dimension node.",
        "Execution details, including group filtering and selection behavior.",
    )

    BLOCK_KEY = "base"
    BLOCK_CATEGORY = "Base"
    TOP_CATEGORY_NAMES: tuple[str, ...] = ()
    ALLOWED_SUBCATEGORY_NAMES: tuple[str, ...] = ()
    EXCLUDED_SUBCATEGORY_NAMES: tuple[str, ...] = ()

    @classmethod
    def _catalog(cls) -> BlockCatalog:
        return get_filtered_catalog(
            cls.BLOCK_KEY,
            tuple(cls.TOP_CATEGORY_NAMES),
            tuple(cls.ALLOWED_SUBCATEGORY_NAMES),
            tuple(cls.EXCLUDED_SUBCATEGORY_NAMES),
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
                        "tooltip": "Limit selection to one subgroup. The option dropdown itself is static and will not visually shrink when group changes.",
                    },
                ),
                "mode": (
                    ["fixed", "randomize", "increment", "decrement"],
                    {
                        "default": "fixed",
                        "tooltip": "fixed keeps the chosen option when valid for the current group. randomize / increment / decrement operate only within the selected group pool.",
                    },
                ),
                "option": (
                    option_choices,
                    {
                        "default": option_choices[0],
                        "tooltip": "Static dropdown for the whole catalog. If the chosen option does not belong to the current group, execution falls back to the first valid item in that group.",
                    },
                ),
            },
            "optional": {
                "enabled": (
                    IO.BOOLEAN,
                    {
                        "default": True,
                        "tooltip": "Disable this block without deleting it from the workflow.",
                    },
                ),
                "seed": (
                    IO.INT,
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFF,
                        "tooltip": "Seed used by randomize mode to get reproducible results inside the current group pool.",
                    },
                ),
                "step": (
                    IO.INT,
                    {
                        "default": 1,
                        "min": 1,
                        "max": 1024,
                        "tooltip": "Step size for increment / decrement mode inside the current group pool.",
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

    @classmethod
    def _resolve_selection(
        cls,
        pool: list[PromptOption],
        option_label: str,
        mode: str,
        seed: int,
        step: int,
        group: str,
    ) -> tuple[int, PromptOption, bool]:
        current_index = cls._find_current_index(pool, option_label)
        if mode == "fixed":
            if current_index >= 0:
                return current_index, pool[current_index], True
            return 0, pool[0], False

        if mode == "randomize":
            random_index = stable_seed(cls.BLOCK_KEY, group, option_label, seed) % len(pool)
            return random_index, pool[random_index], current_index >= 0

        delta = normalize_step(step)
        if mode == "decrement":
            delta = -delta
        if current_index < 0:
            current_index = 0
        next_index = (current_index + delta) % len(pool)
        return next_index, pool[next_index], current_index >= 0

    def build_block(self, group, mode, option, enabled=True, seed=0, step=1):
        if not enabled:
            empty = empty_block(self.BLOCK_KEY, self.BLOCK_CATEGORY)
            return (empty, "", f"{self.BLOCK_CATEGORY}: disabled")

        catalog = self._catalog()
        pool = self._select_pool(catalog, group)
        if not pool:
            empty = empty_block(self.BLOCK_KEY, self.BLOCK_CATEGORY)
            return (empty, "", f"{self.BLOCK_CATEGORY}: no options loaded")

        selected_index, selected, option_in_group = self._resolve_selection(pool, option, mode, seed, step, group)
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
            "requested_group": group,
            "requested_option": option,
            "requested_option_in_group": option_in_group,
        }
        mismatch_note = ""
        if not option_in_group:
            mismatch_note = " requested option not in current group; fallback applied."
        debug_text = (
            f"{self.BLOCK_CATEGORY}: {selected.prompt} "
            f"[group={selected.group_label}, mode={mode}, index={selected_index}/{len(pool)}, option_in_group={option_in_group}]"
            f"{mismatch_note}"
        )
        return (block, selected.prompt, debug_text)
