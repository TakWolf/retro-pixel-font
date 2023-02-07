import logging
import math
import os

from PIL import Image, ImageFont, ImageDraw

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('image-service')


def _load_font(font_config, px_scale=1):
    font_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_output_name}.woff2')
    return ImageFont.truetype(font_file_path, font_config.px * px_scale)


def _draw_text(image, xy, text, font, text_color=(0, 0, 0), shadow_color=None, line_height=None, line_gap=0, is_horizontal_centered=False, is_vertical_centered=False):
    draw = ImageDraw.Draw(image)
    x, y = xy
    default_line_height = sum(font.getmetrics())
    if line_height is None:
        line_height = default_line_height
    y += (line_height - default_line_height) / 2
    spacing = line_height + line_gap - font.getsize('A')[1]
    if is_horizontal_centered:
        x -= draw.textbbox((0, 0), text, font=font)[2] / 2
    if is_vertical_centered:
        y -= line_height / 2
    if shadow_color is not None:
        draw.text((x + 1, y + 1), text, fill=shadow_color, font=font, spacing=spacing)
    draw.text((x, y), text, fill=text_color, font=font, spacing=spacing)


def make_preview_image_file(font_config):
    font = _load_font(font_config)
    background_color = (30, 144, 255)
    text_color = (255, 255, 255)
    lines = font_config.demo_text.split('\n')

    content_width = 0
    for line in lines:
        line_width = math.ceil(font.getlength(line))
        if line_width > content_width:
            content_width = line_width
    content_height = font_config.line_height_px * len(lines)

    image = Image.new('RGBA', (font_config.px * 2 + content_width, font_config.px * 2 + content_height), background_color)
    cursor_x = font_config.px
    cursor_y = font_config.px
    for line in lines:
        _draw_text(image, (cursor_x, cursor_y), line, font, text_color=text_color)
        cursor_y += font_config.line_height_px
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    image_file_path = os.path.join(font_config.outputs_dir, 'preview.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')


def make_readme_banner():
    font_x1 = _load_font(configs.font_config_map['thick'])
    font_x2 = _load_font(configs.font_config_map['thick'], 2)
    text_color = (255, 255, 255)
    shadow_color = (80, 80, 80)

    image = Image.open(os.path.join(path_define.images_dir, 'readme-banner-background.png'))
    _draw_text(image, (image.width / 2, 28), 'Retro Pixel Font', font_x2, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 28 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'readme-banner.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')


def make_github_banner():
    font_x1 = _load_font(configs.font_config_map['thick'])
    font_x2 = _load_font(configs.font_config_map['thick'], 2)
    text_color = (255, 255, 255)
    shadow_color = (80, 80, 80)

    image = Image.open(os.path.join(path_define.images_dir, 'github-banner-background.png'))
    _draw_text(image, (image.width / 2, 40 + 16), 'Retro Pixel Font', font_x2, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 3), 'A set of open source old game style pixel fonts.', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 5), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 6), 'abcdefghijklmnopqrstuvwxyz', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 7), '0123456789', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 40 + 16 * 8), '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'github-banner.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')


def make_itch_io_banner():
    font_x1 = _load_font(configs.font_config_map['thick'])
    font_x2 = _load_font(configs.font_config_map['thick'], 2)
    text_color = (255, 255, 255)
    shadow_color = (80, 80, 80)

    image = Image.open(os.path.join(path_define.images_dir, 'itch-io-banner-background.png'))
    _draw_text(image, (image.width / 2, 32), 'Retro Pixel Font', font_x2, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 32 + 16 * 2 + 8), 'A set of open source old game style pixel fonts.', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'itch-io-banner.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')


def make_itch_io_cover():
    font_x1 = _load_font(configs.font_config_map['thick'])
    font_x2 = _load_font(configs.font_config_map['thick'], 2)
    text_color = (255, 255, 255)
    shadow_color = (80, 80, 80)

    image = Image.open(os.path.join(path_define.images_dir, 'itch-io-cover-background.png'))
    _draw_text(image, (image.width / 2, 6), 'Retro Pixel Font', font_x2, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 3), 'A set of open source\nold game style pixel fonts.', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 7), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 8), 'abcdefghijklmnopqrstuvwxyz', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 9), '0123456789', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 6 + 16 * 11), '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'itch-io-cover.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')


def make_afdian_cover():
    font_x1 = _load_font(configs.font_config_map['thick'])
    font_x2 = _load_font(configs.font_config_map['thick'], 2)
    text_color = (255, 255, 255)
    shadow_color = (80, 80, 80)

    image = Image.open(os.path.join(path_define.images_dir, 'afdian-cover-background.png'))
    _draw_text(image, (image.width / 2, 18), 'Retro Pixel Font', font_x2, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 3), 'A set of open source\nold game style pixel fonts.', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 7), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 9), 'abcdefghijklmnopqrstuvwxyz', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 11), '0123456789', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    _draw_text(image, (image.width / 2, 18 + 16 * 13), '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', font_x1, text_color=text_color, shadow_color=shadow_color, is_horizontal_centered=True)
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(path_define.outputs_dir)
    image_file_path = os.path.join(path_define.outputs_dir, 'afdian-cover.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')
