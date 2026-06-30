OC_BLOCK_TYPE = "OC_BLOCK"
OC_PART_TYPE = "OC_PART"
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
