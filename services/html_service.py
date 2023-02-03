import logging
import os

import minify_html

import configs
from utils import fs_util

logger = logging.getLogger('html-service')


def make_alphabet_html_file(font_config, alphabet):
    template = configs.template_env.get_template('alphabet.html')
    html = template.render(
        font_config=font_config,
        alphabet=''.join(alphabet),
    )
    html = minify_html.minify(html, minify_css=True, minify_js=True)
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    html_file_path = os.path.join(font_config.outputs_dir, 'alphabet.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')
