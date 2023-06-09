import os
import tomllib
from typing import Final

from configs import path_define

_DEFAULT_PREVIEW_TEXT = """
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
"""


class FontConfig:
    FAMILY_NAME_FORMAT: Final[str] = 'Retro Pixel {font_name}'
    MANUFACTURER: Final[str] = 'TakWolf'
    DESIGNER: Final[str] = 'TakWolf'
    COPYRIGHT_INFO_FORMAT: Final[str] = "Copyright (c) 2023, TakWolf (https://takwolf.com), with Reserved Font Name 'Retro Pixel {font_name}'."
    LICENSE_INFO: Final[str] = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    VENDOR_URL: Final[str] = 'https://retro-pixel-font.takwolf.com'
    DESIGNER_URL: Final[str] = 'https://takwolf.com'
    LICENSE_URL: Final[str] = 'https://scripts.sil.org/OFL'

    @staticmethod
    def loads() -> list['FontConfig']:
        configs = []
        for outputs_name in os.listdir(path_define.glyphs_dir):
            config_file_path = os.path.join(path_define.glyphs_dir, outputs_name, 'config.toml')
            if not os.path.isfile(config_file_path):
                continue
            with open(config_file_path, 'rb') as file:
                config_data: dict = tomllib.load(file)['font']
            config = FontConfig(config_data)
            assert config.outputs_name == outputs_name
            configs.append(config)
        configs.sort(key=lambda x: x.name)
        return configs

    def __init__(self, config_data: dict):
        self.name: str = config_data['name']
        self.family_name = FontConfig.FAMILY_NAME_FORMAT.format(font_name=self.name)
        self.outputs_name = self.name.lower().replace(' ', '-')
        self.full_outputs_name = self.family_name.lower().replace(' ', '-')

        self.style_name: str = config_data['style_name']
        self.serif_mode: str = config_data['serif_mode']
        self.width_mode: str = config_data['width_mode']
        self.description: str = config_data['description']
        self.copyright_info = FontConfig.COPYRIGHT_INFO_FORMAT.format(font_name=self.name)

        self.size: int = config_data['size']
        self.line_height: int = config_data['line_height']
        assert (self.line_height - self.size) % 2 == 0, f"Font config '{self.name}': the difference between 'line_height' and 'size' must be a multiple of 2"
        self.box_origin_y: int = config_data['box_origin_y']
        self.ascent = self.box_origin_y + (self.line_height - self.size) // 2
        self.descent = self.ascent - self.line_height
        self.x_height: int = config_data['x_height']
        self.cap_height: int = config_data['cap_height']

        self.fallback_lower_from_upper: bool = config_data.get('fallback_lower_from_upper', False)
        self.fallback_upper_from_lower: bool = config_data.get('fallback_upper_from_lower', False)

        self.readme_intro: str = config_data['readme_intro']
        self.preview_text: str = config_data.get('preview_text', _DEFAULT_PREVIEW_TEXT).strip()

        self.outputs_dir = os.path.join(path_define.outputs_dir, self.outputs_name)
        self.docs_dir = os.path.join(path_define.docs_dir, self.outputs_name)
        self.www_dir = os.path.join(path_define.www_dir, self.outputs_name)
