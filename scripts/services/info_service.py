import logging
import os.path

from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util

logger = logging.getLogger('info-service')


def _load_ofl_string_format() -> str:
    file_path = os.path.join(path_define.project_root_dir, 'LICENSE-OFL')
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


_ofl_string_format = _load_ofl_string_format()


def make_ofl_txt_file(font_config: FontConfig):
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'OFL.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        ofl_string = _load_ofl_string_format().format(font_name=font_config.name)
        file.write(ofl_string)
    logger.info("Make ofl txt file: '%s'", file_path)


def make_info_txt_file(font_config: FontConfig):
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'info.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f'{font_config.family_name}\n\n')
        file.write(f'font-size: {font_config.size}px\n')
        file.write(f'line-height: {font_config.line_height}px\n\n')
        file.write(f'{font_config.description}\n')
    logger.info("Make info txt file: '%s'", file_path)


def make_alphabet_txt_file(font_config: FontConfig, alphabet: list[str]):
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'alphabet.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info("Make alphabet txt file: '%s'", file_path)


def make_readme_txt_file():
    fs_util.make_dir(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, 'readme.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('Retro Pixel Font\n\n')
        file.write('https://retro-pixel-font.takwolf.com\n\n')
        file.write(f'version: {FontConfig.VERSION}\n')
    logger.info("Make readme txt file: '%s'", file_path)
