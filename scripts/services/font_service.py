import logging
import math
import shutil
from pathlib import Path

import unidata_blocks
from pixel_font_builder import FontBuilder, Glyph
from pixel_font_builder.opentype import Flavor

from scripts import configs
from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util, bitmap_util

logger = logging.getLogger('font_service')


class GlyphFile:
    @staticmethod
    def load(file_path: Path) -> 'GlyphFile':
        hex_name = file_path.stem
        if hex_name == 'notdef':
            code_point = -1
        else:
            code_point = int(hex_name, 16)
        return GlyphFile(file_path, code_point)

    file_path: Path
    code_point: int
    bitmap: list[list[int]]
    width: int
    height: int

    def __init__(self, file_path: Path, code_point: int):
        self.file_path = file_path
        self.code_point = code_point
        self.bitmap, self.width, self.height = bitmap_util.load_png(file_path)

    @property
    def glyph_name(self) -> str:
        if self.code_point == -1:
            return '.notdef'
        else:
            return f'uni{self.code_point:04X}'


def collect_glyph_files(font_config: FontConfig) -> tuple[list[str], dict[int, str], list[GlyphFile]]:
    registry = {}
    root_dir = path_define.glyphs_dir.joinpath(font_config.outputs_name)
    for file_dir, _, file_names in root_dir.walk():
        for file_name in file_names:
            if not file_name.endswith('.png'):
                continue
            file_path = file_dir.joinpath(file_name)
            glyph_file = GlyphFile.load(file_path)
            registry[glyph_file.code_point] = glyph_file

    character_mapping = {}
    glyph_files = []
    for glyph_file in registry.values():
        if glyph_file.code_point != -1:
            character_mapping[glyph_file.code_point] = glyph_file.glyph_name
        glyph_files.append(glyph_file)
    glyph_files.sort(key=lambda x: x.code_point)

    if font_config.fallback_lower_from_upper:
        for code_point in range(ord('A'), ord('Z') + 1):
            fallback_code_point = code_point + 32
            if code_point in character_mapping and fallback_code_point not in character_mapping:
                character_mapping[fallback_code_point] = character_mapping[code_point]

    if font_config.fallback_upper_from_lower:
        for code_point in range(ord('a'), ord('z') + 1):
            fallback_code_point = code_point - 32
            if code_point in character_mapping and fallback_code_point not in character_mapping:
                character_mapping[fallback_code_point] = character_mapping[code_point]

    alphabet = [chr(code_point) for code_point in character_mapping]
    alphabet.sort()

    return alphabet, character_mapping, glyph_files


def format_glyph_files(font_config: FontConfig, glyph_files: list[GlyphFile]):
    root_dir = path_define.glyphs_dir.joinpath(font_config.outputs_name)
    for glyph_file in glyph_files:
        assert glyph_file.height == font_config.line_height, f"Glyph data error: '{glyph_file.file_path}'"
        bitmap_util.save_png(glyph_file.bitmap, glyph_file.file_path)

        if glyph_file.code_point == -1:
            file_name = 'notdef.png'
            file_dir = root_dir
        else:
            file_name = f'{glyph_file.code_point:04X}.png'
            block = unidata_blocks.get_block_by_code_point(glyph_file.code_point)
            file_dir = root_dir.joinpath(f'{block.code_start:04X}-{block.code_end:04X} {block.name}')

        file_path = file_dir.joinpath(file_name)
        if glyph_file.file_path != file_path:
            assert not file_path.exists(), f"Glyph file duplication: '{glyph_file.file_path}' -> '{file_path}'"
            file_dir.mkdir(parents=True, exist_ok=True)
            glyph_file.file_path.rename(file_path)
            glyph_file.file_path = file_path
            logger.info(f"Standardize glyph file path: '{glyph_file.file_path}'")

    for file_dir, _, _ in root_dir.walk(top_down=False):
        if fs_util.is_empty_dir(file_dir):
            shutil.rmtree(file_dir)


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_files: list[GlyphFile]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = math.ceil(font_config.line_height / 2)
    builder.font_metric.vertical_layout.descent = math.floor(font_config.line_height / 2)
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = configs.font_version
    builder.meta_info.created_time = configs.font_version_time
    builder.meta_info.modified_time = configs.font_version_time
    builder.meta_info.family_name = f'Retro Pixel {font_config.name}'
    builder.meta_info.weight_name = font_config.weight_name
    builder.meta_info.serif_style = font_config.serif_style
    builder.meta_info.slant_style = font_config.slant_style
    builder.meta_info.width_mode = font_config.width_mode
    builder.meta_info.manufacturer = 'TakWolf'
    builder.meta_info.designer = 'TakWolf'
    builder.meta_info.description = 'Open source retro style pixel font.'
    builder.meta_info.copyright_info = f"Copyright (c) 2023, TakWolf (https://takwolf.com), with Reserved Font Name 'Retro Pixel {font_config.name}'."
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    builder.meta_info.vendor_url = 'https://retro-pixel-font.takwolf.com'
    builder.meta_info.designer_url = 'https://takwolf.com'
    builder.meta_info.license_url = 'https://openfontlicense.org'

    builder.character_mapping.update(character_mapping)

    for glyph_file in glyph_files:
        horizontal_origin_y = math.floor((font_config.ascent + font_config.descent - glyph_file.height) / 2)
        vertical_origin_y = (font_config.font_size - glyph_file.height) // 2
        builder.glyphs.append(Glyph(
            name=glyph_file.glyph_name,
            advance_width=glyph_file.width,
            advance_height=font_config.font_size,
            horizontal_origin=(0, horizontal_origin_y),
            vertical_origin_y=vertical_origin_y,
            bitmap=glyph_file.bitmap,
        ))

    return builder


def make_fonts(font_config: FontConfig, character_mapping: dict[int, str], glyph_files: list[GlyphFile]):
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)

    builder = _create_builder(font_config, character_mapping, glyph_files)
    for font_format in configs.font_formats:
        file_path = font_config.outputs_dir.joinpath(f'retro-pixel-{font_config.outputs_name}.{font_format}')
        if font_format == 'woff2':
            builder.save_otf(file_path, flavor=Flavor.WOFF2)
        else:
            getattr(builder, f'save_{font_format}')(file_path)
        logger.info("Make font: '%s'", file_path)
