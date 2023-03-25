import logging
import os

import bs4

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('html-service')


def make_alphabet_html_file(font_config, alphabet):
    template = configs.template_env.get_template('alphabet.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        alphabet=''.join(alphabet),
    )
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    html_file_path = os.path.join(font_config.outputs_dir, 'alphabet.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def _handle_demo_html_element(soup, element, alphabet):
    if isinstance(element, bs4.element.Tag):
        for child_element in list(element.contents):
            _handle_demo_html_element(soup, child_element, alphabet)
    elif isinstance(element, bs4.element.NavigableString):
        text = str(element)
        tmp_parent = soup.new_tag('div')
        last_status = False
        text_buffer = ''
        for c in text:
            if c == ' ':
                status = last_status
            elif c == '\n':
                status = True
            else:
                status = c in alphabet
            if last_status != status:
                if text_buffer != '':
                    if last_status:
                        tmp_child = bs4.element.NavigableString(text_buffer)
                    else:
                        tmp_child = soup.new_tag('span')
                        tmp_child.string = text_buffer
                        tmp_child['class'] = 'char-notdef'
                    tmp_parent.append(tmp_child)
                    text_buffer = ''
                last_status = status
            text_buffer += c
        if text_buffer != '':
            if last_status:
                tmp_child = bs4.element.NavigableString(text_buffer)
            else:
                tmp_child = soup.new_tag('span')
                tmp_child.string = text_buffer
                tmp_child['class'] = 'char-notdef'
            tmp_parent.append(tmp_child)
        element.replace_with(tmp_parent)
        tmp_parent.unwrap()


def make_demo_html_file(font_config, alphabet):
    content_template = configs.template_env.get_template('demo-content.html')
    content_html = content_template.render(font_config=font_config)
    content_html = ''.join(line.strip() for line in content_html.split('\n'))
    soup = bs4.BeautifulSoup(content_html, 'html.parser')
    _handle_demo_html_element(soup, soup, alphabet)
    content_html = str(soup)

    template = configs.template_env.get_template('demo.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        content_html=content_html,
    )
    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    html_file_path = os.path.join(font_config.outputs_dir, 'demo.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def make_index_html_file():
    template = configs.template_env.get_template('index.html')
    html = template.render(configs=configs)
    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, 'index.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')


def make_itch_io_details_html_file():
    template = configs.template_env.get_template('itch-io-details.html')
    html = template.render(configs=configs)
    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    html_file_path = os.path.join(path_define.outputs_dir, 'itch-io-details.html')
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    logger.info(f'make {html_file_path}')
