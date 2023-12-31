import math
import re

class Board:
    def __init__(self, boardText):
        self.height = boardText.count("\n")
        self.width = boardText.index("\n")
        self.boardLines = boardText.split("\n")
        self.patternPart = re.compile("[0-9]+")
        self.patternSymbol = re.compile("[^0-9.]")
        
    # returns true if the specified span contains a symbol
    def spanContainsSymbol(self, lineNum, startPos, endPos):
        if (lineNum < 0 or lineNum >= self.height):
            return False
        # don't start with a negative number
        startPos = max(0, startPos)
        section = self.boardLines[lineNum][startPos:endPos]
        return self.patternSymbol.search(section) != None

    # returns true if any of the surrounding text contains a symbol
    def spanNextToSymbol(self, lineNum, startPos, endPos):
        # breakpoint()
        # check above
        if self.spanContainsSymbol(lineNum-1, startPos-1, endPos+1):
            return True

        # check this same line, one space before & after
        if self.spanContainsSymbol(lineNum, startPos-1, startPos):
            return True
        if self.spanContainsSymbol(lineNum, endPos, endPos+1):
            return True

        # check below
        if self.spanContainsSymbol(lineNum+1, startPos-1, endPos+1):
            return True

        # no symbols!
        return False

    def getPartTotal(self):
        total = 0
        for (lineNum, line) in enumerate(self.boardLines):
            # find all the partnumbers on this line
            for match in self.patternPart.finditer(line):
                if self.spanNextToSymbol(lineNum, match.start(), match.end()):
                    total += int(match.group())
        return total


if __name__=="__main__":
    # breakpoint()
    # with open("3.txt") as inputFile:
    with open("3real.txt") as inputFile:
        board = Board(inputFile.read())
        print("total={}".format(board.getPartTotal()))

    print("Done.")

# pattern = re.compile("\d+")
# for match in pattern.finditer("467..114.."):
#     print("match {} is at ({},{})".format(match.group(),match.start(),match.end()))
