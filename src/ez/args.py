from argparse import ArgumentParser
from pathlib import Path


parser = ArgumentParser(
    description="The EZ Web Framework Server",
    epilog="Powered by EZ Web Framework",
)

parser.add_argument(
    "--host",
    default="localhost",
    help="The host to bind to",
)

parser.add_argument(
    "--port",
    default=8000,
    type=int,
    help="The port to bind to",
)

parser.add_argument(
    "--sitedir",
    default=".",
    type=Path,
    nargs="?",
    help="The directory to serve",
)


class Args:
    host: str
    port: int
    sitedir: Path


import sys
args: Args
args, unparsed_args = parser.parse_known_args(sys.argv[1:])
del sys

del parser
del ArgumentParser
del Path
del Args
