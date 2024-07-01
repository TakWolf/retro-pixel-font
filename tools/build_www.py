from tools.configs.font import FontConfig
from tools.services import font_service, template_service


def main():
    font_configs = FontConfig.load_all()
    for font_config in font_configs.values():
        alphabet, character_mapping, glyph_files = font_service.collect_glyph_files(font_config)
        font_service.format_glyph_files(font_config, glyph_files)
        font_service.make_fonts(font_config, character_mapping, glyph_files)
        template_service.make_alphabet_html(font_config, alphabet)
        template_service.make_demo_html(font_config, alphabet)
    template_service.make_index_html(font_configs)


if __name__ == '__main__':
    main()
