from collections import defaultdict
import math
import unittest

def getSuccessfulNumbers(gameText):
    (winningText, playerText) = gameText.split(" | ")
    winningNums = filter(lambda x: int(x), winningText.split())
    playerNums = filter(lambda x: int(x), playerText.split())
    return set(winningNums) & set(playerNums)

def getGameSuccesses(line):
    (cardAndNum, gameText) = line.split(": ")
    numSet = getSuccessfulNumbers(gameText)
    if len(numSet) == 0:
        return 0
    else:
        return math.pow(2, len(numSet)-1)

def sumGames(gameData):
    total = 0
    for line in gameData.split("\n"):
        if not line:
            continue
        total += getGameSuccesses(line.rstrip())
    return total

gameSample = open("4.txt").read()
gameReal = open("4real.txt").read()

class TestGuts(unittest.TestCase):
    def test_getSuccessfulNumbers(self):
        self.assertEqual(getSuccessfulNumbers("41 48 83 86 17 | 83 86  6 31 17  9 48 53"), set(["48", "83", "17", "86"]))
        self.assertEqual(getSuccessfulNumbers("13 32 20 16 61 | 61 30 68 82 17 32 24 19"), set(["32", "61"]))
        self.assertEqual(getSuccessfulNumbers(" 1 21 53 59 44 | 69 82 63 72 16 21 14  1"), set(["1", "21"]))
        self.assertEqual(getSuccessfulNumbers("41 92 73 84 69 | 59 84 76 51 58  5 54 83"), set(["84"]))
        self.assertEqual(getSuccessfulNumbers("87 83 26 28 32 | 88 30 70 12 93 22 82 36"), set())
        self.assertEqual(getSuccessfulNumbers("31 18 13 56 72 | 74 77 10 23 35 67 36 11"), set())

    def test_getGameSuccesses(self):
        self.assertEqual(getGameSuccesses("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"), 8)
        self.assertEqual(getGameSuccesses("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"), 2)
        self.assertEqual(getGameSuccesses("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"), 2)
        self.assertEqual(getGameSuccesses("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"), 1)
        self.assertEqual(getGameSuccesses("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"), 0)
        self.assertEqual(getGameSuccesses("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"), 0)

    def test_sumGames(self):
        self.assertEqual(sumGames(gameSample), 13)

if __name__ == "__main__":
    # unittest.main()
    print("real={}".format(sumGames(gameReal)))
