from __future__ import annotations

from inspect import cleandoc

from .oc_block_base import BaseOCBlockNode


class OCThemeBlockNode(BaseOCBlockNode):
    """Theme block for environment, atmosphere, background, and lighting context."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "theme"
    BLOCK_CATEGORY = "Theme"
    TOP_CATEGORY_NAMES = ("场景", "画面")
    ALLOWED_SUBCATEGORY_NAMES = (
        "季节",
        "天气",
        "自然景观",
        "氛围",
        "室外",
        "城市",
        "室内",
        "浴室",
        "背景",
        "光照",
    )
