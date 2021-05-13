import os
import sys

from loguru import logger

from . import cli
from .constants import DB_FILE


def main():
    parser = cli.create_argparser()
    args = parser.parse_args(sys.argv[1:])  # pass the argvs in explicity for testing
    logger.debug(args)
    handler = cli.ArgsHandler(args)
    handler.dispatch()

    # os.remove(DB_FILE)  # for testing only
