import os
import time
import tomllib

from configs import path_define

display_name_format = 'Retro Pixel - {name}'
unique_name_format = 'Retro-Pixel-{name}'
output_file_name_format = 'retro-pixel-{name}'
version = f'{time.strftime("%Y.%m.%d")}'
copyright_string_format = "Copyright (c) 2023, TakWolf (https://takwolf.com), with Reserved Font Name '{name}'."
designer = 'TakWolf'
description = 'Open source pixel font.'
vendor_url = 'https://retro-pixel-font.takwolf.com'
designer_url = 'https://takwolf.com'
license_description = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
license_info_url = 'https://scripts.sil.org/OFL'


class VerticalMetrics:
    def __init__(self, line_height, ascent, descent, x_height, cap_height):
        self.line_height = line_height
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height


class FontConfig:
    @staticmethod
    def loads():
        font_configs = []
        for output_name in os.listdir(path_define.glyphs_dir):
            glyphs_dir = os.path.join(path_define.glyphs_dir, output_name)
            if not os.path.isdir(glyphs_dir):
                continue
            config_file_path = os.path.join(glyphs_dir, 'config.toml')
            with open(config_file_path, 'rb') as config_file:
                config_data = tomllib.load(config_file)['font']
            font_config = FontConfig(config_data, output_name)
            font_configs.append(font_config)
        return font_configs

    def __init__(self, config_data, output_name, dot_em_units=100):
        self.display_name = display_name_format.format(name=config_data['display_name'])
        self.unique_name = unique_name_format.format(name=config_data['unique_name'])
        self.style_name = config_data['style_name']
        self.output_dir_name = output_name
        self.output_file_name = output_file_name_format.format(name=output_name)

        self.px = config_data['px']
        self.line_height_px = config_data['line_height_px']
        self.box_origin_y_px = config_data['box_origin_y_px']
        self.x_height_px = config_data['x_height_px']
        self.cap_height_px = config_data['cap_height_px']
        self.dot_em_units = dot_em_units

    def get_name_strings(self):
        return {
            'copyright': copyright_string_format.format(name=self.display_name),
            'familyName': self.display_name,
            'styleName': self.style_name,
            'uniqueFontIdentifier': f'{self.unique_name};{version}',
            'fullName': self.display_name,
            'version': version,
            'psName': self.unique_name,
            'designer': designer,
            'description': description,
            'vendorURL': vendor_url,
            'designerURL': designer_url,
            'licenseDescription': license_description,
            'licenseInfoURL': license_info_url,
        }

    def get_units_per_em(self):
        return self.px * self.dot_em_units

    def get_box_origin_y(self):
        return self.box_origin_y_px * self.dot_em_units

    def get_vertical_metrics(self):
        line_height = self.line_height_px * self.dot_em_units
        ascent = (self.box_origin_y_px + int((self.line_height_px - self.px) / 2)) * self.dot_em_units
        descent = ascent - line_height
        x_height = self.x_height_px * self.dot_em_units
        cap_height = self.cap_height_px * self.dot_em_units
        return VerticalMetrics(line_height, ascent, descent, x_height, cap_height)
