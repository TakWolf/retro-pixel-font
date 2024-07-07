import math

from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont
from loguru import logger

from tools.configs import path_define
from tools.configs.font import FontConfig


def _load_font(font_config: FontConfig, scale: int = 1) -> FreeTypeFont:
    file_path = font_config.outputs_dir.joinpath(f'retro-pixel-{font_config.outputs_name}.woff2')
    return ImageFont.truetype(file_path, font_config.font_size * scale)


def _draw_text(
        image: Image.Image,
        xy: tuple[float, float],
        text: str,
        font: FreeTypeFont,
        text_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        shadow_color: tuple[int, int, int, int] | None = None,
        line_height: int | None = None,
        line_gap: int = 0,
        is_horizontal_centered: bool = False,
        is_vertical_centered: bool = False,
):
    draw = ImageDraw.Draw(image)
    x, y = xy
    default_line_height = sum(font.getmetrics())
    if line_height is None:
        line_height = default_line_height
    y += (line_height - default_line_height) / 2
    spacing = line_height + line_gap - font.getbbox('A')[3]
    if is_horizontal_centered:
        x -= draw.textbbox((0, 0), text, font=font)[2] / 2
    if is_vertical_centered:
        y -= line_height / 2
    if shadow_color is not None:
        draw.text((x + 1, y + 1), text, fill=shadow_color, font=font, spacing=spacing)
    draw.text((x, y), text, fill=text_color, font=font, spacing=spacing)


def _draw_demo_lines(
        image: Image.Image,
        xy: tuple[float, float],
        line_infos: list[tuple[str, FreeTypeFont]],
        text_color: tuple[int, int, int, int],
        shadow_color: tuple[int, int, int, int],
):
    x, y = xy
    for line, font in line_infos:
        _draw_text(image, (x, y), line, font, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
        y += sum(font.getmetrics())


def make_preview_image(font_config: FontConfig):
    font = _load_font(font_config)
    text_color = (255, 255, 255, 255)
    lines = font_config.preview_text.split('\n')

    content_width = 0
    for line in lines:
        line_width = math.ceil(font.getlength(line))
        if line_width > content_width:
            content_width = line_width
    content_height = font_config.line_height * len(lines)

    image = Image.new('RGBA', (font_config.font_size * 2 + content_width, font_config.font_size * 2 + content_height), (30, 144, 255, 255))
    cursor_x = font_config.font_size
    cursor_y = font_config.font_size
    for line in lines:
        _draw_text(image, (cursor_x, cursor_y), line, font, text_color=text_color)
        cursor_y += font_config.line_height
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    font_config.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = font_config.outputs_dir.joinpath('preview.png')
    image.save(file_path)
    logger.info("Make preview image: '{}'", file_path)


def make_readme_banner(font_configs: dict[str, FontConfig]):
    font_thick = _load_font(font_configs['thick'], 2)
    font_cute_prop = _load_font(font_configs['cute-prop'])
    text_color = (255, 255, 255, 255)
    shadow_color = (80, 80, 80, 255)

    image = Image.open(path_define.images_dir.joinpath('readme-banner-background.png'))
    _draw_text(image, (image.width / 2, 28), 'Retro Pixel Font', font_thick, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 28 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_cute_prop, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('readme-banner.png')
    image.save(file_path)
    logger.info("Make readme banner: '{}'", file_path)


def make_github_banner(font_configs: dict[str, FontConfig]):
    font_title = _load_font(font_configs['thick'], 2)
    font_arcade = _load_font(font_configs['arcade'])
    font_cute_mono = _load_font(font_configs['cute-mono'])
    font_cute_prop = _load_font(font_configs['cute-prop'])
    font_thick = _load_font(font_configs['thick'])
    text_color = (255, 255, 255, 255)
    shadow_color = (80, 80, 80, 255)

    image = Image.open(path_define.images_dir.joinpath('github-banner-background.png'))
    _draw_text(image, (image.width / 2, 40 + 16), 'Retro Pixel Font', font_title, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 3), 'A set of open source old game style pixel fonts.', font_cute_prop, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    line_infos = [
        ('The quick brown fox jumps over a lazy dog.', font_arcade),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_arcade),
        ('The quick brown fox jumps over a lazy dog.', font_cute_mono),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_mono),
        ('The quick brown fox jumps over a lazy dog.', font_cute_prop),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_prop),
        ('The quick brown fox jumps over a lazy dog.', font_thick),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_thick),
    ]
    _draw_demo_lines(image, (image.width / 2, 40 + 16 * 5), line_infos, text_color=text_color, shadow_color=shadow_color)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('github-banner.png')
    image.save(file_path)
    logger.info("Make github banner: '{}'", file_path)


