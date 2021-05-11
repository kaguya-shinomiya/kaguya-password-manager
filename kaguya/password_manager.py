import os

from loguru import logger

from . import cli
from .constants import DB_FILE


def main():
    parser = cli.create_argparser()
    args = parser.parse_args()
    logger.debug(args)
    handler = cli.ArgsHandler(args)
    handler.dispatch()

    os.remove(DB_FILE)  # for testing only
