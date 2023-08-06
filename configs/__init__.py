import random

from configs import path_define
from configs.font_config import FontConfig
from configs.git_deploy_config import GitDeployConfig

build_random_key = random.random()

font_formats = ['otf', 'woff2', 'ttf', 'bdf']

font_configs = FontConfig.loads()
outputs_name_to_config = {font_config.outputs_name: font_config for font_config in font_configs}

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]
