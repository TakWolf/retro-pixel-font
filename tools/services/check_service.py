from pixel_font_knife.cmap.context import CmapContext

from tools.configs.font import FontConfig


def check_cmap_glyphs(font_config: FontConfig) -> None:
    context = CmapContext.load(font_config.glyphs_dir.joinpath('cmap'))
    for code_point, glyph_variants in context.items():
        for glyph_file in set(glyph_variants.values()):
            assert glyph_file.canvas.height == font_config.line_height, f"[{font_config.outputs_name}] glyph bitmap dimensions error: '{glyph_file.file_path}'"
