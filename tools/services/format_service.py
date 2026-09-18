import sys

from pixel_font_knife.cmap.context import CmapContext
from pixel_font_knife.utils import fs_util

from tools.configs.font import FontConfig


def normalize_cmap_glyphs(font_config: FontConfig) -> None:
    glyphs_dir = font_config.glyphs_dir.joinpath('cmap')
    context = CmapContext.load(glyphs_dir)
    context.normalize(glyphs_dir)


def format_glyphs(font_config: FontConfig) -> None:
    if sys.platform != 'win32':
        fs_util.format_glyph_files(font_config.glyphs_dir)
