from tools.configs.font import FontConfig
from tools.services import check_service


def main():
    for font_config in FontConfig.load().values():
        check_service.check_glyph_files(font_config)


if __name__ == '__main__':
    main()
