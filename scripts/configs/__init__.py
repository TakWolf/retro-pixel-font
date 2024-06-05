from scripts.configs import path_define
from scripts.configs.deploy import GitDeployConfig
from scripts.configs.font import FontConfig

font_version = '2024.05.12'

font_formats = ['otf', 'woff2', 'ttf', 'bdf', 'pcf']

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]
