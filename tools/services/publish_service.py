import shutil
import zipfile
from pathlib import Path

from loguru import logger

from tools import configs
from tools.configs import path_define
from tools.configs.font import FontConfig


def make_release_zips(font_configs: dict[str, FontConfig]):
    path_define.releases_dir.mkdir(parents=True, exist_ok=True)

    for font_format in configs.font_formats:
        file_path = path_define.releases_dir.joinpath(f'retro-pixel-font-{font_format}-v{configs.font_version}.zip')
        with zipfile.ZipFile(file_path, 'w') as file:
            file.write(path_define.project_root_dir.joinpath('LICENSE-OFL'), 'OFL.txt')
            for font_config in font_configs.values():
                outputs_arc = Path(font_config.outputs_name)
                font_file_name = f'retro-pixel-{font_config.outputs_name}.{font_format}'
                file.write(font_config.outputs_dir.joinpath(font_file_name), outputs_arc.joinpath(font_file_name))
                file.write(font_config.outputs_dir.joinpath('preview.png'), outputs_arc.joinpath('preview.png'))
        logger.info("Make release zip: '{}'", file_path)


def update_readme_md(font_configs: dict[str, FontConfig]):
    preview_lines = []
    for font_config in font_configs.values():
        preview_lines.append(f'### {font_config.name}')
        preview_lines.append('')
        info = f'尺寸：{font_config.font_size}px / 行高：{font_config.line_height}px · '
        info += f'[实时预览](https://retro-pixel-font.takwolf.com#font-{font_config.outputs_name}) · '
        info += f'[字母表](https://retro-pixel-font.takwolf.com/{font_config.outputs_name}/alphabet.html) · '
        info += f'[示例文本](https://retro-pixel-font.takwolf.com/{font_config.outputs_name}/demo.html)'
        preview_lines.append(info)
        preview_lines.append('')
        preview_lines.append(f'![preview-{font_config.outputs_name}](docs/{font_config.outputs_name}/preview.png)')
        preview_lines.append('')

    file_path = path_define.project_root_dir.joinpath('README.md')

    front_lines = []
    back_lines = []
    with file_path.open('r', encoding='utf-8') as file:
        current_lines = front_lines
        for line in file.readlines():
            line = line.rstrip()
            if line == '可以通过 [主页](https://retro-pixel-font.takwolf.com) 实时预览字体效果。':
                current_lines.append(line)
                current_lines.append('')
                current_lines = None
            elif current_lines is None and line.startswith('## '):
                current_lines = back_lines
                current_lines.append(line)
            elif current_lines is not None:
                current_lines.append(line)
        current_lines.append('')

    file_path.write_text('\n'.join(front_lines + preview_lines + back_lines), 'utf-8')
    logger.info("Update: 'README.md'")


def update_docs():
    if path_define.docs_dir.exists():
        shutil.rmtree(path_define.docs_dir)

    for file_dir, _, file_names in path_define.outputs_dir.walk():
        for file_name in file_names:
            if file_name not in ('preview.png', 'readme-banner.png'):
                continue
            path_from = file_dir.joinpath(file_name)
            path_to = path_define.docs_dir.joinpath(path_from.relative_to(path_define.outputs_dir))
            path_to.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path_from, path_to)
            logger.info("Copy file: '{}' -> '{}'", path_from, path_to)
