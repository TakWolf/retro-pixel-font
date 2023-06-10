import datetime
import logging
import os
import shutil
import zipfile

import git

import configs
from configs import path_define, FontConfig
from utils import fs_util

logger = logging.getLogger('publish-service')


def make_release_zips():
    fs_util.make_dirs(path_define.releases_dir)
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
        logger.info(f"Make release zip: '{file_path}'")


def _copy_file(file_name: str, from_dir: str, to_dir: str):
    from_path = os.path.join(from_dir, file_name)
    to_path = os.path.join(to_dir, file_name)
    shutil.copyfile(from_path, to_path)
    logger.info(f"Copy from '{from_path}' to '{to_path}'")


def update_docs():
    fs_util.delete_dir(path_define.docs_dir)
    os.mkdir(path_define.docs_dir)
    _copy_file('readme-banner.png', path_define.outputs_dir, path_define.docs_dir)
    for font_config in configs.font_configs:
        fs_util.make_dirs(font_config.docs_dir)
        _copy_file('preview.png', font_config.outputs_dir, font_config.docs_dir)


def update_www():
    fs_util.delete_dir(path_define.www_dir)
    shutil.copytree(path_define.www_static_dir, path_define.www_dir)
    _copy_file('index.html', path_define.outputs_dir, path_define.www_dir)
    for font_config in configs.font_configs:
        fs_util.make_dirs(font_config.www_dir)
        _copy_file(f'{font_config.full_outputs_name}.woff2', font_config.outputs_dir, font_config.www_dir)
        _copy_file('alphabet.html', font_config.outputs_dir, font_config.www_dir)
        _copy_file('demo.html', font_config.outputs_dir, font_config.www_dir)


def deploy_www():
    repo = git.Repo.init(path_define.www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()}')
    current_branch_name = repo.git.branch(show_current=True)
    for git_deploy_config in configs.git_deploy_configs:
        repo.git.remote('add', git_deploy_config.remote_name, git_deploy_config.url)
        repo.git.push(git_deploy_config.remote_name, f'{current_branch_name}:{git_deploy_config.branch_name}', '-f')
