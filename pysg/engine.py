from typing import Protocol

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pysg.config import Config


class Renderer(Protocol):
    def render(self, template: str, context: dict | None = None) -> str:
        ...


class FileSystemRenderer(Renderer):
    def __init__(self, config: Config):
        self.engine = Environment(loader=FileSystemLoader(config.templates_dir), autoescape=select_autoescape())

    def render(self, template: str, context: dict | None = None) -> str:
        return self.engine.get_template(template).render(context or {})
