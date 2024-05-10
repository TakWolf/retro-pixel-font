import logging
import math
import os

import unidata_blocks
from pixel_font_builder import FontBuilder, Glyph
from pixel_font_builder.opentype import Flavor

from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util, bitmap_util

logger = logging.getLogger('font_service')


class GlyphFile:
    @staticmethod
    def load(file_path: str) -> 'GlyphFile':
        hex_name = os.path.basename(file_path).removesuffix('.png')
        if hex_name == 'notdef':
            code_point = -1
        else:
            code_point = int(hex_name, 16)
        return GlyphFile(file_path, code_point)

    def __init__(self, file_path: str, code_point: int):
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
    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)
    for file_dir, _, file_names in os.walk(root_dir):
        for file_name in file_names:
            if not file_name.endswith('.png'):
                continue
            file_path = os.path.join(file_dir, file_name)
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
    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)
    for glyph_file in glyph_files:
        assert glyph_file.height == font_config.line_height, f"Glyph data error: '{glyph_file.file_path}'"
        bitmap_util.save_png(glyph_file.bitmap, glyph_file.file_path)

        if glyph_file.code_point == -1:
            file_name = 'notdef.png'
            file_dir = root_dir
        else:
            file_name = f'{glyph_file.code_point:04X}.png'
            block = unidata_blocks.get_block_by_code_point(glyph_file.code_point)
            file_dir = os.path.join(root_dir, f'{block.code_start:04X}-{block.code_end:04X} {block.name}')

        file_path = os.path.join(file_dir, file_name)
        if glyph_file.file_path != file_path:
            assert not os.path.exists(file_path), f"Glyph file duplication: '{glyph_file.file_path}' -> '{file_path}'"
            fs_util.make_dir(file_dir)
            os.rename(glyph_file.file_path, file_path)
            glyph_file.file_path = file_path
            logger.info(f"Standardize glyph file path: '{glyph_file.file_path}'")

    for file_dir, _, _ in os.walk(root_dir, topdown=False):
        file_names = os.listdir(file_dir)
        if '.DS_Store' in file_names:
            file_names.remove('.DS_Store')
        if len(file_names) == 0:
            fs_util.delete_dir(file_dir)


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_files: list[GlyphFile]) -> FontBuilder:
    builder = FontBuilder()
    builder.font_metric.font_size = font_config.font_size
    builder.font_metric.horizontal_layout.ascent = font_config.ascent
    builder.font_metric.horizontal_layout.descent = font_config.descent
    builder.font_metric.vertical_layout.ascent = math.ceil(font_config.line_height / 2)
    builder.font_metric.vertical_layout.descent = math.floor(font_config.line_height / 2)
    builder.font_metric.x_height = font_config.x_height
    builder.font_metric.cap_height = font_config.cap_height

    builder.meta_info.version = FontConfig.VERSION
    builder.meta_info.created_time = FontConfig.VERSION_TIME
    builder.meta_info.modified_time = FontConfig.VERSION_TIME
    builder.meta_info.family_name = font_config.family_name
    builder.meta_info.weight_name = font_config.weight_name
    builder.meta_info.serif_style = font_config.serif_style
    builder.meta_info.slant_style = font_config.slant_style
    builder.meta_info.width_mode = font_config.width_mode
    builder.meta_info.manufacturer = FontConfig.MANUFACTURER
    builder.meta_info.designer = FontConfig.DESIGNER
    builder.meta_info.description = font_config.description
    builder.meta_info.copyright_info = font_config.copyright_info
    builder.meta_info.license_info = FontConfig.LICENSE_INFO
    builder.meta_info.vendor_url = FontConfig.VENDOR_URL
    builder.meta_info.designer_url = FontConfig.DESIGNER_URL
    builder.meta_info.license_url = FontConfig.LICENSE_URL

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


def make_font_files(font_config: FontConfig, character_mapping: dict[int, str], glyph_files: list[GlyphFile]):
    fs_util.make_dir(font_config.outputs_dir)

    builder = _create_builder(font_config, character_mapping, glyph_files)

    otf_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_outputs_name}.otf')
    builder.save_otf(otf_file_path)
    logger.info("Make font file: '%s'", otf_file_path)

    woff2_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_outputs_name}.woff2')
    builder.save_otf(woff2_file_path, flavor=Flavor.WOFF2)
    logger.info("Make font file: '%s'", woff2_file_path)

    ttf_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_outputs_name}.ttf')
    builder.save_ttf(ttf_file_path)
    logger.info("Make font file: '%s'", ttf_file_path)

    bdf_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_outputs_name}.bdf')
    builder.save_bdf(bdf_file_path)
    logger.info("Make font file: '%s'", bdf_file_path)

    pcf_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_outputs_name}.pcf')
    builder.save_pcf(pcf_file_path)
    logger.info("Make font file: '%s'", pcf_file_path)
