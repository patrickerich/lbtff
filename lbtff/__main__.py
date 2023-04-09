"""
Default execution entry point if running the package via python -m
"""
import lbtff.cli
import sys


def main():
    """Run lbtff from script entry point."""
    return lbtff.cli.main()


if __name__ == '__main__':
    sys.exit(main())
