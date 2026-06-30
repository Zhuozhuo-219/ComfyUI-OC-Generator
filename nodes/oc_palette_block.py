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
from .oc_data import get_color_catalog
from .oc_types import OC_PALETTE_TYPE


PALETTE_STYLES = ["balanced", "monochrome", "high_contrast", "warm", "cool"]
NONE_COLOR = "__none__"

STYLE_PRESETS = {
    "balanced": [
        {"primary": ["black", "white"], "secondary": "gray", "accent": "red", "neutral": "silver"},
        {"primary": ["navy", "white"], "secondary": "gray", "accent": "gold", "neutral": "black"},
        {"primary": ["brown", "beige"], "secondary": "ivory", "accent": "forestgreen", "neutral": "tan"},
    ],
    "monochrome": [
        {"primary": ["black", "darkgray", "gray"], "secondary": "whitesmoke", "accent": "silver", "neutral": "gray"},
        {"primary": ["white", "lightgray"], "secondary": "gray", "accent": "silver", "neutral": "black"},
        {"primary": ["navy", "slateblue"], "secondary": "lightsteelblue", "accent": "white", "neutral": "gray"},
    ],
    "high_contrast": [
        {"primary": ["black"], "secondary": "white", "accent": "red", "neutral": "gray"},
        {"primary": ["navy"], "secondary": "white", "accent": "gold", "neutral": "gray"},
        {"primary": ["purple"], "secondary": "black", "accent": "gold", "neutral": "silver"},
    ],
    "warm": [
        {"primary": ["brown", "sienna"], "secondary": "beige", "accent": "orange", "neutral": "ivory"},
        {"primary": ["red", "darkred"], "secondary": "black", "accent": "gold", "neutral": "gray"},
        {"primary": ["salmon", "pink"], "secondary": "white", "accent": "coral", "neutral": "beige"},
    ],
    "cool": [
        {"primary": ["blue", "navy"], "secondary": "white", "accent": "cyan", "neutral": "gray"},
        {"primary": ["teal", "darkcyan"], "secondary": "black", "accent": "silver", "neutral": "gray"},
        {"primary": ["forestgreen", "green"], "secondary": "black", "accent": "yellowgreen", "neutral": "beige"},
    ],
}


def _color_choices() -> list[str]:
    catalog = get_color_catalog()
    colors = [option.prompt for option in catalog.options]
    deduped = list(dict.fromkeys(colors))
    return [NONE_COLOR, *deduped]


def _normalize_color(value: str) -> str | None:
    if not value or value == NONE_COLOR:
        return None
    return value.strip() or None


def _unique_colors(values: list[str | None]) -> list[str]:
    result = []
    seen = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


class OCPaletteBlockNode(ComfyNodeABC):
    """Generate a reusable outfit palette so multiple clothing parts stay within one coordinated color system."""

    DESCRIPTION = cleandoc(__doc__)
    CATEGORY = "OC Generator/Character"
    FUNCTION = "build_palette"
    RETURN_TYPES = (OC_PALETTE_TYPE, IO.STRING, IO.STRING)
    RETURN_NAMES = ("palette", "palette_preview", "debug_text")
    OUTPUT_TOOLTIPS = (
        "Structured palette data for Character Outfit Block.",
        "Short readable palette summary.",
        "Debug details about the palette selection process.",
    )

    @classmethod
    def INPUT_TYPES(cls):
        color_choices = _color_choices()
        return {
            "required": {
                "mode": (
                    ["fixed", "randomize"],
                    {
                        "default": "fixed",
                        "tooltip": "fixed uses the manually selected colors. randomize selects a palette preset from the chosen palette style.",
                    },
                ),
                "palette_style": (
                    PALETTE_STYLES,
                    {
                        "default": "balanced",
                        "tooltip": "Palette family used by randomize mode and as a semantic description of the palette.",
                    },
                ),
                "primary_1": (
                    color_choices,
                    {
                        "default": "black",
                        "tooltip": "First primary color. The palette may use up to three primary colors.",
                    },
                ),
                "primary_2": (
                    color_choices,
                    {
                        "default": NONE_COLOR,
                        "tooltip": "Optional second primary color.",
                    },
                ),
                "primary_3": (
                    color_choices,
                    {
                        "default": NONE_COLOR,
                        "tooltip": "Optional third primary color.",
                    },
                ),
                "secondary": (
                    color_choices,
                    {
                        "default": "white",
                        "tooltip": "Secondary color for contrast or layering.",
                    },
                ),
                "accent": (
                    color_choices,
                    {
                        "default": "red",
                        "tooltip": "Accent color for smaller emphasis areas.",
                    },
                ),
                "neutral": (
                    color_choices,
                    {
                        "default": "gray",
                        "tooltip": "Neutral support color for subtle parts like socks or shoes.",
                    },
                ),
                "seed": (
                    IO.INT,
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFF,
                        "tooltip": "Seed used when randomize mode selects a preset inside the chosen palette style.",
                    },
                ),
            }
        }

    def build_palette(self, mode, palette_style, primary_1, primary_2, primary_3, secondary, accent, neutral, seed):
        if mode == "randomize":
            presets = STYLE_PRESETS[palette_style]
            preset_index = stable_seed("palette", palette_style, seed) % len(presets)
            preset = presets[preset_index]
            primary_colors = preset["primary"]
            secondary_color = preset["secondary"]
            accent_color = preset["accent"]
            neutral_color = preset["neutral"]
            debug_text = f"Palette: randomize [{palette_style}] preset={preset_index}"
        else:
            primary_colors = _unique_colors(
                [
                    _normalize_color(primary_1),
                    _normalize_color(primary_2),
                    _normalize_color(primary_3),
                ]
            )
            secondary_color = _normalize_color(secondary) or "white"
            accent_color = _normalize_color(accent) or "red"
            neutral_color = _normalize_color(neutral) or "gray"
            debug_text = f"Palette: fixed [{palette_style}]"

        if not primary_colors:
            primary_colors = ["black"]

        palette = {
            "palette_type": "oc_palette",
            "style": palette_style,
            "mode": mode,
            "primary": primary_colors,
            "secondary": secondary_color,
            "accent": accent_color,
            "neutral": neutral_color,
        }
        preview = (
            f"primary={'+'.join(primary_colors)}, "
            f"secondary={secondary_color}, accent={accent_color}, neutral={neutral_color}"
        )
        return (palette, preview, debug_text)
