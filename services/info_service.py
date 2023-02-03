import logging
import os.path

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
        ofl_string = _load_ofl_string_format().format(name=font_config.display_name)
        file.write(ofl_string)
    logger.info(f'make {txt_file_path}')


def make_alphabet_txt_file(font_config, alphabet):
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    txt_file_path = os.path.join(font_config.outputs_dir, 'alphabet.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {txt_file_path}')


_default_demo_text = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'abcdefghijklmnopqrstuvwxyz',
    '0123456789',
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
]


def get_demo_text(alphabet):
    demo_text = []
    for default_demo_line in _default_demo_text:
        demo_line = []
        for c in default_demo_line:
            if c in alphabet:
                demo_line.append(c)
        if len(demo_line) > 0:
            demo_text.append(''.join(demo_line))
    return demo_text
