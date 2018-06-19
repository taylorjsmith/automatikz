#!/usr/bin/env python3

"""A tool to generate figures of finite automata automatically from regular expressions."""

__author__ = "Taylor J. Smith"
__email__ = "tsmith@cs.queensu.ca"
__status__ = "Development"
__version__ = "0.3.0"

###############
# Imports
###############

import subprocess
import sys

###############
# Constants
###############

GRAIL_PATH = "/usr/local/bin/Grail-3.4.4"

###############
# Methods
###############

def convertRegExpToFA(re):
    """Convert a regular expression to a textual representation of a finite automaton."""
    # construct command string pointing to Grail tool
    command = GRAIL_PATH + "/bin/retofm"

    # send command to terminal
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8")

    # send regular expression as input and obtain output/error
    (stdoutData, stderrData) = process.communicate(re)

    # check if error occurred during command call
    if (stderrData is not ""):
        print("Error:", stderrData)
        sys.exit(1)

    return stdoutData

def getRegExp():
    """Get a regular expression as input."""
    # get regular expression as input
    regExp = input()
    return regExp

def parseFA(fa):
    """Parse the tokenized finite automaton for future processing."""
    # loop through tokens
    for i in range(0, len(fa)):
        print(fa[i])

        # determine start states
        if fa[i][0] == "(START)":
            print("Start state is " + fa[i][2])

        # determine final states
        if fa[i][2] == "(FINAL)":
            print("Final state is " + fa[i][0])

def tokenizeFA(fa):
    """Tokenize the textual representation of a finite automaton."""
    # split textual representation on whitespace
    faList = fa.split()

    # use list comprehension to create individual sublists for each transition
    # each sublist is of length three (start state, transition symbol, end state)
    faList = [faList[i:i+3] for i in range(0, len(faList), 3)]

    return faList

def main():
    """Main method."""
    # get regular expression as input
    re = getRegExp()

    # convert regular expression to textual representation of automaton
    fa = convertRegExpToFA(re)

    # tokenize textual representation of automaton
    fa = tokenizeFA(fa)

    # parse tokenized automaton to extract certain data for future use
    parseFA(fa)

if __name__ == "__main__":
    main()
