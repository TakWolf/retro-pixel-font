import os
import random

from jinja2 import Environment, FileSystemLoader

from configs import path_define
from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig
from utils.unidata_util import UnidataDB

build_random_key = random.random()

font_version = font_config.version

font_configs = FontConfig.loads()
font_config_map = {font_config.output_name: font_config for font_config in font_configs}

font_formats = ['otf', 'woff2', 'ttf']

unidata_db = UnidataDB(os.path.join(path_define.unidata_dir, 'Blocks.txt'))

template_env = Environment(loader=FileSystemLoader(path_define.templates_dir))

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]
