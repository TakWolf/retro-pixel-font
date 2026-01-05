import math
from datetime import datetime

from loguru import logger
from pixel_font_builder import FontBuilder, Glyph, opentype
from pixel_font_knife import glyph_file_util
from pixel_font_knife.glyph_file_util import GlyphFile

from tools import configs
from tools.configs import options
from tools.configs.font import FontConfig


def collect_glyph_files(font_config: FontConfig) -> tuple[list[GlyphFile], dict[int, str], set[str]]:
    context = glyph_file_util.load_context(font_config.glyphs_dir)

    if font_config.fallback_lower_from_upper:
        for code_point in range(ord('A'), ord('Z') + 1):
            fallback_code_point = code_point + 32
            if code_point in context and fallback_code_point not in context:
                context[fallback_code_point] = context[code_point]

    if font_config.fallback_upper_from_lower:
        for code_point in range(ord('a'), ord('z') + 1):
            fallback_code_point = code_point - 32
            if code_point in context and fallback_code_point not in context:
                context[fallback_code_point] = context[code_point]

    glyph_sequence = glyph_file_util.get_glyph_sequence(context)
    character_mapping = glyph_file_util.get_character_mapping(context)
    alphabet = {chr(code_point) for code_point in context if code_point >= 0}
    return glyph_sequence, character_mapping, alphabet


def _create_builder(font_config: FontConfig, glyph_sequence: list[GlyphFile], character_mapping: dict[int, str]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = math.ceil(font_config.line_height / 2)
    builder.font_metric.vertical_layout.descent = -math.floor(font_config.line_height / 2)
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = configs.version
    builder.meta_info.created_time = datetime.fromisoformat(f'{configs.version.replace('.', '-')}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'Retro Pixel {font_config.name}'
    builder.meta_info.weight_name = font_config.weight_name
    builder.meta_info.serif_style = font_config.serif_style
    builder.meta_info.slant_style = font_config.slant_style
    builder.meta_info.width_style = font_config.width_style
    builder.meta_info.manufacturer = 'TakWolf'
    builder.meta_info.designer = 'TakWolf'
    builder.meta_info.description = 'Open source retro style pixel font'
    builder.meta_info.copyright_info = 'Copyright (c) 2023, TakWolf (https://takwolf.com), with Reserved Font Name "Retro Pixel"'
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1'
    builder.meta_info.vendor_url = 'https://retro-pixel-font.takwolf.com'
    builder.meta_info.designer_url = 'https://takwolf.com'
    builder.meta_info.license_url = 'https://github.com/TakWolf/retro-pixel-font/blob/master/LICENSE-OFL'

    for glyph_file in glyph_sequence:
        horizontal_offset_x = 0
        horizontal_offset_y = (font_config.ascent + font_config.descent - glyph_file.height) // 2
        vertical_offset_x = -math.ceil(glyph_file.width / 2)
        vertical_offset_y = (font_config.font_size - glyph_file.height) // 2
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            horizontal_offset=(horizontal_offset_x, horizontal_offset_y),
            advance_width=glyph_file.width,
            vertical_offset=(vertical_offset_x, vertical_offset_y),
            advance_height=font_config.font_size,
            bitmap=glyph_file.bitmap.data,
        ))

    builder.character_mapping.update(character_mapping)

    return builder


def make_fonts(font_config: FontConfig, glyph_sequence: list[GlyphFile], character_mapping: dict[int, str]):
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)

    builder = _create_builder(font_config, glyph_sequence, character_mapping)
    for font_format in options.font_formats:
        file_path = font_config.outputs_dir.joinpath(f'retro-pixel-{font_config.outputs_name}.{font_format}')
        match font_format:
            case 'otf.woff':
                builder.save_otf(file_path, flavor=opentype.Flavor.WOFF)
            case 'otf.woff2':
                builder.save_otf(file_path, flavor=opentype.Flavor.WOFF2)
            case 'ttf.woff':
                builder.save_ttf(file_path, flavor=opentype.Flavor.WOFF)
            case 'ttf.woff2':
                builder.save_ttf(file_path, flavor=opentype.Flavor.WOFF2)
            case _:
                getattr(builder, f'save_{font_format}')(file_path)
        logger.info("Make font: '{}'", file_path)
