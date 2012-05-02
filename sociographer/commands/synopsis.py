import importlib
import json

from sociographer import synopsis
from sociographer import formats

__help__ = "Generate synopsis files."

def configure_subparser(parser):
    parser.add_argument('--output', '-o', metavar='FILE',
                        help="File to output to.")
    parser.add_argument('filename', metavar='FILE',
                        help="Log file to use.")

def main(args, config):
    fmt = importlib.import_module("." + config['format'], "sociographer.formats")
    synopsis.generate_json(fmt, args.filename, args.output, **config['context'])

