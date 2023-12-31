import unittest
from datetime import datetime

# Game contains multiple Stage instances
#
# soil-to-fertilizer map: <- Stage instance
# 0 15 37 <- Mapper instance
# 37 52 2
# 39 0 15

def normalizeAnswerSet(answerSet):
    # breakpoint()
    answerSorted = sorted(answerSet, key=lambda x: x[0])
    answerCurrent = None
    answersNew = []
    for answer in answerSorted:
        if not answerCurrent:
            answerCurrent = answer
            continue
        if answerCurrent[0]+answerCurrent[1] > answer[0]:
            # answer gets consumed into answerCurrent
            # expand answer's maxRange if necessary
            newBase = min(answer[0],answerCurrent[0])
            newMax = max(answer[0]+answer[1],answerCurrent[0]+answerCurrent[1])
            answerCurrent = (newBase, newMax-newBase)
        else:
            # this new answer set outside of answerCurrent,
            # the latter isn't going to change anymore
            answersNew.append(answerCurrent)
            answerCurrent=answer
    if answerCurrent:
        answersNew.append(answerCurrent)
    return answersNew

class Mapper:
    def __init__(self, destStart, sourceStart, rangeLength):
        self.destStart=destStart
        self.sourceStart=sourceStart
        self.rangeLength=rangeLength

    def __lt__(self, other):
        return self.sourceStart < other.sourceStart

    def __str__(self):
        return "{}->{} to {}->{}"\
            .format(self.sourceStart,self.sourceStart+self.rangeLength,
                    self.destStart, self.destStart+self.rangeLength)

    def isCorrectMapper(self, num):
        return num >= self.sourceStart \
            and num < self.sourceStart+self.rangeLength

    def apply(self, num):
        if not self.isCorrectMapper(num):
            error = "num {} shouldn't be used in mapper {}-{}"\
                .format(num, self.sourceStart, self.sourceStart+self.rangeLength)
            raise ValueError(error)
        return num + (self.destStart-self.sourceStart)

class TestGuts(unittest.TestCase):

    def test_normalizeAnswers(self):
        self.assertEqual(normalizeAnswerSet([(93, 1), (58, 53), (99, 83), (60, 65)]), [(58, 124)])
        self.assertEqual(normalizeAnswerSet([(79, 14), (55, 13)]), [(55, 13), (79, 14)])
        self.assertEqual(normalizeAnswerSet([(29, 24), (86, 82), (41, 3), (21, 15)]), [(21, 32), (86, 82)])

    def test_Mapper(self):
        m = Mapper(50, 98, 2)
        self.assertEqual(str(m), "98->100 to 50->52")
        self.assertEqual(m.isCorrectMapper(-1), False)
        self.assertEqual(m.isCorrectMapper(0), False)
        self.assertEqual(m.isCorrectMapper(1), False)
        self.assertEqual(m.isCorrectMapper(49), False)
        self.assertEqual(m.isCorrectMapper(50), False)
        self.assertEqual(m.isCorrectMapper(51), False)
        self.assertEqual(m.isCorrectMapper(97), False)
        self.assertEqual(m.isCorrectMapper(98), True)
        self.assertEqual(m.isCorrectMapper(99), True)
        self.assertEqual(m.isCorrectMapper(100), False)

        self.assertEqual(m.apply(98), 50)
        self.assertEqual(m.apply(99), 51)

if __name__=="__main__":
    # with open("5.txt") as inputFile:
    # with open("5real.txt") as inputFile:
    #     g = Game(inputFile.read())
    #     print(str(g))
    #     print("lowest={:,}".format(g.run()))
    unittest.main()