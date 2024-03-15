import logging
import os

import bs4
from jinja2 import Environment, FileSystemLoader

from scripts import configs
from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util

logger = logging.getLogger('template-service')

_environment = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(path_define.templates_dir),
)


def make_alphabet_html_file(font_config: FontConfig, alphabet: list[str]):
    template = _environment.get_template('alphabet.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        alphabet=''.join(alphabet),
    )
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'alphabet.html')
    fs_util.write_str(html, file_path)
    logger.info("Make alphabet html file: '%s'", file_path)


def _handle_demo_html_element(alphabet: list[str], soup: bs4.BeautifulSoup, element: bs4.PageElement):
    if isinstance(element, bs4.element.Tag):
        for child_element in list(element.contents):
            _handle_demo_html_element(alphabet, soup, child_element)
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


def make_demo_html_file(font_config: FontConfig, alphabet: list[str]):
    content_template = _environment.get_template('demo-content.html')
    content_html = content_template.render(font_config=font_config)
    content_html = ''.join(line.strip() for line in content_html.split('\n'))
    soup = bs4.BeautifulSoup(content_html, 'html.parser')
    _handle_demo_html_element(alphabet, soup, soup)
    content_html = str(soup)

    template = _environment.get_template('demo.html')
    html = template.render(
        configs=configs,
        font_config=font_config,
        content_html=content_html,
    )
    fs_util.make_dir(font_config.outputs_dir)
    file_path = os.path.join(font_config.outputs_dir, 'demo.html')
    fs_util.write_str(html, file_path)
    logger.info("Make demo html file: '%s'", file_path)


def make_index_html_file():
    template = _environment.get_template('index.html')
    html = template.render(configs=configs)
    fs_util.make_dir(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, 'index.html')
    fs_util.write_str(html, file_path)
    logger.info("Make index html file: '%s'", file_path)


def make_itch_io_details_html_file():
    template = _environment.get_template('itch-io-details.html')
    html = template.render(configs=configs)
    fs_util.make_dir(path_define.outputs_dir)
    file_path = os.path.join(path_define.outputs_dir, 'itch-io-details.html')
    fs_util.write_str(html, file_path)
    logger.info("Make itch.io details html file: '%s'", file_path)
