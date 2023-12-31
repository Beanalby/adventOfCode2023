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

    # splits the passed answer into 3 sections: the section below
    # this mapper, the section this mapper transformed, and the
    # section above this mapper.  Each could be None, but at least
    # one will be non-None
    def splitAnswer(self, answer):
        answerBelow = None
        transformed = None
        answerAbove = None

        # extract the section below, if any
        if answer[0] < self.sourceStart:
            answerBelow = (answer[0],
                           min(answer[1],
                               self.sourceStart - answer[0]))

        # extract the transformed section
        offset = self.destStart - self.sourceStart
        transformedStart = max(answer[0], self.sourceStart)+offset
        transformedEnd = min(answer[0]+answer[1],self.sourceStart+self.rangeLength)+offset
        if(transformedStart < transformedEnd):
            transformed = (transformedStart, transformedEnd-transformedStart)
        
        # extract the above section
        if answer[0]+answer[1] > self.sourceStart+self.rangeLength:
            aboveStart = max(answer[0], self.sourceStart+self.rangeLength)
            answerAbove = (aboveStart, (answer[1]+answer[0]) - aboveStart)

        return (answerBelow, transformed, answerAbove)

    def UselessApply(self, answerSet):
        answersNew = []
        for answer in answerSet:
            # if it's completely below our min, just passes through
            if answer[0]+answer[1] <= self.sourceStart:
                answersNew.append(answer)
                continue
            # if it's completely above our range, also straight through
            if self.sourceStart+self.rangeLength <= answer[0]:
                answersNew.append(answer)
                continue

            # there's overlap!
            # see if there's any below that passes through
            if answer[0] < self.sourceStart:
                answersNew.append((answer[0], self.sourceStart-answer[0]))
            # map the overlap
            
        return num + (self.destStart-self.sourceStart)

class TestGuts(unittest.TestCase):

    def test_normalizeAnswers(self):
        self.assertEqual(normalizeAnswerSet([(93, 1), (58, 53), (99, 83), (60, 65)]), [(58, 124)])
        self.assertEqual(normalizeAnswerSet([(79, 14), (55, 13)]), [(55, 13), (79, 14)])
        self.assertEqual(normalizeAnswerSet([(29, 24), (86, 82), (41, 3), (21, 15)]), [(21, 32), (86, 82)])

    def test_Mapper(self):
        m = Mapper(50, 98, 2)
        self.assertEqual(str(m), "98->100 to 50->52")
        # self.assertEqual(m.apply(98), 50)
        # self.assertEqual(m.apply(99), 51)
    def test_MapperSplit(self):
        # test the pen & paper version
        m = Mapper(50, 5, 5)

        self.assertEqual(m.splitAnswer((1,3)), ((1,3),None,None))
        self.assertEqual(m.splitAnswer((11, 2)), (None, None, (11,2)))
        self.assertEqual(m.splitAnswer((3, 10)), ((3,2), (50, 5), (10, 3)))
        self.assertEqual(m.splitAnswer((7, 5)), (None, (52, 3), (10, 2)))

        # test the first example
        m1 = Mapper(50, 98, 2)
        m2 = Mapper(52, 50, 48)
        self.assertEqual(m1.splitAnswer((79, 14)), ((79,14), None, None))
        self.assertEqual(m2.splitAnswer((79, 14)), (None, (81, 14), None))

if __name__=="__main__":
    # with open("5.txt") as inputFile:
    # with open("5real.txt") as inputFile:
    #     g = Game(inputFile.read())
    #     print(str(g))
    #     print("lowest={:,}".format(g.run()))
    unittest.main()
