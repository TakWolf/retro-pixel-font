import datetime
import logging
import os
import shutil

import git

import configs
from configs import path_define
from utils import fs_util

logger = logging.getLogger('publish-service')


def _copy_file(file_name, from_dir, to_dir):
    from_path = os.path.join(from_dir, file_name)
    to_path = os.path.join(to_dir, file_name)
    shutil.copyfile(from_path, to_path)
    logger.info(f'copy from {from_path} to {to_path}')


def update_docs():
    _copy_file('README.md', path_define.outputs_dir, path_define.project_root_dir)
    fs_util.delete_dir(path_define.docs_dir)
    os.mkdir(path_define.docs_dir)
    for font_config in configs.font_configs:
        fs_util.make_dirs_if_not_exists(font_config.docs_dir)
        _copy_file('preview.png', font_config.outputs_dir, font_config.docs_dir)


def update_www():
    fs_util.delete_dir(path_define.www_dir)
    shutil.copytree(path_define.www_static_dir, path_define.www_dir)
    for font_config in configs.font_configs:
        fs_util.make_dirs_if_not_exists(font_config.www_dir)
        _copy_file(f'{font_config.full_output_name}.woff2', font_config.outputs_dir, font_config.www_dir)
        _copy_file('alphabet.html', font_config.outputs_dir, font_config.www_dir)


def deploy_www():
    repo = git.Repo.init(path_define.www_dir)
    repo.git.add(all=True)
    repo.git.commit(m=f'deployed at {datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()}')
    current_branch_name = repo.git.branch(show_current=True)
    for git_deploy_config in configs.git_deploy_configs:
        repo.git.remote('add', git_deploy_config.remote_name, git_deploy_config.url)
        repo.git.push(git_deploy_config.remote_name, f'{current_branch_name}:{git_deploy_config.branch_name}', '-f')
