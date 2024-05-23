import logging

from scripts.configs import path_define, FontConfig

logger = logging.getLogger('info_service')

_ofl_string_format = path_define.project_root_dir.joinpath('LICENSE-OFL').read_text('utf-8')


def make_ofl_txt_file(font_config: FontConfig):
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('OFL.txt')
    ofl_string = _ofl_string_format.format(font_name=font_config.name)
    file_path.write_text(ofl_string, 'utf-8')
    logger.info("Make ofl txt file: '%s'", file_path)


def make_info_txt_file(font_config: FontConfig):
    lines = [
        f'{font_config.family_name}',
        '',
        f'font-size: {font_config.font_size}px',
        f'line-height: {font_config.line_height}px',
        '',
        f'{font_config.description}',
        '',
    ]

    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('info.txt')
    file_path.write_text('\n'.join(lines), 'utf-8')
    logger.info("Make info txt file: '%s'", file_path)


def make_alphabet_txt_file(font_config: FontConfig, alphabet: list[str]):
    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('alphabet.txt')
    file_path.write_text(''.join(alphabet), 'utf-8')
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

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('readme.txt')
    file_path.write_text('\n'.join(lines), 'utf-8')
    logger.info("Make readme txt file: '%s'", file_path)
