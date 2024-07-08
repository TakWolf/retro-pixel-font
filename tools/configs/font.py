import tomllib
from pathlib import Path

from pixel_font_builder import WeightName, SerifStyle, SlantStyle, WidthStyle

from tools.configs import path_define

_DEFAULT_PREVIEW_TEXT = '''
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789
!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
'''


class FontConfig:
    @staticmethod
    def load() -> dict[str, 'FontConfig']:
        configs = []
        for file_dir in path_define.glyphs_dir.iterdir():
            file_path = file_dir.joinpath('config.toml')
            if not file_path.is_file():
                continue
            config_data = tomllib.loads(file_path.read_text('utf-8'))['font']
            name = config_data['name']
            weight_name = WeightName(config_data['weight_name'])
            serif_style = SerifStyle(config_data['serif_style'])
            slant_style = SlantStyle(config_data['slant_style'])
            width_style = WidthStyle(config_data['width_style'])
            font_size = config_data['size']
            ascent = config_data['ascent']
            descent = config_data['descent']
            x_height = config_data['x_height']
            cap_height = config_data['cap_height']
            fallback_lower_from_upper = config_data.get('fallback_lower_from_upper', False)
            fallback_upper_from_lower = config_data.get('fallback_upper_from_lower', False)
            preview_text = config_data.get('preview_text', _DEFAULT_PREVIEW_TEXT).strip()
            config = FontConfig(
                name,
                weight_name,
                serif_style,
                slant_style,
                width_style,
                font_size,
                ascent,
                descent,
                x_height,
                cap_height,
                fallback_lower_from_upper,
                fallback_upper_from_lower,
                preview_text,
            )
            assert config.outputs_name == file_dir.name, f"Config 'name' error: '{file_path}'"
            assert (config.line_height - font_size) % 2 == 0, f"Config 'line_height' error: '{file_path}'"
            configs.append(config)
        configs.sort(key=lambda x: x.name)
        return {config.outputs_name: config for config in configs}

    name: str
    outputs_name: str

    weight_name: WeightName
    serif_style: SerifStyle
    slant_style: SlantStyle
    width_style: WidthStyle

    font_size: int
    ascent: int
    descent: int
    x_height: int
    cap_height: int

    fallback_lower_from_upper: bool
    fallback_upper_from_lower: bool

    preview_text: str

    glyphs_dir: Path
    outputs_dir: Path
    docs_dir: Path

    def __init__(
            self,
            name: str,
            weight_name: WeightName,
            serif_style: SerifStyle,
            slant_style: SlantStyle,
            width_style: WidthStyle,
            font_size: int,
            ascent: int,
            descent: int,
            x_height: int,
            cap_height: int,
            fallback_lower_from_upper: bool,
            fallback_upper_from_lower: bool,
            preview_text: str,
    ):
        self.name = name
        self.outputs_name = name.lower().replace(' ', '-')

        self.weight_name = weight_name
        self.serif_style = serif_style
        self.slant_style = slant_style
        self.width_style = width_style

        self.font_size = font_size
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height

        self.fallback_lower_from_upper = fallback_lower_from_upper
        self.fallback_upper_from_lower = fallback_upper_from_lower

        self.preview_text = preview_text

        self.glyphs_dir = path_define.glyphs_dir.joinpath(self.outputs_name)
        self.outputs_dir = path_define.outputs_dir.joinpath(self.outputs_name)
        self.docs_dir = path_define.docs_dir.joinpath(self.outputs_name)

    @property
    def line_height(self) -> int:
        return self.ascent - self.descent
