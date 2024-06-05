import logging

from scripts.configs import FontConfig

logger = logging.getLogger('info_service')


def make_info_txt(font_config: FontConfig):
    lines = [
        f'name: {font_config.name}',
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
