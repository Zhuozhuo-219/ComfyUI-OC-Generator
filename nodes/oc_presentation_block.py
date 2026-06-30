from __future__ import annotations

from inspect import cleandoc

from .oc_block_base import BaseOCBlockNode


class OCPresentationPoseBlockNode(BaseOCBlockNode):
    """Presentation pose block for base pose, body action, and non-interaction movement."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "presentation_pose"
    BLOCK_CATEGORY = "Pose"
    TOP_CATEGORY_NAMES = ("动作",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "基础动作",
        "腿部动作",
        "其他动作",
    )


class OCPresentationInteractionBlockNode(BaseOCBlockNode):
    """Presentation interaction block for hand interaction and pose-adjacent interaction cues."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "presentation_interaction"
    BLOCK_CATEGORY = "Pose"
    TOP_CATEGORY_NAMES = ("动作", "视角")
    ALLOWED_SUBCATEGORY_NAMES = (
        "手部动作",
        "人物动作",
    )


class OCPresentationExpressionBlockNode(BaseOCBlockNode):
    """Presentation expression block for emotional facial presentation."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "presentation_expression"
    BLOCK_CATEGORY = "Face"
    TOP_CATEGORY_NAMES = ("表情",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "笑",
        "哭",
        "不开心",
        "蔑视",
        "生气",
        "其他表情",
    )


class OCPresentationCameraBlockNode(BaseOCBlockNode):
    """Presentation camera block for framing, lens type, and camera angle selection."""

    DESCRIPTION = cleandoc(__doc__)
    BLOCK_KEY = "presentation_camera"
    BLOCK_CATEGORY = "Camera"
    TOP_CATEGORY_NAMES = ("视角",)
    ALLOWED_SUBCATEGORY_NAMES = (
        "镜头",
        "特写镜头",
        "镜头角度",
    )