def make_itch_io_banner(font_configs: dict[str, FontConfig]):
    font_thick = _load_font(font_configs['thick'], 2)
    font_cute_prop = _load_font(font_configs['cute-prop'])
    text_color = (255, 255, 255, 255)
    shadow_color = (80, 80, 80, 255)

    image = Image.open(path_define.images_dir.joinpath('itch-io-banner-background.png'))
    _draw_text(image, (image.width / 2, 32), 'Retro Pixel Font', font_thick, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 32 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_cute_prop, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('itch-io-banner.png')
    image.save(file_path)
    logger.info("Make itch.io banner: '{}'", file_path)


def make_itch_io_cover(font_configs: dict[str, FontConfig]):
    font_title = _load_font(font_configs['thick'], 2)
    font_arcade = _load_font(font_configs['arcade'])
    font_cute_mono = _load_font(font_configs['cute-mono'])
    font_cute_prop = _load_font(font_configs['cute-prop'])
    font_thick = _load_font(font_configs['thick'])
    text_color = (255, 255, 255, 255)
    shadow_color = (80, 80, 80, 255)

    image = Image.open(path_define.images_dir.joinpath('itch-io-cover-background.png'))
    _draw_text(image, (image.width / 2, 6), 'Retro Pixel Font', font_title, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_cute_prop, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    line_infos = [
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_arcade),
        ('0123456789', font_arcade),
        ('The quick brown fox jumps over a lazy dog.', font_cute_mono),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_mono),
        ('The quick brown fox jumps over a lazy dog.', font_cute_prop),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_prop),
        ('The quick brown fox jumps over a lazy dog.', font_thick),
        ('0123456789', font_thick),
        ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_thick),
    ]
    _draw_demo_lines(image, (image.width / 2, 6 + 16 * 2 + 8 + 11 + 24), line_infos, text_color=text_color, shadow_color=shadow_color)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('itch-io-cover.png')
    image.save(file_path)
    logger.info("Make itch.io cover: '{}'", file_path)


def make_afdian_cover(font_configs: dict[str, FontConfig]):
    font_title = _load_font(font_configs['thick'], 2)
    font_arcade = _load_font(font_configs['arcade'])
    font_cute_mono = _load_font(font_configs['cute-mono'])
    font_cute_prop = _load_font(font_configs['cute-prop'])
    font_thick = _load_font(font_configs['thick'])
    text_color = (255, 255, 255, 255)
    shadow_color = (80, 80, 80, 255)

    image = Image.open(path_define.images_dir.joinpath('afdian-cover-background.png'))
    _draw_text(image, (image.width / 2, 18), 'Retro Pixel Font', font_title, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_cute_prop, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    line_infos = [
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_arcade),
        ('abcdefghijklmnopqrstuvwxyz', font_arcade),
        ('0123456789', font_arcade),
        ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_arcade),
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_cute_mono),
        ('abcdefghijklmnopqrstuvwxyz', font_cute_mono),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_mono),
        ('ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_cute_prop),
        ('abcdefghijklmnopqrstuvwxyz', font_cute_prop),
        ('0123456789 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_cute_prop),
        ('The quick brown fox jumps over a lazy dog.', font_thick),
        ('0123456789', font_thick),
        ('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_thick),
    ]
    _draw_demo_lines(image, (image.width / 2, 18 + 16 * 2 + 8 + 11 + 24), line_infos, text_color=text_color, shadow_color=shadow_color)
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)
    file_path = path_define.outputs_dir.joinpath('afdian-cover.png')
    image.save(file_path)
    logger.info("Make afdian cover: '{}'", file_path)
