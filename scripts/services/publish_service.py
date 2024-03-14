import datetime
import logging
import os
import shutil
import zipfile

import git

from scripts import configs
from scripts.configs import path_define, FontConfig
from scripts.utils import fs_util

logger = logging.getLogger('publish-service')


def make_release_zips():
    fs_util.make_dir(path_define.releases_dir)
    for font_format in configs.font_formats:
        file_path = os.path.join(path_define.releases_dir, f'{FontConfig.ZIP_OUTPUTS_NAME}-{font_format}-v{FontConfig.VERSION}.zip')
        with zipfile.ZipFile(file_path, 'w') as file:
            file.write(os.path.join(path_define.outputs_dir, 'readme.txt'), 'readme.txt')
            for font_config in configs.font_configs:
                font_file_name = f'{font_config.full_outputs_name}.{font_format}'
                file.write(os.path.join(font_config.outputs_dir, font_file_name), os.path.join(font_config.outputs_name, font_file_name))
                file.write(os.path.join(font_config.outputs_dir, 'OFL.txt'), os.path.join(font_config.outputs_name, 'OFL.txt'))
                file.write(os.path.join(font_config.outputs_dir, 'info.txt'), os.path.join(font_config.outputs_name, 'info.txt'))
                file.write(os.path.join(font_config.outputs_dir, 'preview.png'), os.path.join(font_config.outputs_name, 'preview.png'))
        logger.info("Make release zip: '%s'", file_path)


def _copy_file(file_name: str, dir_from: str, dir_to: str):
    path_from = os.path.join(dir_from, file_name)
    path_to = os.path.join(dir_to, file_name)
    shutil.copyfile(path_from, path_to)
    logger.info("Copy from '%s' to '%s'", path_from, path_to)


def update_docs():
    fs_util.delete_dir(path_define.docs_dir)
    os.mkdir(path_define.docs_dir)
    _copy_file('readme-banner.png', path_define.outputs_dir, path_define.docs_dir)
    for font_config in configs.font_configs:
        fs_util.make_dir(font_config.docs_dir)
        _copy_file('preview.png', font_config.outputs_dir, font_config.docs_dir)


def update_www():
    fs_util.delete_dir(path_define.www_dir)
    shutil.copytree(path_define.www_static_dir, path_define.www_dir)
    _copy_file('index.html', path_define.outputs_dir, path_define.www_dir)
    for font_config in configs.font_configs:
        fs_util.make_dir(font_config.www_dir)
        _copy_file(f'{font_config.full_outputs_name}.woff2', font_config.outputs_dir, font_config.www_dir)
        _copy_file('alphabet.html', font_config.outputs_dir, font_config.www_dir)
        _copy_file('demo.html', font_config.outputs_dir, font_config.www_dir)


def deploy_www():
    repo = git.Repo.init(path_define.www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {datetime.datetime.now(datetime.UTC).isoformat()}')
    current_branch_name = repo.git.branch(show_current=True)
    for git_deploy_config in configs.git_deploy_configs:
        repo.git.remote('add', git_deploy_config.remote_name, git_deploy_config.url)
        repo.git.push(git_deploy_config.remote_name, f'{current_branch_name}:{git_deploy_config.branch_name}', '-f')


def update_readme_md():
    preview_lines = []
    for font_config in configs.font_configs:
        preview_lines.append(f'### {font_config.name}')
        preview_lines.append('')
        info = f'尺寸：{font_config.size}px / 行高：{font_config.line_height}px · '
        info += f'[实时预览](https://retro-pixel-font.takwolf.com#font-{font_config.outputs_name}) · '
        info += f'[字母表](https://retro-pixel-font.takwolf.com/{font_config.outputs_name}/alphabet.html) · '
        info += f'[示例文本](https://retro-pixel-font.takwolf.com/{font_config.outputs_name}/demo.html)'
        preview_lines.append(info)
        preview_lines.append('')
        preview_lines.append(f'{font_config.readme_intro}')
        preview_lines.append('')
        preview_lines.append(f'![preview-{font_config.outputs_name}](docs/{font_config.outputs_name}/preview.png)')
        preview_lines.append('')

    file_path = os.path.join(path_define.project_root_dir, 'README.md')

    front_lines = []
    back_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
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

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(front_lines + preview_lines + back_lines))
        file.write('\n')
    logger.info("Update: 'README.md'")
