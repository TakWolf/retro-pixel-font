from io import BytesIO

import unidata_blocks
from pixel_font_knife import glyph_file_util

from tools.configs.font import FontConfig


def check_glyph_files(font_config: FontConfig):
    context = glyph_file_util.load_context(font_config.glyphs_dir)
    for code_point, flavor_group in context.items():
        glyph_file = flavor_group.get_file()

        if code_point == -1:
            file_name = 'notdef.png'
            file_dir = font_config.glyphs_dir
        else:
            file_name = f'{code_point:04X}.png'
            block = unidata_blocks.get_block_by_code_point(code_point)
            file_dir = font_config.glyphs_dir.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')
        file_path = file_dir.joinpath(file_name)

        assert glyph_file.file_path == file_path, f"[{font_config.outputs_name}] Glyph file path is not standardized: '{glyph_file.file_path}' -> '{file_path}'"

        assert glyph_file.height == font_config.line_height, f"[{font_config.outputs_name}] Glyph data error: '{glyph_file.file_path}'"

        glyph_bytes = BytesIO()
        glyph_file.bitmap.dump_png(glyph_bytes)
        assert glyph_file.file_path.read_bytes() == glyph_bytes.getvalue(), f"[{font_config.outputs_name}] Glyph file data is not standardized: '{glyph_file.file_path}'"
