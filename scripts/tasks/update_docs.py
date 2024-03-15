from scripts.services import publish_service


def main():
    publish_service.update_readme_md()
    publish_service.update_docs()


if __name__ == '__main__':
    main()
