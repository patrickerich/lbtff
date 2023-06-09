"""cli entry point lbtff.
Parse command line arguments in, invoke lbtff.
"""

import os
import sys
import re
import math
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
    # TBD: Elegant solution for in-string quotes
    re_includes = None
    re_excludes = None
    if parsed_args.inc_re:
        re_includes = [re.compile(str(regex)) for regex in parsed_args.inc_re]
    if parsed_args.exc_re:
        re_excludes = [re.compile(str(regex)) for regex in parsed_args.exc_re]

    # Determine total number of lines in input file
    num_lines = sum(1 for _ in open(parsed_args.fileIn))
    linenr_width = math.ceil(math.log10(num_lines))
    linenr = 0

    # Process the input file and write the output file
    with open(parsed_args.fileIn,  'r') as fpIn, open(parsed_args.fileOut, 'w') as fpOut:
        for line in fpIn:
            linenr += 1
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
                if parsed_args.print_linenr:
                    fpOut.write(f'{linenr:{linenr_width}} :  ')
                fpOut.write(f'{line}\n')


def get_args(args):
    """Parse arguments passed in from shell"""
    return get_parser().parse_args(args)


def get_parser():
    """Return ArgumentParser for lbtff cli"""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        description=(
            textwrap.fill(
                'Line based text file filter that utilizes '
                'Python\'s regular expression module (re).',
                width=70,
            )
        ),
        epilog=(
            textwrap.fill(
                'IMPORTANT NOTE: '
                'The regular expressions should be in quotes '
                '(preceded and followed by quotation marks). '
                'Both "RE" and \'RE\' are allowed. '
                'Should the regular expression itself contain similar '
                'quotation marks (as those used to surround it), then '
                'they need to be escaped by preceding them with a '
                'backslash (\\).',
                width=70,
                replace_whitespace=False
            )
        ),
        formatter_class=(
            lambda prog: argparse.RawDescriptionHelpFormatter(
                prog,
                max_help_position=40,
                width=70,
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
        nargs=1,
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
        nargs=1,
        action='extend',
        help=(
            'Regular expression determining EXclusion of a line '
            'of the input file in the output file (dominant). '
            'Multiple instances of this argument are effectively OR-ed.'
        ),
    )
    parser.add_argument(
        '-pl', '--print-linenr',
        action='store_true',
        help=(
            'Precede every matched line with the line number of the '
            'match in the original file.'
        ),
    )
    return parser
