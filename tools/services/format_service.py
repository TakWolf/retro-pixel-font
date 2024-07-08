import shutil
from pathlib import Path

import unidata_blocks
from loguru import logger
from pixel_font_knife import glyph_file_util

from tools.configs.font import FontConfig


def _is_empty_dir(path: Path) -> bool:
    for item_path in path.iterdir():
        if item_path.name == '.DS_Store':
            continue
        return False
    return True


def format_glyph_files(font_config: FontConfig):
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

        if glyph_file.file_path != file_path:
            assert not file_path.exists(), f"[{font_config.outputs_name}] Glyph file duplication: '{glyph_file.file_path}' -> '{file_path}'"
            file_dir.mkdir(parents=True, exist_ok=True)
            glyph_file.file_path.rename(file_path)
            logger.info("Format glyph file path: '{}' -> '{}'", glyph_file.file_path, file_path)
            glyph_file.file_path = file_path

        glyph_file.bitmap.save_png(glyph_file.file_path)

    for file_dir, _, _ in font_config.glyphs_dir.walk(top_down=False):
        if _is_empty_dir(file_dir):
            shutil.rmtree(file_dir)
