import http.server
import os
import shutil
import socketserver
import sys
import tomllib
from distutils.dir_util import copy_tree
from time import perf_counter

import typer
from loguru import logger

from pysg.config import load
from pysg.engine import FileSystemRenderer

app = typer.Typer()


@app.command()
def serve(port: int = 8000):
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


@app.command()
def build():
    start = perf_counter()
    try:
        config = load()
    except FileNotFoundError:
        logger.error("the configuration file 'config.toml' was not found. Please verify it exists at the root level")
        sys.exit()

    destination_path = config.out_dir
    fs = FileSystemRenderer(config)

    logger.info(f"🏁 Start building {config.name}")

    clean_dist(destination_path)

    for page in os.scandir(config.templates_dir):
        if page.is_file():
            with open(os.path.join(destination_path, page.name), "w") as fd:
                data = parse_data(page, config.data_dir)
                logger.info(f"📃Render '{page.name}'")
                fd.write(fs.render(page.name, data))

    logger.info("⏩ Copy staticfiles to build")
    copy_tree(config.static_dir, os.path.join(config.out_dir))

    end = perf_counter()
    logger.info(f"🎉 Done… in {(end - start) * 1000:.2f} ms")


def parse_data(page: os.DirEntry, data_dir: str) -> dict:
    data_file_path = os.path.join(data_dir, f"{page.name.split('.')[0]}.toml")
    data = {}
    if os.path.isfile(data_file_path):
        with open(data_file_path, "rb") as f:
            data = tomllib.load(f)
    return data


def clean_dist(destination_path: str):
    if os.path.exists(destination_path) and os.path.isdir(destination_path):
        shutil.rmtree(destination_path)
    os.mkdir(destination_path)


if __name__ == "__main__":
    app()
