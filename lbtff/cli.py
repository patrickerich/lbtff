"""cli entry point lbtff.
Parse command line arguments in, invoke lbtff.
"""

import os
import sys
import re
import argparse
import textwrap
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
    if parsed_args.inc:
        re_includes = [re.compile(str(regex)) for regex in parsed_args.inc]
    if parsed_args.exc:
        re_excludes = [re.compile(str(regex)) for regex in parsed_args.exc]

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
        description='Line based text file filter',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'fileIn',
        help=wrap('input file name')
    )
    parser.add_argument(
        'fileOut',
        help=wrap('output file name')
    )
    parser.add_argument(
        '--inc',
        nargs='*',
        action='extend',
        help=wrap(
            'regular expression(s) determining INclusion of a line '
            'of the input file in the output file (non-dominant)\n'
            'multiple instances allowed'
        )
    )
    parser.add_argument(
        '--exc',
        action='extend',
        nargs='*',
        help=wrap(
            'regular expression(s) determining EXclusion of a line '
            'of the input file in the output file (dominant)\n'
            'multiple instances allowed'
        )
    )
    parser.add_argument('--version', action='version',
                        help='echo version number.',
                        version=f'{lbtff.version.get_version()}')
    return parser


def wrap(text, **kwargs):
    """Wrap lines in argparse so they align nicely in 2 columns.
    Default width is 70.
    With gratitude to paul.j3 https://bugs.python.org/issue12806
    """
    # apply textwrap to each line individually
    text = text.splitlines()
    text = [textwrap.fill(line, **kwargs) for line in text]
    return '\n'.join(text)
