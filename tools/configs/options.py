from typing import Literal, get_args

type FontFormat = Literal[
    'otf',
    'otf.woff',
    'otf.woff2',
    'ttf',
    'ttf.woff',
    'ttf.woff2',
    'ms.bitmap.ttf',
    'otb',
    'dfont',
    'bdf',
    'pcf',
]
FONT_FORMATS = list[FontFormat](get_args(FontFormat.__value__))
