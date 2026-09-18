import math
from collections.abc import Mapping, Sequence
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, Glyph
from pixel_font_knife.cmap.context import CmapContext
from pixel_font_knife.glyph.file import GlyphFile
from pixel_font_knife.named.file import NamedGlyphFile

from tools import configs
from tools.configs import options
from tools.configs.font import FontConfig


def collect_glyph_files(font_config: FontConfig) -> tuple[Sequence[GlyphFile], Mapping[int, str], Sequence[str]]:
    notdef_glyph_file = NamedGlyphFile.load_notdef(font_config.glyphs_dir.joinpath('notdef.png'))

    context = CmapContext.load(font_config.glyphs_dir.joinpath('cmap'))

    if font_config.fallback_lower_from_upper:
        for code_point in range(ord('A'), ord('Z') + 1):
            fallback_code_point = code_point + 32
            if code_point in context and fallback_code_point not in context:
                context[fallback_code_point] = context[code_point].copy()

    if font_config.fallback_upper_from_lower:
        for code_point in range(ord('a'), ord('z') + 1):
            fallback_code_point = code_point - 32
            if code_point in context and fallback_code_point not in context:
                context[fallback_code_point] = context[code_point].copy()

    glyph_sequence = [notdef_glyph_file] + context.get_glyph_sequence()
    character_mapping = context.get_character_mapping()
    alphabet = [chr(code_point) for code_point in sorted(character_mapping.keys())]
    return glyph_sequence, character_mapping, alphabet


def _create_builder(font_config: FontConfig, glyph_sequence: Sequence[GlyphFile], character_mapping: Mapping[int, str]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = math.ceil(font_config.line_height / 2)
    builder.font_metric.vertical_layout.descent = -math.floor(font_config.line_height / 2)
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = configs.VERSION
    builder.meta_info.created_time = datetime.fromisoformat(f'{configs.VERSION.replace('.', '-')}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'Retro Pixel {font_config.name}'
    builder.meta_info.weight_name = font_config.weight_name
    builder.meta_info.serif_style = font_config.serif_style
    builder.meta_info.slant_style = font_config.slant_style
    builder.meta_info.width_style = font_config.width_style
    builder.meta_info.manufacturer = 'TakWolf'
    builder.meta_info.designer = 'TakWolf'
    builder.meta_info.description = 'Open source retro style pixel font'
    builder.meta_info.copyright_info = 'Copyright (c) 2023, TakWolf (https://takwolf.com)'
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1'
    builder.meta_info.vendor_url = 'https://retro-pixel-font.takwolf.com'
    builder.meta_info.designer_url = 'https://takwolf.com'
    builder.meta_info.license_url = 'https://github.com/TakWolf/retro-pixel-font/blob/master/LICENSE-OFL'

    for glyph_file in glyph_sequence:
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=glyph_file.canvas.horizontal_offset_for_trimmed(font_config.font_size, font_config.baseline),
            advance_width=glyph_file.canvas.advance_width(),
            vertical_offset=glyph_file.canvas.vertical_offset_for_trimmed(font_config.font_size),
            advance_height=glyph_file.canvas.advance_height(font_config.font_size),
            bitmap=glyph_file.canvas.trimmed_bitmap.data,
        ))

    builder.character_mapping.update(character_mapping)

    return builder


def make_fonts(font_config: FontConfig, glyph_sequence: Sequence[GlyphFile], character_mapping: Mapping[int, str]) -> None:
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)

    builder = _create_builder(font_config, glyph_sequence, character_mapping)
    for font_format in options.FONT_FORMATS:
        file_path = font_config.outputs_dir.joinpath(f'retro-pixel-{font_config.outputs_name}.{font_format}')
        getattr(builder, f'save_{font_format.replace('.', '_')}')(file_path)
        logger.info("Make font: '{}'", file_path)
