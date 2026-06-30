from __future__ import annotations

from inspect import cleandoc

try:
    from comfy.comfy_types.node_typing import IO, ComfyNodeABC
except ImportError:
    class IO:
        BOOLEAN = "BOOLEAN"
        STRING = "STRING"

    ComfyNodeABC = object

from .oc_block_base import BaseOCBlockNode
from .oc_types import (
    OC_BLOCK_TYPE,
    OUTFIT_DECORATION_PART_TYPE,
    OUTFIT_FACEWEAR_PART_TYPE,
    OUTFIT_FOOTWEAR_PART_TYPE,
    OUTFIT_HEADWEAR_PART_TYPE,
    OUTFIT_JEWELRY_PART_TYPE,
    OUTFIT_LEGWEAR_PART_TYPE,
    OUTFIT_LOWER_PART_TYPE,
    OUTFIT_OUTER_PART_TYPE,
    OUTFIT_STYLE_PART_TYPE,
    OUTFIT_UPPER_PART_TYPE,
    empty_block,
)


def _normalized_part(value) -> dict | None:
    if isinstance(value, dict):
        return value
    return None


class OCCharacterBodyBlockNode(BaseOCBlockNode):
    """Character body block for role identity, age, body, and non-face physical traits."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "character_body"
    BLOCK_CATEGORY = "Body"
    TOP_CATEGORY_NAMES = ("人物",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "对象",
        "身份",
        "二次元角色",
        "年龄",
        "皮肤",
        "身材",
        "肩部",
        "胸部",
        "腰部",
        "腹部",
        "腿部",
        "脚部",
        "翅膀",
    )


class OCCharacterFaceBlockNode(BaseOCBlockNode):
    """Character face block for facial structure and expression-capable facial features."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "character_face"
    BLOCK_CATEGORY = "Face"
    TOP_CATEGORY_NAMES = ("人物",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "脸型",
        "面部",
        "耳朵",
        "眉毛",
        "眼睛",
        "瞳孔",
        "鼻子",
        "嘴巴",
        "牙齿",
        "舌头",
    )


class OCCharacterHairBlockNode(BaseOCBlockNode):
    """Character hair block for hairstyle-level selection."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "character_hair"
    BLOCK_CATEGORY = "Hair"
    TOP_CATEGORY_NAMES = ("人物",)
    ALLOWED_SUBCATEGORY_NAMES = ("发型",)


class OCCharacterAccessoriesBlockNode(BaseOCBlockNode):
    """Character accessories block for piercing, jewelry, and other decorative add-ons."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "character_accessories"
    BLOCK_CATEGORY = "Accessories"
    TOP_CATEGORY_NAMES = ("人物", "服饰")
    ALLOWED_SUBCATEGORY_NAMES = (
        "穿刺、穿环、纹身",
        "面部饰品",
        "耳饰",
        "头饰",
        "帽子",
        "发饰",
        "装饰",
        "首饰",
        "其他",
    )


class OCCharacterOutfitBlockNode(ComfyNodeABC):
    """Aggregate outfit part nodes into one structured Outfit block."""

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator/Character"
    FUNCTION = "build_outfit_block"
    RETURN_TYPES = (OC_BLOCK_TYPE, IO.STRING, IO.STRING)
    RETURN_NAMES = ("oc_block", "prompt_preview", "debug_text")
    OUTPUT_TOOLTIPS = (
        "Structured Outfit block composed from connected outfit parts.",
        "The final outfit prompt fragment assembled from slot inputs.",
        "Readable slot-by-slot summary for the composed outfit.",
    )

    SLOT_INPUTS = (
        ("base_style_part", OUTFIT_STYLE_PART_TYPE, "Outfit style input."),
        ("upper_part", OUTFIT_UPPER_PART_TYPE, "Upper clothing input such as tops and shirts."),
        ("outer_part", OUTFIT_OUTER_PART_TYPE, "Outerwear input such as coats and jackets."),
        ("lower_part", OUTFIT_LOWER_PART_TYPE, "Lower clothing input such as pants or skirts."),
        ("legwear_part", OUTFIT_LEGWEAR_PART_TYPE, "Legwear input such as socks or stockings."),
        ("footwear_part", OUTFIT_FOOTWEAR_PART_TYPE, "Footwear input such as shoes or boots."),
        ("headwear_part", OUTFIT_HEADWEAR_PART_TYPE, "Headwear input such as hats or hair decorations."),
        ("facewear_part", OUTFIT_FACEWEAR_PART_TYPE, "Facewear input such as glasses or masks."),
        ("jewelry_part", OUTFIT_JEWELRY_PART_TYPE, "Jewelry input such as earrings and necklaces."),
        ("decoration_part", OUTFIT_DECORATION_PART_TYPE, "Decorative accessory input."),
    )

    @classmethod
    def INPUT_TYPES(cls):
        optional_inputs = {}
        for input_name, input_type, tooltip in cls.SLOT_INPUTS:
            optional_inputs[input_name] = (
                input_type,
                {"forceInput": True, "tooltip": tooltip},
            )

        return {
            "required": {
                "separator": (
                    IO.STRING,
                    {
                        "default": ", ",
                        "tooltip": "String used to join outfit slot prompts.",
                    },
                ),
                "dedupe": (
                    IO.BOOLEAN,
                    {
                        "default": True,
                        "tooltip": "Remove duplicated outfit fragments during composition.",
                    },
                ),
            },
            "optional": optional_inputs,
        }

    def build_outfit_block(self, separator, dedupe, **kwargs):
        parts = []
        debug_lines = []
        seen_prompts = set()

        for input_name, _input_type, _tooltip in self.SLOT_INPUTS:
            part = _normalized_part(kwargs.get(input_name))
            if not part:
                continue
            prompt = str(part.get("prompt", "")).strip()
            if not prompt:
                debug_lines.append(f"{input_name}: unset")
                continue
            if dedupe and prompt in seen_prompts:
                debug_lines.append(f"{input_name}: duplicate skipped -> {prompt}")
                continue
            seen_prompts.add(prompt)
            parts.append(part)
            debug_lines.append(f"{input_name}: {prompt} [{part.get('mode', 'fixed')}]")

        if not parts:
            empty = empty_block("character_outfit", "Outfit")
            empty["mode"] = "composed"
            return (empty, "", "Outfit: no active parts")

        final_prompt = separator.join(part["prompt"] for part in parts if part.get("prompt"))
        block = {
            "block_type": "character_outfit",
            "category": "Outfit",
            "group": "Outfit Slots",
            "label": "Character Outfit",
            "prompt": final_prompt,
            "mode": "composed",
            "index": len(parts),
            "pool_size": len(parts),
            "top_category": "服饰",
            "subcategory": "",
            "child_category": "",
            "option_id": "",
            "note": "",
            "parts": parts,
        }
        return (block, final_prompt, "\n".join(debug_lines))
