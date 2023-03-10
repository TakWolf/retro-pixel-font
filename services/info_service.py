import logging
import os.path

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('info-service')

_ofl_string_format = None


def _load_ofl_string_format():
    global _ofl_string_format
    if _ofl_string_format is None:
        ofl_file_path = os.path.join(path_define.project_root_dir, 'LICENSE-OFL')
        with open(ofl_file_path, 'r', encoding='utf-8') as file:
            _ofl_string_format = file.read()
    return _ofl_string_format


def make_ofl_txt_file(font_config):
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    txt_file_path = os.path.join(font_config.outputs_dir, 'OFL.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        ofl_string = _load_ofl_string_format().format(
            font_name=font_config.display_name,
            designer=font_config.designer,
            designer_url=font_config.designer_url,
            copyright_year=font_config.copyright_year,
        )
        file.write(ofl_string)
    logger.info(f'make {txt_file_path}')


def make_info_txt_file(font_config):
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    txt_file_path = os.path.join(font_config.outputs_dir, 'info.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(f'{font_config.full_display_name}\n\n')
        file.write(f'font-size: { font_config.px }px\n')
        file.write(f'line-height: { font_config.line_height_px }px\n\n')
        file.write(f'{font_config.description}\n')
    logger.info(f'make {txt_file_path}')


def make_alphabet_txt_file(font_config, alphabet):
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    txt_file_path = os.path.join(font_config.outputs_dir, 'alphabet.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {txt_file_path}')


def make_readme_txt_file():
    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    txt_file_path = os.path.join(path_define.outputs_dir, 'readme.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write('Retro Pixel Font\n\n')
        file.write('https://retro-pixel-font.takwolf.com\n\n')
        file.write(f'version: {configs.font_version}\n')
    logger.info(f'make {txt_file_path}')


def make_readme_md_file():
    preview = ''
    for font_config in configs.font_configs:
        preview += f'### {font_config.display_name}\n\n'
        preview += f'?????????{font_config.px}px / ?????????{font_config.line_height_px}px ?? '
        preview += f'[????????????](https://retro-pixel-font.takwolf.com#font-{font_config.output_name}) ?? '
        preview += f'[?????????](https://retro-pixel-font.takwolf.com/{font_config.output_name}/alphabet.html) ?? '
        preview += f'[????????????](https://retro-pixel-font.takwolf.com/{font_config.output_name}/demo.html)\n\n'
        preview += f'{font_config.readme_intro}\n\n'
        preview += f'![preview-{font_config.output_name}](docs/{font_config.output_name}/preview.png)\n\n'
    preview = preview.strip()

    template = configs.template_env.get_template('README.md')
    markdown = template.render(preview=preview)
    md_file_path = os.path.join(path_define.project_root_dir, 'README.md')
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(markdown)
        file.write('\n')
    logger.info(f'make {md_file_path}')
