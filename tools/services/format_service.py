import shutil
from pathlib import Path

from pixel_font_knife import glyph_file_util

from tools.configs.font import FontConfig


def _is_empty_dir(path: Path) -> bool:
    for item_path in path.iterdir():
        if item_path.name == '.DS_Store':
            continue
        return False
    return True


def format_glyphs(font_config: FontConfig):
    context = glyph_file_util.load_context(font_config.glyphs_dir)
    glyph_file_util.normalize_context(context, font_config.glyphs_dir)

    for file_dir, _, _ in font_config.glyphs_dir.walk(top_down=False):
        if _is_empty_dir(file_dir):
            shutil.rmtree(file_dir)
