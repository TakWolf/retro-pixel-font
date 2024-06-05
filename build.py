from scripts.configs import path_define, FontConfig
from scripts.services import font_service, publish_service, info_service, template_service, image_service
from scripts.utils import fs_util


def main():
    fs_util.delete_dir(path_define.outputs_dir)
    fs_util.delete_dir(path_define.releases_dir)

    font_configs = FontConfig.load_all()
    for font_config in font_configs.values():
        alphabet, character_mapping, glyph_files = font_service.collect_glyph_files(font_config)
        font_service.format_glyph_files(font_config, glyph_files)
        font_service.make_fonts(font_config, character_mapping, glyph_files)
        info_service.make_ofl_txt(font_config)
        info_service.make_info_txt(font_config)
        info_service.make_alphabet_txt(font_config, alphabet)
        image_service.make_preview_image(font_config)
        template_service.make_alphabet_html(font_config, alphabet)
        template_service.make_demo_html(font_config, alphabet)
    info_service.make_readme_txt()
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
