from __future__ import print_function

from argparse import ArgumentParser

from .gen import generate, runUI

__version__ = '0.5.0'

def main():
    parser = ArgumentParser()
    parser.add_argument('command', choices=['compile', 'run'],
        help="The command to execute")
    parser.add_argument('source',
        help="Path of the UI script to convert")
    parser.add_argument('dest', nargs='?',
        help="Destination path for the resulting Objective-C file (compile only)")
    parser.add_argument('--loc-table', dest='loc_table',
        help="Name of the localization table to use for NSLocalizedStringFromTable().")
    args = parser.parse_args()
    if args.command == 'compile':
        if not args.dest:
            print("The compile command requires a <dest> argument.")
            return 1
        generate(args.source, args.dest, localizationTable=args.loc_table)
    else:
        runUI(args.source)
