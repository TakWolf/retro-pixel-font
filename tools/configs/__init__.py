from tools.configs.deploy import GitDeployConfig

font_version = '2024.05.12'

font_formats = ['otf', 'woff2', 'ttf', 'bdf', 'pcf']

git_deploy_configs = [GitDeployConfig(
    url='git@github.com:TakWolf/retro-pixel-font.git',
    remote_name='github',
    branch_name='gh-pages',
)]
