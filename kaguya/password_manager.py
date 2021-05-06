from . import cli


def main():
    parser = cli.create_argparser()
    args = parser.parse_args()
    cli.HandleArgs(args)

    # TODO logic for handling args
