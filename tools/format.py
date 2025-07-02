from tools.configs.font import FontConfig
from tools.services import format_service


def main():
    for font_config in FontConfig.load().values():
        format_service.format_glyphs(font_config)


if __name__ == '__main__':
    main()
