#!/usr/bin/env python3

"""A tool to generate figures of finite automata automatically from regular expressions."""

__author__ = "Taylor J. Smith"
__email__ = "tsmith@cs.queensu.ca"
__status__ = "Development"
__version__ = "0.4.0"

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

def generateTikzCode(stateTransitionList, startStateSet, finalStateSet):
    """Generate TikZ figure code for a given automaton."""
    code = ""

    # write preamble code
    code += "\\documentclass{article}\n\n\\usepackage{pgf}\n\\usepackage{tikz}\n\\usetikzlibrary{automata}\n\n\\begin{document}\n\n\\begin{tikzpicture}[->, auto, node distance = 2cm]\n"

    # write figure code
    code += generateTikzCodeStates(stateTransitionList, startStateSet, finalStateSet)
    code += "\n"
    code += generateTikzCodeTransitions(stateTransitionList)

    # write postamble code
    code += "\\end{tikzpicture}\n\n\\end{document}"

    return code

def generateTikzCodeStates(stateTransitionList, startStateSet, finalStateSet):
    """Generate TikZ figure code for states of an automaton."""
    stateCode = ""
    initStateList = []
    stateList = []

    # iterate through list of states
    for i in range(len(stateTransitionList)):
        # get "name" of current state
        currStateTransitionPair = stateTransitionList[i]
        currStateName = currStateTransitionPair[0]
        
        stateStatus = ""
        startStateFlag = False

        # determine initial state status
        if currStateName in startStateSet:
            stateStatus += "initial,"
            startStateFlag = True
        # default state string
        stateStatus += "state"
        # determine final state status
        if currStateName in finalStateSet:
            stateStatus += ",accepting"

        # generate code for current state
        # if state is initial, prepend code instead of appending (to put initial states first)
        if startStateFlag == True:
            stateCode = "\\node[" + stateStatus + "] (q" + currStateName + ") {$q_{" + currStateName + "}$};\n" + stateCode
        else:
            stateCode += "\\node[" + stateStatus + "] (q" + currStateName + ") {$q_{" + currStateName + "}$};\n"

        # keep track of ordering of states
        if startStateFlag == True:
            initStateList += ["q" + currStateName]
        else:
            stateList += ["q" + currStateName]

        # reset flag
        startStateFlag = False

    # combine two state ordering lists into one
    stateList = initStateList + stateList

    modStateCode = ""
    lineNum = 0

    # modify each line in state code to specify relative positioning
    for line in stateCode.splitlines():
        # if we are not looking at the first line of state code
        if lineNum != 0:
            # find the index in the line to insert the position code
            indexNum = line.find(")")

            # insert the position code (position current state to the right of previous state)
            line = line[:(indexNum + 1)] + " [right of=" + stateList[lineNum - 1] + "]" + line[(indexNum + 1):]
        
        # modify state code and move to next line
        modStateCode = modStateCode + line + "\n"
        lineNum = lineNum + 1

    stateCode = modStateCode

    return stateCode

def generateTikzCodeTransitions(stateTransitionList):
    """Generate TikZ figure code for transitions of an automaton."""
    transitionCode = ""

    # iterate through list of states
    for i in range(len(stateTransitionList)):
        # get "name" of current state and sublist of transitions
        currStateTransitionPair = stateTransitionList[i]
        currStateName = currStateTransitionPair[0]

        # if transitions from the current state exist
        # (that is, if the sublist of transitions has length greater than one)
        if len(currStateTransitionPair) > 1:
            # iterate through sublist of transitions
            for j in range(1, len(currStateTransitionPair)):
                # get "name" of state being transitioned to and transition symbol
                currTransition = currStateTransitionPair[j]
                nextStateName = currTransition[0]
                nextStateSymbol = currTransition[1]

                transitionStatus = ""
                
                # check if transition is a loop and, if so, handle styling appropriately
                if nextStateName == currStateName:
                    transitionStatus = "[loop above] "

                # generate code for current transition
                transitionCode += "\\path (q" + currStateName + ") edge " + transitionStatus + "node {" + nextStateSymbol + "} (q" + nextStateName + ");\n"

    return transitionCode

def getRegExp():
    """Get a regular expression as input."""
    # get regular expression as input
    regExp = input()
    return regExp

def parseFA(fa):
    """Parse the tokenized finite automaton for future processing."""
    # create lists to store states and transitions
    stateList = list()
    stateTransitionList = list()

    # create sets to store start states and final states
    startStateSet = set()
    finalStateSet = set()

    # loop through tokens
    for i in range(0, len(fa)):
        # determine start states
        if fa[i][0] == "(START)":
            startStateSet.add(fa[i][2])

        # determine final states
        if fa[i][2] == "(FINAL)":
            finalStateSet.add(fa[i][0])

        # add state to list if not already accounted for
        if (fa[i][0] not in stateList) and (fa[i][0] != "(START)"):
            stateList.append(fa[i][0])
            stateTransitionList.append([fa[i][0]])

        # associate transition with state in state list
        if (fa[i][2] != "(FINAL)"):
            for j in range(0, len(stateTransitionList)):
                if stateTransitionList[j][0] == fa[i][0]:
                    stateTransitionList[j].append([fa[i][2], fa[i][1]])

    return stateTransitionList, startStateSet, finalStateSet

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
    faParsed, startStateSet, finalStateSet = parseFA(fa)

    # generate TikZ figure code for automaton
    figCode = generateTikzCode(faParsed, startStateSet, finalStateSet)

    print(figCode)

if __name__ == "__main__":
    main()
