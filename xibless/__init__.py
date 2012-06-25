from argparse import ArgumentParser

from .gen import generate

def main():
    parser = ArgumentParser()
    parser.add_argument('source',
        help="Path of the UI script to convert")
    parser.add_argument('dest',
        help="Destination path for the resulting Objective-C file")
    args = parser.parse_args()
    generate(args.source, args.dest)
