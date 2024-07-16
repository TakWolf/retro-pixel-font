import random
from pathlib import Path

import bs4
from jinja2 import Environment, FileSystemLoader
from loguru import logger

from tools.configs import path_define
from tools.configs.font import FontConfig

_environment = Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(path_define.templates_dir),
)

_build_random_key = random.random()


def _make_html(template_name: str, file_path: Path, params: dict[str, object] | None = None):
    params = {} if params is None else dict(params)
    params['build_random_key'] = _build_random_key

    html = _environment.get_template(template_name).render(params)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html, 'utf-8')
    logger.info("Make html: '{}'", file_path)


def make_alphabet_html(font_config: FontConfig, alphabet: set[str]):
    _make_html('alphabet.html', font_config.outputs_dir.joinpath('alphabet.html'), {
        'font_config': font_config,
        'alphabet': ''.join(sorted(alphabet)),
    })


def _handle_demo_html_element(alphabet: set[str], soup: bs4.BeautifulSoup, element: bs4.PageElement):
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


def make_demo_html(font_config: FontConfig, alphabet: set[str]):
    content_html = _environment.get_template('demo-content.html').render(font_config=font_config)
    content_html = ''.join(line.strip() for line in content_html.split('\n'))
    soup = bs4.BeautifulSoup(content_html, 'html.parser')
    _handle_demo_html_element(alphabet, soup, soup)
    content_html = str(soup)

    _make_html('demo.html', font_config.outputs_dir.joinpath('demo.html'), {
        'font_config': font_config,
        'content_html': content_html,
    })


def make_index_html(font_configs: dict[str, FontConfig]):
    _make_html('index.html', path_define.outputs_dir.joinpath('index.html'), {
        'font_configs': font_configs,
    })


def make_itch_io_details_html(font_configs: dict[str, FontConfig]):
    _make_html('itch-io-details.html', path_define.outputs_dir.joinpath('itch-io-details.html'), {
        'font_configs': font_configs,
    })
