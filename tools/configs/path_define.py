from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..', '..').resolve()

ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
GLYPHS_DIR = ASSETS_DIR.joinpath('glyphs')
TEMPLATES_DIR = ASSETS_DIR.joinpath('templates')
IMAGES_DIR = ASSETS_DIR.joinpath('images')

BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
OUTPUTS_DIR = BUILD_DIR.joinpath('outputs')
RELEASES_DIR = BUILD_DIR.joinpath('releases')

DOCS_DIR = PROJECT_ROOT_DIR.joinpath('docs')
