from __future__ import print_function

from argparse import ArgumentParser

from .gen import generate, runUI

def main():
    parser = ArgumentParser()
    parser.add_argument('command', choices=['compile', 'run'],
        help="The command to execute")
    parser.add_argument('source',
        help="Path of the UI script to convert")
    parser.add_argument('dest', nargs='?',
        help="Destination path for the resulting Objective-C file (compile only)")
    args = parser.parse_args()
    if args.command == 'compile':
        if not args.dest:
            print("The compile command requires a <dest> argument.")
            return 1
        generate(args.source, args.dest)
    else:
        runUI(args.source)
