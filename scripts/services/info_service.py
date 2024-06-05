import logging

from scripts import configs
from scripts.configs import path_define, FontConfig

logger = logging.getLogger('info_service')


def make_info_txt(font_config: FontConfig):
    lines = [
        f'Retro Pixel {font_config.name}',
        '',
        f'font-size: {font_config.font_size}px',
        f'line-height: {font_config.line_height}px',
        '',
    ]

    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('info.txt')
    file_path.write_text('\n'.join(lines), 'utf-8')
    logger.info("Make info txt: '%s'", file_path)


def make_alphabet_txt(font_config: FontConfig, alphabet: list[str]):
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('alphabet.txt')
    file_path.write_text(''.join(alphabet), 'utf-8')
    logger.info("Make alphabet txt: '%s'", file_path)


def make_readme_txt():
    lines = [
        'Retro Pixel Font',
        '',
        'https://retro-pixel-font.takwolf.com',
        '',
        f'version: {configs.font_version}',
        '',
    ]

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('readme.txt')
    file_path.write_text('\n'.join(lines), 'utf-8')
    logger.info("Make readme txt: '%s'", file_path)
