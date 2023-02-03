import os
import time
import tomllib

from configs import path_define

full_display_name_format = 'Retro Pixel - {name}'
full_unique_name_format = 'Retro-Pixel-{name}'
full_output_name_format = 'retro-pixel-{name}'
version = f'{time.strftime("%Y.%m.%d")}'
copyright_string_format = 'Copyright (c) {copyright_year}, {designer} ({designer_url}), with Reserved Font Name "Retro Pixel - {font_name}".'
vendor_url = 'https://retro-pixel-font.takwolf.com'
license_description = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
license_info_url = 'https://scripts.sil.org/OFL'


class VerticalMetrics:
    def __init__(self, ascent, descent, x_height, cap_height):
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
            if not os.path.isfile(config_file_path):
                continue
            with open(config_file_path, 'rb') as config_file:
                config_data = tomllib.load(config_file)['font']
            font_config = FontConfig(config_data, output_name)
            font_configs.append(font_config)
        return font_configs

    def __init__(self, config_data, output_name, dot_em_units=100):
        self.display_name = config_data['display_name']
        self.unique_name = config_data['unique_name']
        self.style_name = config_data['style_name']
        self.description = config_data['description']
        self.designer = config_data['designer']
        self.designer_url = config_data['designer_url']
        self.copyright_year = config_data['copyright_year']

        self.output_name = output_name
        self.outputs_dir = os.path.join(path_define.outputs_dir, output_name)
        self.docs_dir = os.path.join(path_define.docs_dir, output_name)
        self.www_dir = os.path.join(path_define.www_dir, output_name)

        self.full_display_name = full_display_name_format.format(name=self.display_name)
        self.full_unique_name = full_unique_name_format.format(name=self.unique_name)
        self.full_output_name = full_output_name_format.format(name=output_name)

        self.px = config_data['px']
        self.line_height_px = config_data['line_height_px']
        self.box_origin_y_px = config_data['box_origin_y_px']
        self.x_height_px = config_data['x_height_px']
        self.cap_height_px = config_data['cap_height_px']
        self.dot_em_units = dot_em_units

    def get_name_strings(self):
        return {
            'copyright': copyright_string_format.format(
                font_name=self.display_name,
                designer=self.designer,
                designer_url=self.designer_url,
                copyright_year=self.copyright_year,
            ),
            'familyName': self.full_display_name,
            'styleName': self.style_name,
            'uniqueFontIdentifier': f'{self.full_unique_name};{version}',
            'fullName': self.full_display_name,
            'version': version,
            'psName': self.full_unique_name,
            'designer': self.designer,
            'description': self.description,
            'vendorURL': vendor_url,
            'designerURL': self.designer_url,
            'licenseDescription': license_description,
            'licenseInfoURL': license_info_url,
        }

    def get_units_per_em(self):
        return self.px * self.dot_em_units

    def get_box_origin_y(self):
        return self.box_origin_y_px * self.dot_em_units

    def get_vertical_metrics(self):
        ascent = (self.box_origin_y_px + int((self.line_height_px - self.px) / 2)) * self.dot_em_units
        descent = ascent - self.line_height_px * self.dot_em_units
        x_height = self.x_height_px * self.dot_em_units
        cap_height = self.cap_height_px * self.dot_em_units
        return VerticalMetrics(ascent, descent, x_height, cap_height)
