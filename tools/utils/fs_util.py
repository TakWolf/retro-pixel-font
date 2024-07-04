import tomllib
from pathlib import Path
from typing import Any


def is_empty_dir(path: Path) -> bool:
    for item_path in path.iterdir():
        if item_path.name == '.DS_Store':
            continue
        return False
    return True


def read_toml(path: Path) -> Any:
    with path.open('rb') as file:
        return tomllib.load(file)
