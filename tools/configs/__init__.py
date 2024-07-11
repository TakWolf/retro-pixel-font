from typing import Literal, get_args

version = '2024.05.12'

type FontFormat = Literal['otf', 'woff2', 'ttf', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))
