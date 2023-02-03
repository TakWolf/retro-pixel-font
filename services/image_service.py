import logging
import math
import os

from PIL import Image, ImageFont, ImageDraw

from utils import fs_util

logger = logging.getLogger('image-service')


def _load_font(font_config):
    font_file_path = os.path.join(font_config.outputs_dir, f'{font_config.full_output_name}.woff2')
    return ImageFont.truetype(font_file_path, font_config.px)


def _draw_text(image, xy, text, font, text_color=(0, 0, 0), line_height=None, line_gap=0, is_horizontal_centered=False, is_vertical_centered=False):
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
    draw.text((x, y), text, fill=text_color, font=font, spacing=spacing)


def make_preview_image_file(font_config, demo_text):
    font = _load_font(font_config)
    background_color = (30, 144, 255)
    text_color = (255, 255, 255)

    content_width = 0
    for demo_line in demo_text:
        line_width = math.ceil(font.getlength(demo_line))
        if line_width > content_width:
            content_width = line_width
    content_height = font_config.line_height_px * len(demo_text)

    image = Image.new('RGBA', (font_config.px * 2 + content_width, font_config.px * 2 + content_height), background_color)
    cursor_x = font_config.px
    cursor_y = font_config.px
    for demo_line in demo_text:
        _draw_text(image, (cursor_x, cursor_y), demo_line, font, text_color=text_color)
        cursor_y += font_config.line_height_px
    image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)

    fs_util.make_dirs_if_not_exists(font_config.outputs_dir)
    image_file_path = os.path.join(font_config.outputs_dir, 'preview.png')
    image.save(image_file_path)
    logger.info(f'make {image_file_path}')
