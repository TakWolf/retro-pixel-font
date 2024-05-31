import logging
import random
from pathlib import Path

import bs4
from jinja2 import Environment, FileSystemLoader

from scripts import configs
from scripts.configs import path_define, FontConfig

logger = logging.getLogger('template_service')

_environment = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(path_define.templates_dir),
)

_build_random_key = random.random()


def _make_html_file(template_name: str, outputs_dir: Path, file_name: str, params: dict[str, object] = None):
    params = {} if params is None else dict(params)
    params['build_random_key'] = _build_random_key
    params['font_configs'] = configs.font_configs

    html = _environment.get_template(template_name).render(params)

    outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = outputs_dir.joinpath(file_name)
    file_path.write_text(html, 'utf-8')
    logger.info("Make html file: '%s'", file_path)


def make_alphabet_html_file(font_config: FontConfig, alphabet: list[str]):
    _make_html_file('alphabet.html', font_config.outputs_dir, 'alphabet.html', {
        'font_config': font_config,
        'alphabet': ''.join(alphabet),
    })


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
    content_html = _environment.get_template('demo-content.html').render(font_config=font_config)
    content_html = ''.join(line.strip() for line in content_html.split('\n'))
    soup = bs4.BeautifulSoup(content_html, 'html.parser')
    _handle_demo_html_element(alphabet, soup, soup)
    content_html = str(soup)

    _make_html_file('demo.html', font_config.outputs_dir, 'demo.html', {
        'font_config': font_config,
        'content_html': content_html,
    })


def make_index_html_file():
    _make_html_file('index.html', path_define.outputs_dir, 'index.html')


def make_itch_io_details_html_file():
    _make_html_file('itch-io-details.html', path_define.outputs_dir, 'itch-io-details.html')
