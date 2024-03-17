from scripts.configs import path_define
from scripts.configs.font import FontConfig
from scripts.configs.deploy import GitDeployConfig

font_configs = FontConfig.load_all()

font_formats = ['otf', 'woff2', 'ttf', 'bdf']

git_deploy_config = GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)
