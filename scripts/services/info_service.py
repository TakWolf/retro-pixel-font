import logging
import os.path

from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util

logger = logging.getLogger('info_service')

_ofl_string_format = fs_util.read_str(os.path.join(path_define.project_root_dir, 'LICENSE-OFL'))


def make_ofl_txt_file(font_config: FontConfig):
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'OFL.txt')
    ofl_string = _ofl_string_format.format(font_name=font_config.name)
    fs_util.write_str(ofl_string, file_path)
    logger.info("Make ofl txt file: '%s'", file_path)


def make_info_txt_file(font_config: FontConfig):
    lines = [
        f'{font_config.family_name}',
        '',
        f'font-size: {font_config.size}px',
        f'line-height: {font_config.line_height}px',
        '',
        f'{font_config.description}',
        '',
    ]

    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'info.txt')
    fs_util.write_str('\n'.join(lines), file_path)
    logger.info("Make info txt file: '%s'", file_path)


def make_alphabet_txt_file(font_config: FontConfig, alphabet: list[str]):
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'alphabet.txt')
    fs_util.write_str(''.join(alphabet), file_path)
    logger.info("Make alphabet txt file: '%s'", file_path)


def make_readme_txt_file():
    lines = [
        'Retro Pixel Font',
        '',
        'https://retro-pixel-font.takwolf.com',
        '',
        f'version: {FontConfig.VERSION}',
        '',
    ]

    fs_util.make_dir(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, 'readme.txt')
    fs_util.write_str('\n'.join(lines), file_path)
    logger.info("Make readme txt file: '%s'", file_path)
