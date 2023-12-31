import re
import unittest

def isDigit(c):
    return c >= '0' and c <= '9'

class Board:
    def __init__(self, boardText):
        self.height = boardText.count("\n")
        self.width = boardText.index("\n")
        self.boardLines = boardText.split("\n")
        self.patternPart = re.compile("[0-9]+")
        self.patternSymbol = re.compile("[^0-9.]")

    def getLine(self, lineNum):
        return self.boardLines[lineNum]

    def getExpandedNumber(self, lineNum, pos):

        # if we're outside the bounds, nothing to expand
        if lineNum < 0 or lineNum >= self.height:
            return []
        if pos < 0 or pos >= self.width:
            return []

        line = self.getLine(lineNum)
        # if we're not on a digit, nothing to expand
        if not isDigit(line[pos]):
            return []
        
        # start with just this character...
        startPos=pos
        endPos=pos+1
        
        # expand startPos left while there are more digits
        while True:
            if(startPos == 0):
                break
            prevChar = line[startPos-1:startPos]
            if(not isDigit(prevChar)):
                break
            # prevChar is a number, include it
            startPos-=1

        # expand endPos right while there are more digits
        while True:
            if(endPos == self.width):
                break
            nextChar = line[endPos:endPos+1]
            if(not isDigit(nextChar)):
                break
            # nextChar is a number, include it
            endPos+=1

        return [int(line[startPos:endPos])]

    # get 1-2 numbers above or below a given position
    # lineNum: the line above or below the gear
    # pos: the horizontal position of the gear
    def getSurroundingVerticalNumbers(self, lineNum, pos):
        # the only time we'll have two numbers is if
        # BOTH pos-1 & pos+1 are numbers,
        # and pos ISN'T a number.  Handle that case first
        line = self.getLine(lineNum)
        
        # only check special case if we're not on the left/right edge
        if pos!=0 and pos != self.width-1:
            if isDigit(line[pos-1]) \
               and not isDigit(line[pos]) \
               and isDigit(line[pos+1]):
                # special case!
                return self.getExpandedNumber(lineNum, pos-1) \
                    + self.getExpandedNumber(lineNum, pos+1)

        # not the 2-number case, just look for A number.
        # we know we can stop as soon as we find one, because
        # we know we handled all the multi-number cases above
        if pos > 0 and isDigit(line[pos-1]):
            return self.getExpandedNumber(lineNum, pos-1)
        if isDigit(line[pos]):
            return self.getExpandedNumber(lineNum, pos)
        if pos < self.width and isDigit(line[pos+1]):
            return self.getExpandedNumber(lineNum, pos+1)
        # no digits in any of the 3 spots
        return []

    def getSurroundingNumbers(self, lineNum, pos):
        return self.getSurroundingVerticalNumbers(lineNum-1, pos) \
            + self.getExpandedNumber(lineNum, pos-1) \
            + self.getExpandedNumber(lineNum, pos+1) \
            + self.getSurroundingVerticalNumbers(lineNum+1, pos)

boardSample = Board(open("3.txt").read())
boardTest = Board(open("3test.txt").read())
boardReal = Board(open("3real.txt").read())

class TestGuts(unittest.TestCase):
    def test_getExpandedNumber(self):
        self.assertEqual(boardTest.getExpandedNumber(-1,-1),[])
        self.assertEqual(boardTest.getExpandedNumber(-1,0),[])
        self.assertEqual(boardTest.getExpandedNumber(-1,1),[])

        self.assertEqual(boardTest.getExpandedNumber(0,-1),[])
        self.assertEqual(boardTest.getExpandedNumber(0,0),[467])
        self.assertEqual(boardTest.getExpandedNumber(0,1),[467])
        self.assertEqual(boardTest.getExpandedNumber(0,2),[467])
        self.assertEqual(boardTest.getExpandedNumber(0,3),[])
        self.assertEqual(boardTest.getExpandedNumber(0,4),[])
        self.assertEqual(boardTest.getExpandedNumber(0,5),[114])
        self.assertEqual(boardTest.getExpandedNumber(0,6),[114])
        self.assertEqual(boardTest.getExpandedNumber(0,7),[114])
        self.assertEqual(boardTest.getExpandedNumber(0,8),[])
        self.assertEqual(boardTest.getExpandedNumber(0,9),[])
        self.assertEqual(boardTest.getExpandedNumber(0,10),[])

        self.assertEqual(boardTest.getExpandedNumber(2,2),[35])
        self.assertEqual(boardTest.getExpandedNumber(2,3),[35])

        self.assertEqual(boardTest.getExpandedNumber(10,6),[5984])
        self.assertEqual(boardTest.getExpandedNumber(10,7),[5984])
        self.assertEqual(boardTest.getExpandedNumber(10,8),[5984])
        self.assertEqual(boardTest.getExpandedNumber(10,9),[5984])

    def test_getSurroundingVerticalNumbers(self):
        self.assertEqual(boardTest.getSurroundingVerticalNumbers(0, 3), [467])
        self.assertEqual(boardTest.getSurroundingVerticalNumbers(0, 4), [114])
        self.assertEqual(boardTest.getSurroundingVerticalNumbers(2, 3), [35])
        self.assertEqual(boardTest.getSurroundingVerticalNumbers(5, 3), [])
        self.assertEqual(boardTest.getSurroundingVerticalNumbers(9, 4), [664, 598])

    def test_getSurroundingNumbers(self):
        self.assertEqual(boardTest.getSurroundingNumbers(1, 3), [467,35])
        self.assertEqual(boardTest.getSurroundingNumbers(1, 4), [114,35])
        self.assertEqual(boardTest.getSurroundingNumbers(4, 3), [617])
        self.assertEqual(boardTest.getSurroundingNumbers(5, 5), [592])

def doThing():
    print("0,0={}".format(board.getExpandedNumber(10, 9)))
    # print("total={}".format(board.getPartTotal()))

if __name__=="__main__":
    unittest.main()
    # doThing()
