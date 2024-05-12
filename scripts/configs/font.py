import datetime
import os
from typing import Final

from pixel_font_builder import WeightName, SerifStyle, SlantStyle, WidthMode

from scripts.configs import path_define
from scripts.utils import fs_util

_DEFAULT_PREVIEW_TEXT = '''
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
'''


class FontConfig:
    VERSION: Final[str] = '2024.05.12'
    VERSION_TIME: Final[datetime.datetime] = datetime.datetime.fromisoformat(f'{VERSION.replace('.', '-')}T00:00:00Z')
    FAMILY_NAME_FORMAT: Final[str] = 'Retro Pixel {font_name}'
    ZIP_OUTPUTS_NAME: Final[str] = 'retro-pixel-font'
    MANUFACTURER: Final[str] = 'TakWolf'
    DESIGNER: Final[str] = 'TakWolf'
    COPYRIGHT_INFO_FORMAT: Final[str] = "Copyright (c) 2023, TakWolf (https://takwolf.com), with Reserved Font Name 'Retro Pixel {font_name}'."
    LICENSE_INFO: Final[str] = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    VENDOR_URL: Final[str] = 'https://retro-pixel-font.takwolf.com'
    DESIGNER_URL: Final[str] = 'https://takwolf.com'
    LICENSE_URL: Final[str] = 'https://openfontlicense.org'

    @staticmethod
    def load_all() -> dict[str, 'FontConfig']:
        configs = []
        for outputs_name in os.listdir(path_define.glyphs_dir):
            file_path = os.path.join(path_define.glyphs_dir, outputs_name, 'config.toml')
            if not os.path.isfile(file_path):
                continue
            config_data = fs_util.read_toml(file_path)['font']
            name = config_data['name']
            weight_name = WeightName(config_data['weight_name'])
            serif_style = SerifStyle(config_data['serif_style'])
            slant_style = SlantStyle(config_data['slant_style'])
            width_mode = WidthMode(config_data['width_mode'])
            description = config_data['description']
            font_size = config_data['size']
            ascent = config_data['ascent']
            descent = config_data['descent']
            x_height = config_data['x_height']
            cap_height = config_data['cap_height']
            fallback_lower_from_upper = config_data.get('fallback_lower_from_upper', False)
            fallback_upper_from_lower = config_data.get('fallback_upper_from_lower', False)
            readme_intro = config_data['readme_intro']
            preview_text = config_data.get('preview_text', _DEFAULT_PREVIEW_TEXT).strip()
            config = FontConfig(
                name,
                weight_name,
                serif_style,
                slant_style,
                width_mode,
                description,
                font_size,
                ascent,
                descent,
                x_height,
                cap_height,
                fallback_lower_from_upper,
                fallback_upper_from_lower,
                readme_intro,
                preview_text,
            )
            assert config.outputs_name == outputs_name, f"Config 'name' error: '{file_path}'"
            assert (config.line_height - font_size) % 2 == 0, f"Config 'line_height' error: '{file_path}'"
            configs.append(config)
        configs.sort(key=lambda x: x.name)
        return {config.outputs_name: config for config in configs}

    def __init__(
            self,
            name: str,
            weight_name: WeightName,
            serif_style: SerifStyle,
            slant_style: SlantStyle,
            width_mode: WidthMode,
            description: str,
            font_size: int,
            ascent: int,
            descent: int,
            x_height: int,
            cap_height: int,
            fallback_lower_from_upper: bool,
            fallback_upper_from_lower: bool,
            readme_intro: str,
            preview_text: str,
    ):
        self.name = name
        self.family_name = FontConfig.FAMILY_NAME_FORMAT.format(font_name=name)
        self.outputs_name = name.lower().replace(' ', '-')
        self.full_outputs_name = self.family_name.lower().replace(' ', '-')

        self.weight_name = weight_name
        self.serif_style = serif_style
        self.slant_style = slant_style
        self.width_mode = width_mode
        self.description = description
        self.copyright_info = FontConfig.COPYRIGHT_INFO_FORMAT.format(font_name=name)

        self.font_size = font_size
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height

        self.fallback_lower_from_upper = fallback_lower_from_upper
        self.fallback_upper_from_lower = fallback_upper_from_lower

        self.readme_intro = readme_intro
        self.preview_text = preview_text

        self.outputs_dir = os.path.join(path_define.outputs_dir, self.outputs_name)
        self.docs_dir = os.path.join(path_define.docs_dir, self.outputs_name)
        self.www_dir = os.path.join(path_define.www_dir, self.outputs_name)

    @property
    def line_height(self) -> int:
        return self.ascent - self.descent
