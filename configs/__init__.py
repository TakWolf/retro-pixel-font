from jinja2 import Environment, FileSystemLoader

from configs import path_define
from configs.git_deploy_config import GitDeployConfig

font_formats = ['otf', 'woff2', 'ttf']

template_env = Environment(loader=FileSystemLoader(path_define.templates_dir))

git_deploy_configs = [GitDeployConfig(
    'git@github.com:TakWolf/retro-pixel-font.git',
    'github',
    'gh-pages',
)]
