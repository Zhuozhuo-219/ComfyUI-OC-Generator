from __future__ import annotations

from inspect import cleandoc

from .oc_block_base import BaseOCBlockNode


class OCRenderingBlockNode(BaseOCBlockNode):
    """Rendering block for visual style, quality, brush language, and image effects.

    The current rawdata does not yet provide a strong dedicated artist-string dataset,
    so this block focuses on the rendering-oriented entries already available under `画面`.
    """

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "rendering"
    BLOCK_CATEGORY = "Rendering"
    TOP_CATEGORY_NAMES = ("画面",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "画质",
        "艺术风格",
        "素描",
        "画笔",
        "颜色",
        "画面效果",
    )
