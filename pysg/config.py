import tomllib
from dataclasses import dataclass

NAME = "name"


@dataclass(frozen=True)
class Config:
    name: str
    static_dir: str
    data_dir: str
    out_dir: str
    templates_dir: str


def load() -> Config:
    with open("config.toml", "rb") as f:
        raw_config = tomllib.load(f)
        return Config(
            name=raw_config[NAME],
            static_dir="assets",
            data_dir="data",
            out_dir="dist",
            templates_dir="pages",
        )
