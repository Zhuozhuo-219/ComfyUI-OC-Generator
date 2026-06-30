from __future__ import annotations

from inspect import cleandoc

from .oc_part_base import BaseOCPartNode


class OCOutfitStylePartNode(BaseOCPartNode):
    """Outfit base style part node for high-level clothing style selection."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_style"
    PART_SLOT = "base_style"
    PART_CATEGORY = "Outfit Style"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("正装", "风格", "休闲服", "运动服", "泳装", "制服", "盔甲")


class OCOutfitUpperPartNode(BaseOCPartNode):
    """Outfit upper part node for top garments."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_upper"
    PART_SLOT = "upper"
    PART_CATEGORY = "Outfit Upper"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("上衣",)


class OCOutfitOuterPartNode(BaseOCPartNode):
    """Outfit outer part node for coats and jackets."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_outer"
    PART_SLOT = "outer"
    PART_CATEGORY = "Outfit Outer"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("外套",)


class OCOutfitPantsPartNode(BaseOCPartNode):
    """Outfit lower part node for pants."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_pants"
    PART_SLOT = "lower"
    PART_CATEGORY = "Outfit Pants"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("裤子",)


class OCOutfitSkirtPartNode(BaseOCPartNode):
    """Outfit lower part node for skirts."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_skirt"
    PART_SLOT = "lower"
    PART_CATEGORY = "Outfit Skirt"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("裙子",)


class OCOutfitLegwearPartNode(BaseOCPartNode):
    """Outfit legwear part node for socks and stockings."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_legwear"
    PART_SLOT = "legwear"
    PART_CATEGORY = "Outfit Legwear"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("袜子",)


class OCOutfitFootwearPartNode(BaseOCPartNode):
    """Outfit footwear part node for shoes and boots."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_footwear"
    PART_SLOT = "footwear"
    PART_CATEGORY = "Outfit Footwear"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("鞋子",)


class OCOutfitHeadwearPartNode(BaseOCPartNode):
    """Outfit headwear part node for hats and head accessories."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_headwear"
    PART_SLOT = "headwear"
    PART_CATEGORY = "Outfit Headwear"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("帽子", "头饰", "发饰")


class OCOutfitFacewearPartNode(BaseOCPartNode):
    """Outfit facewear part node for glasses and masks."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_facewear"
    PART_SLOT = "facewear"
    PART_CATEGORY = "Outfit Facewear"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("面部饰品",)


class OCOutfitJewelryPartNode(BaseOCPartNode):
    """Outfit jewelry part node for earrings and jewelry pieces."""

    DESCRIPTION = cleandoc(__doc__)
    PART_KIND = "outfit_jewelry"
    PART_SLOT = "jewelry"
    PART_CATEGORY = "Outfit Jewelry"
    TOP_CATEGORY_NAMES = ("服饰",)
    ALLOWED_SUBCATEGORY_NAMES = ("耳饰", "首饰")
