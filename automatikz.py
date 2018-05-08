#!/usr/bin/env python3

"""A tool to generate figures of finite automata automatically from regular expressions."""

__author__ = "Taylor J. Smith"
__email__ = "tsmith@cs.queensu.ca"
__status__ = "Development"
__version__ = "0.1.0"

def getRegExp():
    """Get a regular expression as input."""
    regExp = input()
    return regExp

def main():
    """Main method."""
    re = getRegExp()
    print(re)

if __name__ == "__main__":
    main()
