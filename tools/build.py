import shutil

from tools.configs import path_define
from tools.configs.font import FontConfig
from tools.services import font_service, publish_service, template_service, image_service


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)

    font_configs = FontConfig.load()
    for font_config in font_configs.values():
        alphabet, character_mapping, glyph_files = font_service.collect_glyph_files(font_config)
        font_service.format_glyph_files(font_config, glyph_files)
        font_service.make_fonts(font_config, character_mapping, glyph_files)
        image_service.make_preview_image(font_config)
        template_service.make_alphabet_html(font_config, alphabet)
        template_service.make_demo_html(font_config, alphabet)
    publish_service.make_release_zips(font_configs)
    template_service.make_index_html(font_configs)
    template_service.make_itch_io_details_html(font_configs)
    image_service.make_readme_banner(font_configs)
    image_service.make_github_banner(font_configs)
    image_service.make_itch_io_banner(font_configs)
    image_service.make_itch_io_cover(font_configs)
    image_service.make_afdian_cover(font_configs)


if __name__ == '__main__':
    main()
