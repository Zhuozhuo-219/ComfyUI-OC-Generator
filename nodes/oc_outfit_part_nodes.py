from __future__ import annotations

from inspect import cleandoc

from .oc_part_base import BaseOCPartNode
from .oc_types import (
    OUTFIT_DECORATION_PART_TYPE,
    OUTFIT_FACEWEAR_PART_TYPE,
    OUTFIT_FOOTWEAR_PART_TYPE,
    OUTFIT_HANDWEAR_PART_TYPE,
    OUTFIT_HEADWEAR_PART_TYPE,
    OUTFIT_JEWELRY_PART_TYPE,
    OUTFIT_LEGWEAR_PART_TYPE,
    OUTFIT_LOWER_PART_TYPE,
    OUTFIT_NECKWEAR_PART_TYPE,
    OUTFIT_OUTER_PART_TYPE,
    OUTFIT_STYLE_PART_TYPE,
    OUTFIT_UPPER_PART_TYPE,
    OUTFIT_WAIST_PART_TYPE,
)


class OCOutfitStylePartNode(BaseOCPartNode):
    """Outfit base style part node for high-level clothing style selection."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_style"
    PART_SLOT = "base_style"
    PART_CATEGORY = "Outfit Style"
    PART_OUTPUT_TYPE = OUTFIT_STYLE_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("正装", "风格", "休闲服", "运动服", "泳装", "制服", "盔甲")


class OCOutfitUpperPartNode(BaseOCPartNode):
    """Outfit upper part node for top garments."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_upper"
    PART_SLOT = "upper"
    PART_CATEGORY = "Outfit Upper"
    PART_OUTPUT_TYPE = OUTFIT_UPPER_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("上衣",)


class OCOutfitOuterPartNode(BaseOCPartNode):
    """Outfit outer part node for coats and jackets."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_outer"
    PART_SLOT = "outer"
    PART_CATEGORY = "Outfit Outer"
    PART_OUTPUT_TYPE = OUTFIT_OUTER_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("外套",)


class OCOutfitPantsPartNode(BaseOCPartNode):
    """Outfit lower part node for pants."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_pants"
    PART_SLOT = "lower"
    PART_CATEGORY = "Outfit Pants"
    PART_OUTPUT_TYPE = OUTFIT_LOWER_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("裤子",)


class OCOutfitSkirtPartNode(BaseOCPartNode):
    """Outfit lower part node for skirts."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_skirt"
    PART_SLOT = "lower"
    PART_CATEGORY = "Outfit Skirt"
    PART_OUTPUT_TYPE = OUTFIT_LOWER_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("裙子",)


class OCOutfitLegwearPartNode(BaseOCPartNode):
    """Outfit legwear part node for socks and stockings."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_legwear"
    PART_SLOT = "legwear"
    PART_CATEGORY = "Outfit Legwear"
    PART_OUTPUT_TYPE = OUTFIT_LEGWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("袜子",)


class OCOutfitFootwearPartNode(BaseOCPartNode):
    """Outfit footwear part node for shoes and boots."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_footwear"
    PART_SLOT = "footwear"
    PART_CATEGORY = "Outfit Footwear"
    PART_OUTPUT_TYPE = OUTFIT_FOOTWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("鞋子",)


class OCOutfitNeckwearPartNode(BaseOCPartNode):
    """Outfit neckwear part node for scarves and collar accessories."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_neckwear"
    PART_SLOT = "neckwear"
    PART_CATEGORY = "Outfit Neckwear"
    PART_OUTPUT_TYPE = OUTFIT_NECKWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("领口",)


class OCOutfitHandwearPartNode(BaseOCPartNode):
    """Outfit handwear part node for gloves and arm or wrist wearables."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_handwear"
    PART_SLOT = "handwear"
    PART_CATEGORY = "Outfit Handwear"
    PART_OUTPUT_TYPE = OUTFIT_HANDWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("手部",)


class OCOutfitWaistPartNode(BaseOCPartNode):
    """Outfit waist part node for belts and waist accessories."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_waist"
    PART_SLOT = "waist"
    PART_CATEGORY = "Outfit Waist"
    PART_OUTPUT_TYPE = OUTFIT_WAIST_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("腰部",)


class OCOutfitHeadwearPartNode(BaseOCPartNode):
    """Outfit headwear part node for hats and head accessories."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_headwear"
    PART_SLOT = "headwear"
    PART_CATEGORY = "Outfit Headwear"
    PART_OUTPUT_TYPE = OUTFIT_HEADWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("帽子", "头饰", "发饰")


class OCOutfitFacewearPartNode(BaseOCPartNode):
    """Outfit facewear part node for glasses and masks."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_facewear"
    PART_SLOT = "facewear"
    PART_CATEGORY = "Outfit Facewear"
    PART_OUTPUT_TYPE = OUTFIT_FACEWEAR_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("面部饰品",)


class OCOutfitJewelryPartNode(BaseOCPartNode):
    """Outfit jewelry part node for earrings and jewelry pieces."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_jewelry"
    PART_SLOT = "jewelry"
    PART_CATEGORY = "Outfit Jewelry"
    PART_OUTPUT_TYPE = OUTFIT_JEWELRY_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("耳饰", "首饰")


class OCOutfitDecorationPartNode(BaseOCPartNode):
    """Outfit decoration part node for decorative clothing details."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_decoration"
    PART_SLOT = "decoration"
    PART_CATEGORY = "Outfit Decoration"
    PART_OUTPUT_TYPE = OUTFIT_DECORATION_PART_TYPE
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("装饰", "其他")
