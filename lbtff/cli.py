"""cli entry point lbtff.
Parse command line arguments in, invoke lbtff.
"""

import os
import sys
import re
import argparse
import lbtff.version


def main(args=None):
    """Entry point for lbtff cli.
    The setup_py entry_point wraps this in sys.exit already so this effectively
    becomes sys.exit(main()).
    The __main__ entry point similarly wraps sys.exit().
    """

    # Get the cli arguments
    if args is None:
        args = ['--help', ]
        if len(sys.argv) > 1:
            args = sys.argv[1:]

    # Parse the cli arguments
    parsed_args = get_args(args)

    # Verify source file
    if not os.path.isfile(parsed_args.fileIn):
        print(f'error: {parsed_args.fileIn} does not exist')
        sys.exit(1)

    # Verify destination file
    if os.path.isfile(parsed_args.fileOut):
        print(f'{parsed_args.fileOut} exists. Override (y/n)?:', end=' ')
        reply = input().strip().lower()
        if reply[0] != 'y':
            sys.exit(1)

    # Compile any regular expressions
    re_includes = None
    re_excludes = None
    if parsed_args.inc_re:
        re_includes = [re.compile(str(regex)) for regex in parsed_args.inc_re]
    if parsed_args.exc_re:
        re_excludes = [re.compile(str(regex)) for regex in parsed_args.exc_re]

    # Process the input file and write the output file
    with open(parsed_args.fileIn,  'r') as fpIn, open(parsed_args.fileOut, 'w') as fpOut:
        for line in fpIn:
            line = line.rstrip()
            include = True
            exclude = False
            if re_includes:
                include = False
                for regex in re_includes:
                    if regex.search(line):
                        include = True
            if re_excludes:
                for regex in re_excludes:
                    if regex.search(line):
                        exclude = True
            if include and not exclude:
                fpOut.write(f"{line}\n")


def get_args(args):
    """Parse arguments passed in from shell"""
    return get_parser().parse_args(args)


def get_parser():
    """Return ArgumentParser for lbtff cli"""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=(
            'Line based text file filter.'
            'Utilizes Python\'s regular expression module'
        ),
        formatter_class=(
            lambda prog: argparse.HelpFormatter(
                prog,
                max_help_position=80,
                width=100,
            )
        ),
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        help='Echo version number.',
        version=f'{lbtff.version.get_version()}',
    )
    parser.add_argument(
        'fileIn',
        type=str,
        help=('Input file'),
    )
    parser.add_argument(
        'fileOut',
        type=str,
        help=('Output file'),
    )
    parser.add_argument(
        '-i', '--inc-re',
        type=str,
        action='extend',
        help=(
            'Regular expression determining INclusion of a line '
            'of the input file in the output file (non-dominant). '
            'Multiple instances of this argument are effectively OR-ed.'
        ),
    )
    parser.add_argument(
        '-e', '--exc-re',
        type=str,
        action='extend',
        help=(
            'Regular expression determining EXclusion of a line '
            'of the input file in the output file (dominant). '
            'Multiple instances of this argument are effectively OR-ed.'
        ),
    )
    return parser
