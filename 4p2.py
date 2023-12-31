from collections import defaultdict
import math
import unittest

class MatchGame:
    def __init__(self, cardsText):
        self.gameLines = cardsText.split("\n")
        self.gameCopies = defaultdict(lambda: int(1))

    def getSuccessfulNumbers(self, gameText):
        (winningText, playerText) = gameText.split(" | ")
        winningNums = filter(lambda x: int(x), winningText.split())
        playerNums = filter(lambda x: int(x), playerText.split())
        return set(winningNums) & set(playerNums)

    def getGameNumber(self, line):
        (cardAndNum, gameText) = line.split(": ")
        return int(cardAndNum.split()[1])

    def getGameSuccesses(self, line):
        (cardAndNum, gameText) = line.split(": ")
        numSet = self.getSuccessfulNumbers(gameText)
        return len(numSet)
    
    def getCopyCount(self, gameNumber):
        return self.gameCopies[gameNumber]
    
    def incrementCopies(self, gameNumber, count):
        self.gameCopies[gameNumber] += count

    def incrementCopiesFromSuccess(self, gameNumber, successfulNumber):
        incrementNumber = self.getCopyCount(gameNumber)
        for i in range(1, successfulNumber+1):
            self.incrementCopies(gameNumber+i, incrementNumber)

    def applyGames(self):
        self.gameCopies = defaultdict(lambda: 1)
        for line in self.gameLines:
            if not line:
                continue
            gameNumber = self.getGameNumber(line)
            gameSuccesses = self.getGameSuccesses(line)
            self.incrementCopiesFromSuccess(gameNumber, gameSuccesses)
            # print("After {}, now copies={}".format(gameNumber, self.gameCopies))
        # print("+++ done, copies={}".format(self.gameCopies))
        return sum(self.gameCopies.values())

gameSample = MatchGame(open("4.txt").read())
gameReal = MatchGame(open("4real.txt").read())

class TestGuts(unittest.TestCase):
    def test_getSuccessfulNumbers(self):
        self.assertEqual(gameSample.getSuccessfulNumbers("41 48 83 86 17 | 83 86  6 31 17  9 48 53"), set(["48", "83", "17", "86"]))
        self.assertEqual(gameSample.getSuccessfulNumbers("13 32 20 16 61 | 61 30 68 82 17 32 24 19"), set(["32", "61"]))
        self.assertEqual(gameSample.getSuccessfulNumbers(" 1 21 53 59 44 | 69 82 63 72 16 21 14  1"), set(["1", "21"]))
        self.assertEqual(gameSample.getSuccessfulNumbers("41 92 73 84 69 | 59 84 76 51 58  5 54 83"), set(["84"]))
        self.assertEqual(gameSample.getSuccessfulNumbers("87 83 26 28 32 | 88 30 70 12 93 22 82 36"), set())
        self.assertEqual(gameSample.getSuccessfulNumbers("31 18 13 56 72 | 74 77 10 23 35 67 36 11"), set())

    def test_getGameSuccesses(self):
        self.assertEqual(gameSample.getGameSuccesses("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"), 4)
        self.assertEqual(gameSample.getGameSuccesses("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19"), 2)
        self.assertEqual(gameSample.getGameSuccesses("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1"), 2)
        self.assertEqual(gameSample.getGameSuccesses("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83"), 1)
        self.assertEqual(gameSample.getGameSuccesses("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36"), 0)
        self.assertEqual(gameSample.getGameSuccesses("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"), 0)

    def test_IncrementCopiesFromSuccess(self):
        self.assertEqual(gameSample.gameCopies, {})
        gameSample.incrementCopiesFromSuccess(1, 4)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 2, 4: 2, 5: 2})
        gameSample.incrementCopiesFromSuccess(2, 2)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 4, 4: 4, 5: 2})
        gameSample.incrementCopiesFromSuccess(3, 2)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 4, 4: 8, 5: 6})
        gameSample.incrementCopiesFromSuccess(4, 1)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 4, 4: 8, 5: 14})
        gameSample.incrementCopiesFromSuccess(5, 0)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 4, 4: 8, 5: 14})
        gameSample.incrementCopiesFromSuccess(6, 0)
        self.assertEqual(gameSample.gameCopies, {1: 1, 2: 2, 3: 4, 4: 8, 5: 14, 6: 1})
        
    def test_applyGames(self):
        self.assertEqual(gameSample.applyGames(), 30)

if __name__ == "__main__":
    print("real={}".format(gameReal.applyGames()))
    # print("sample={}".format(gameSample.applyGames()))
    # unittest.main()
    # print("start: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(1, 4)
    # print("after 1: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(2, 2)
    # print("after 2: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(3, 2)
    # print("after 3: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(4, 1)
    # print("after 4: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(5, 0)
    # print("after 4: {}".format(gameSample.gameCopies))
    # gameSample.incrementCopiesFromSuccess(6, 0)
    # print("after 4: {}".format(gameSample.gameCopies))
