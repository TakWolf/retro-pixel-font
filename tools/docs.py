from tools.configs.font import FontConfig
from tools.services import publish_service


def main():
    publish_service.update_readme_md(FontConfig.load())
    publish_service.update_docs()


if __name__ == '__main__':
    main()
