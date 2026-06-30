OC_BLOCK_TYPE = "OC_BLOCK"
OC_PART_TYPE = "OC_PART"
OUTFIT_STYLE_PART_TYPE = "OC_PART_OUTFIT_STYLE"
OUTFIT_UPPER_PART_TYPE = "OC_PART_OUTFIT_UPPER"
OUTFIT_OUTER_PART_TYPE = "OC_PART_OUTFIT_OUTER"
OUTFIT_LOWER_PART_TYPE = "OC_PART_OUTFIT_LOWER"
OUTFIT_LEGWEAR_PART_TYPE = "OC_PART_OUTFIT_LEGWEAR"
OUTFIT_FOOTWEAR_PART_TYPE = "OC_PART_OUTFIT_FOOTWEAR"
OUTFIT_HEADWEAR_PART_TYPE = "OC_PART_OUTFIT_HEADWEAR"
OUTFIT_FACEWEAR_PART_TYPE = "OC_PART_OUTFIT_FACEWEAR"
OUTFIT_JEWELRY_PART_TYPE = "OC_PART_OUTFIT_JEWELRY"
OUTFIT_DECORATION_PART_TYPE = "OC_PART_OUTFIT_DECORATION"
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

OUTFIT_SLOT_ORDER = [
    "base_style",
    "upper",
    "outer",
    "lower",
    "legwear",
    "footwear",
    "headwear",
    "facewear",
    "jewelry",
    "decoration",
]


def empty_block(block_type: str, category: str) -> dict:
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


def empty_part(part_slot: str, part_category: str) -> dict:
    return {
        "part_type": "generic",
        "part_slot": part_slot,
        "part_category": part_category,
        "group": "",
        "label": "",
        "prompt": "",
        "mode": "unset",
        "index": -1,
        "pool_size": 0,
        "top_category": "",
        "subcategory": "",
        "child_category": "",
        "option_id": "",
        "note": "",
        "requested_group": "",
        "requested_option": "",
        "requested_option_in_group": False,
    }
