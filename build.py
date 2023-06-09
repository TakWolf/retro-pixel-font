import logging

import configs
from configs import path_define
from services import font_service, publish_service, info_service, template_service, image_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    for font_config in configs.font_configs:
        font_service.format_glyph_files(font_config)
        alphabet, character_mapping, glyph_file_paths = font_service.collect_glyph_files(font_config)
        font_service.make_font_files(font_config, character_mapping, glyph_file_paths)
        info_service.make_ofl_txt_file(font_config)
        info_service.make_info_txt_file(font_config)
        info_service.make_alphabet_txt_file(font_config, alphabet)
        image_service.make_preview_image_file(font_config)
        template_service.make_alphabet_html_file(font_config, alphabet)
        template_service.make_demo_html_file(font_config, alphabet)
    info_service.make_readme_txt_file()
    publish_service.make_release_zips()
    template_service.make_index_html_file()
    template_service.make_itch_io_details_html_file()
    image_service.make_readme_banner()
    image_service.make_github_banner()
    image_service.make_itch_io_banner()
    image_service.make_itch_io_cover()
    image_service.make_afdian_cover()


if __name__ == '__main__':
    main()
