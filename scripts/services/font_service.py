import logging
import math
import os

import unidata_blocks
from pixel_font_builder import FontBuilder, Glyph
from pixel_font_builder.opentype import Flavor

from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util, glyph_util

logger = logging.getLogger('font-service')


def format_glyph_files(font_config: FontConfig):
    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)
    for file_from_dir, _, file_names in list(os.walk(root_dir, topdown=False)):
        for file_name in file_names:
            if not file_name.endswith('.png'):
                continue
            file_from_path = os.path.join(file_from_dir, file_name)
            if file_name == 'notdef.png':
                file_to_dir = root_dir
            else:
                code_point = int(file_name.removesuffix('.png'), 16)
                file_name = f'{code_point:04X}.png'
                block = unidata_blocks.get_block_by_code_point(code_point)
                block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
                file_to_dir = os.path.join(root_dir, block_dir_name)
            file_to_path = os.path.join(file_to_dir, file_name)

            glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(file_from_path)
            assert (glyph_height - font_config.size) % 2 == 0, f"Incorrect glyph data: '{file_from_path}'"
            if glyph_height > font_config.line_height:
                for i in range((glyph_height - font_config.line_height) // 2):
                    glyph_data.pop(0)
                    glyph_data.pop()
            elif glyph_height < font_config.line_height:
                for i in range((font_config.line_height - glyph_height) // 2):
                    glyph_data.insert(0, [0 for _ in range(glyph_width)])
                    glyph_data.append([0 for _ in range(glyph_width)])

            if file_to_path != file_from_path:
                assert not os.path.exists(file_to_path), f"Glyph file duplication: '{file_from_path}'"
                fs_util.make_dirs(file_to_dir)
                os.remove(file_from_path)
            glyph_util.save_glyph_data_to_png(glyph_data, file_to_path)
            logger.info("Format glyph file: '%s'", file_to_path)

        entry_names = os.listdir(file_from_dir)
        if '.DS_Store' in entry_names:
            os.remove(os.path.join(file_from_dir, '.DS_Store'))
            entry_names.remove('.DS_Store')
        if len(entry_names) == 0:
            os.rmdir(file_from_dir)


def collect_glyph_files(font_config: FontConfig) -> tuple[list[str], dict[int, str], list[tuple[str, str]]]:
    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)

    registry = {}
    for file_dir, _, file_names in os.walk(root_dir):
        for file_name in file_names:
            if not file_name.endswith('.png'):
                continue
            file_path = os.path.join(file_dir, file_name)
            if file_name == 'notdef.png':
                code_point = -1
            else:
                code_point = int(file_name.removesuffix('.png'), 16)
            registry[code_point] = file_path

    sequence = list(registry.keys())
    sequence.sort()

    character_mapping = {}
    glyph_file_infos = []
    for code_point in sequence:
        if code_point == -1:
            glyph_name = '.notdef'
        else:
            glyph_name = f'uni{code_point:04X}'
            character_mapping[code_point] = glyph_name
        glyph_file_infos.append((glyph_name, registry[code_point]))

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

    return alphabet, character_mapping, glyph_file_infos


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_infos: list[tuple[str, str]]) -> FontBuilder:
    builder = FontBuilder(font_config.size)

    builder.meta_infos.version = FontConfig.VERSION
    builder.meta_infos.family_name = font_config.family_name
    builder.meta_infos.style_name = font_config.style_name
    builder.meta_infos.serif_mode = font_config.serif_mode
    builder.meta_infos.width_mode = font_config.width_mode
    builder.meta_infos.manufacturer = FontConfig.MANUFACTURER
    builder.meta_infos.designer = FontConfig.DESIGNER
    builder.meta_infos.description = font_config.description
    builder.meta_infos.copyright_info = font_config.copyright_info
    builder.meta_infos.license_info = FontConfig.LICENSE_INFO
    builder.meta_infos.vendor_url = FontConfig.VENDOR_URL
    builder.meta_infos.designer_url = FontConfig.DESIGNER_URL
    builder.meta_infos.license_url = FontConfig.LICENSE_URL

    builder.horizontal_header.ascent = font_config.ascent
    builder.horizontal_header.descent = font_config.descent

    builder.vertical_header.ascent = font_config.ascent
    builder.vertical_header.descent = font_config.descent

    builder.properties.x_height = font_config.x_height
    builder.properties.cap_height = font_config.cap_height

    builder.character_mapping.update(character_mapping)

    for glyph_name, file_path in glyph_file_infos:
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(file_path)
        horizontal_origin_y = math.floor((font_config.ascent + font_config.descent - glyph_height) / 2)
        vertical_origin_y = (glyph_height - font_config.size) // 2
        builder.glyphs.append(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            advance_height=font_config.size,
            horizontal_origin=(0, horizontal_origin_y),
            vertical_origin_y=vertical_origin_y,
            data=glyph_data,
        ))

    return builder


def make_font_files(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_infos: list[tuple[str, str]]):
    fs_util.make_dirs(font_config.outputs_dir)

    builder = _create_builder(font_config, character_mapping, glyph_file_infos)

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
