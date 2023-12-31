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

    def expandNumber(self, lineNum, pos):
        startPos=pos
        endPos=pos+1
        
        while True:
            if(startPos == 0):
                break
            prevChar = self.boardLines[lineNum][startPos-1:startPos]
            if(not isDigit(prevChar)):
                break
            # prevChar is a number, include it
            startPos-=1

        while True:
            if(endPos == self.width):
                break
            nextChar = self.boardLines[lineNum][endPos:endPos+1]
            if(not isDigit(nextChar)):
                break
            # nextChar is a number, include it
            endPos+=1
        return int(self.boardLines[lineNum][startPos:endPos])


boardSample = Board(open("3.txt").read())
boardTest = Board(open("3test.txt").read())
boardReal = Board(open("3real.txt").read())

class TestGuts(unittest.TestCase):
    def testExpandNumber(self):
        self.assertEqual(boardTest.expandNumber(0,0),467)
        self.assertEqual(boardTest.expandNumber(0,1),467)
        self.assertEqual(boardTest.expandNumber(0,2),467)
        self.assertEqual(boardTest.expandNumber(0,5),114)
        self.assertEqual(boardTest.expandNumber(0,6),114)
        self.assertEqual(boardTest.expandNumber(0,7),114)

        self.assertEqual(boardTest.expandNumber(2,2),35)
        self.assertEqual(boardTest.expandNumber(2,3),35)

        self.assertEqual(boardTest.expandNumber(10,6),5984)
        self.assertEqual(boardTest.expandNumber(10,7),5984)
        self.assertEqual(boardTest.expandNumber(10,8),5984)
        self.assertEqual(boardTest.expandNumber(10,9),5984)

def doThing():
    print("0,0={}".format(board.expandNumber(10, 9)))
    # print("total={}".format(board.getPartTotal()))

if __name__=="__main__":
    unittest.main()
    # doThing()
