__help__ = "Generate graph from synopsis file."

from sociographer import graph

def configure_subparser(parser):
    parser.add_argument('--output', '-o', metavar='FILE',
                        help="File to output to.")
    parser.add_argument('filename', metavar='FILE',
                        help="Synopsis file to use.")

def main(args, config):
    graph.generate_dot(args.filename, args.output, **config)

