from pixel_font_knife import glyph_file_util

from tools.configs.font import FontConfig


def format_glyphs(font_config: FontConfig):
    context = glyph_file_util.load_context(font_config.glyphs_dir)
    glyph_file_util.normalize_context(context, font_config.glyphs_dir)
