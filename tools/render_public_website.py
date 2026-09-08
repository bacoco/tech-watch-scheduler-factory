#!/usr/bin/env python3
"""Small wrapper around the factory website renderer."""
import sys
from tech_watch.cli import main


if __name__ == '__main__':
    raise SystemExit(main(['website-render', *sys.argv[1:]]))
