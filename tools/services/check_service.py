from pixel_font_knife import glyph_file_util

from tools.configs.font import FontConfig


def check_glyph_files(font_config: FontConfig):
    context = glyph_file_util.load_context(font_config.glyphs_dir)
    for code_point, flavor_group in context.items():
        for glyph_file in set(flavor_group.values()):
            assert glyph_file.height == font_config.line_height, f"[{font_config.outputs_name}] glyph bitmap size error: '{glyph_file.file_path}'"
