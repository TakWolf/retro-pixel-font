import logging
import os
import shutil

import unidata_blocks
from pixel_font_builder import FontBuilder, Glyph
from pixel_font_builder.opentype import Flavor

from configs import path_define, FontConfig
from utils import fs_util, glyph_util

logger = logging.getLogger('font-service')


def format_glyph_files(font_config: FontConfig):
    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)
    tmp_dir = os.path.join(path_define.glyphs_tmp_dir, font_config.outputs_name)
    fs_util.delete_dir(tmp_dir)
    for file_from_dir, file_name in fs_util.walk_files(root_dir):
        file_from_path = os.path.join(file_from_dir, file_name)

        if file_name == 'config.toml':
            file_to_dir = tmp_dir
            file_to_path = os.path.join(file_to_dir, file_name)
            assert not os.path.exists(file_to_path), f"Config file duplication: '{file_from_path}'"
            fs_util.make_dirs(file_to_dir)
            shutil.copyfile(file_from_path, file_to_path)
            logger.info("Copy config file: '%s'", file_to_path)
            continue

        if not file_name.endswith('.png'):
            continue
        if file_name == 'notdef.png':
            file_to_dir = tmp_dir
        else:
            hex_name = file_name.removesuffix('.png').upper()
            code_point = int(hex_name, 16)
            file_name = f'{hex_name}.png'
            block = unidata_blocks.get_block_by_code_point(code_point)
            block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
            file_to_dir = os.path.join(tmp_dir, block_dir_name)
        file_to_path = os.path.join(file_to_dir, file_name)
        assert not os.path.exists(file_to_path), f"Glyph file duplication: '{file_from_path}'"

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

        fs_util.make_dirs(file_to_dir)
        glyph_util.save_glyph_data_to_png(glyph_data, file_to_path)
        logger.info("Format glyph file: '%s'", file_to_path)
    shutil.rmtree(root_dir)
    os.rename(tmp_dir, root_dir)


def collect_glyph_files(font_config: FontConfig) -> tuple[list[str], dict[int, str], dict[str, str]]:
    character_mapping = {}
    glyph_file_paths = {}

    root_dir = os.path.join(path_define.glyphs_dir, font_config.outputs_name)
    for glyph_file_dir, glyph_file_name in fs_util.walk_files(root_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
        if glyph_file_name == 'notdef.png':
            glyph_file_paths['.notdef'] = glyph_file_path
        else:
            hex_name = glyph_file_name.removesuffix('.png')
            code_point = int(hex_name, 16)
            glyph_name = f'uni{code_point:04X}'
            character_mapping[code_point] = glyph_name
            glyph_file_paths[glyph_name] = glyph_file_path

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

    return alphabet, character_mapping, glyph_file_paths


def _create_builder(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_paths: dict[str, str]) -> FontBuilder:
    builder = FontBuilder(
        font_config.size,
        font_config.ascent,
        font_config.descent,
        font_config.x_height,
        font_config.cap_height,
    )

    builder.character_mapping.update(character_mapping)
    for glyph_name, glyph_file_path in glyph_file_paths.items():
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        offset_y = font_config.box_origin_y + (glyph_height - font_config.size) // 2 - glyph_height
        builder.add_glyph(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, offset_y),
            data=glyph_data,
        ))

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

    return builder


def make_font_files(font_config: FontConfig, character_mapping: dict[int, str], glyph_file_paths: dict[str, str]):
    fs_util.make_dirs(font_config.outputs_dir)

    builder = _create_builder(font_config, character_mapping, glyph_file_paths)

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
