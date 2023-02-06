import logging
import os
import shutil

import configs
from configs import path_define
from utils import fs_util, glyph_util

logger = logging.getLogger('design-service')


def classify_glyph_files(font_config):
    glyphs_dir = os.path.join(path_define.glyphs_dir, font_config.output_name)
    glyphs_tmp_dir = os.path.join(path_define.glyphs_tmp_dir, font_config.output_name)
    fs_util.delete_dir(glyphs_tmp_dir)
    for file_from_dir, _, file_names in os.walk(glyphs_dir):
        for file_name in file_names:
            file_from_path = os.path.join(file_from_dir, file_name)
            if file_name == 'config.toml' or file_name == 'notdef.png':
                file_to_dir = glyphs_tmp_dir
            elif file_name.endswith('.png'):
                uni_hex_name = file_name.removesuffix('.png').upper()
                code_point = int(uni_hex_name, 16)
                unicode_block = configs.unidata_db.get_block_by_code_point(code_point)
                block_dir_name = f'{unicode_block.begin:04X}-{unicode_block.end:04X} {unicode_block.name}'
                file_to_dir = os.path.join(glyphs_tmp_dir, block_dir_name)
                file_name = f'{uni_hex_name}.png'
            else:
                continue
            file_to_path = os.path.join(file_to_dir, file_name)
            assert not os.path.exists(file_to_path), file_from_path
            fs_util.make_dirs_if_not_exists(file_to_dir)
            shutil.copyfile(file_from_path, file_to_path)
            logger.info(f'classify glyph file {file_to_path}')
    glyphs_old_dir = os.path.join(path_define.glyphs_tmp_dir, f'{font_config.output_name}.old')
    os.rename(glyphs_dir, glyphs_old_dir)
    os.rename(glyphs_tmp_dir, glyphs_dir)
    shutil.rmtree(glyphs_old_dir)


def verify_glyph_files(font_config):
    glyphs_dir = os.path.join(path_define.glyphs_dir, font_config.output_name)
    for glyph_file_dir, _, glyph_file_names in os.walk(glyphs_dir):
        for glyph_file_name in glyph_file_names:
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
            glyph_data, width, height = glyph_util.load_glyph_data_from_png(glyph_file_path)

            assert (height - font_config.px) % 2 == 0, glyph_file_path
            if height > font_config.line_height_px:
                for i in range(int((height - font_config.line_height_px) / 2)):
                    glyph_data.pop(0)
                    glyph_data.pop()
            elif height < font_config.line_height_px:
                for i in range(int((font_config.line_height_px - height) / 2)):
                    glyph_data.insert(0, [0 for _ in range(width)])
                    glyph_data.append([0 for _ in range(width)])

            glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_path)
            logger.info(f'format glyph file {glyph_file_path}')


def collect_glyph_files(font_config):
    alphabet = set()
    glyph_file_paths = {}
    glyphs_dir = os.path.join(path_define.glyphs_dir, font_config.output_name)
    for glyph_file_dir, _, glyph_file_names in os.walk(glyphs_dir):
        for glyph_file_name in glyph_file_names:
            if not glyph_file_name.endswith('.png'):
                continue
            glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
            if glyph_file_name == 'notdef.png':
                glyph_file_paths['.notdef'] = glyph_file_path
            else:
                uni_hex_name = glyph_file_name.removesuffix('.png').upper()
                code_point = int(uni_hex_name, 16)
                glyph_file_paths[code_point] = glyph_file_path
                c = chr(code_point)
                alphabet.add(c)
    alphabet = list(alphabet)
    alphabet.sort()
    return alphabet, glyph_file_paths
