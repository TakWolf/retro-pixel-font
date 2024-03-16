from scripts.configs import path_define
from scripts.configs.font_config import FontConfig
from scripts.configs.git_deploy_config import GitDeployConfig

font_formats = ['otf', 'woff2', 'ttf', 'bdf']

font_configs = FontConfig.loads()
outputs_name_to_config = {font_config.outputs_name: font_config for font_config in font_configs}

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]
