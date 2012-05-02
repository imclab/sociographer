import importlib
import argparse
import json

import sociographer.commands

def main():
    parser = argparse.ArgumentParser(description="IRC social graph visualizer.")
    parser.add_argument('--config', '-c', metavar='CONFIG',
                        help="Global configuration file.", required=True)
    subparsers = parser.add_subparsers(help="sub-command help")

    for tool_name in sociographer.commands.__all__:
        tool = importlib.import_module("." + tool_name, "sociographer.commands")
        subparser = subparsers.add_parser(tool_name, help=tool.__help__)
        tool.configure_subparser(subparser)
        subparser.set_defaults(func=tool.main)

    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    args.func(args, config)

if __name__ == "__main__":
    main()

