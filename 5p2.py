import unittest
from datetime import datetime

# Game contains multiple Stage instances
#
# soil-to-fertilizer map: <- Stage instance
# 0 15 37 <- Mapper instance
# 37 52 2
# 39 0 15

def normalizeAnswerSet(answerSet):
    answerSorted = sorted(answerSet, key=lambda x: x[0])
    answerCurrent = None
    answersNew = []
    for answer in answerSorted:
        if not answerCurrent:
            answerCurrent = answer
            continue
        if answerCurrent[1] >= answer[0]:
            # answer gets consumed into answerCurrent
            # expand answer's maxRange if necessary
            newStart = min(answer[0],answerCurrent[0])
            newEnd = max(answer[1],answerCurrent[1])
            answerCurrent = (newStart, newEnd)
        else:
            # this new answer set outside of answerCurrent,
            # the latter isn't going to change anymore
            answersNew.append(answerCurrent)
            answerCurrent=answer
    if answerCurrent:
        answersNew.append(answerCurrent)
    return answersNew

class Mapper:
    def __init__(self, destStart, sourceStart, sourceEnd):
        self.destStart=destStart
        self.sourceStart=sourceStart
        self.sourceEnd=sourceEnd

    def __lt__(self, other):
        return self.sourceStart < other.sourceStart

    def __str__(self):
        return "{}->{} to {}->{}"\
            .format(self.sourceStart,self.sourceEnd,
                    self.destStart, self.destStart+(self.sourceEnd-self.sourceStart))

    # splits the passed answer into 3 sections: the section below
    # this mapper, the section this mapper transformed, and the
    # section above this mapper.  Each could be None, but at least
    # one will be non-None
    def splitAnswer(self, answer):
        answerBelow = None
        answerTransformed = None
        answerAbove = None

        # extract the section below, if any
        if answer[0] < self.sourceStart:
            answerBelow = (answer[0], min(answer[1], self.sourceStart))

        # extract the transformed section
        offset = self.destStart - self.sourceStart
        transformedStart = max(answer[0], self.sourceStart)+offset
        transformedEnd = min(answer[1],self.sourceEnd)+offset
        if(transformedStart < transformedEnd):
            answerTransformed = (transformedStart, transformedEnd)

        # extract the above section
        if answer[1] > self.sourceEnd:
            answerAbove = (max(answer[0], self.sourceEnd), answer[1])

        assert(answerBelow!=None \
               or answerTransformed!=None \
               or answerAbove!=None)

        return (answerBelow, answerTransformed, answerAbove)

class Stage:
    def __init__(self, name):
        self.name = name
        self.mappers = []
    def __str__(self):
        s = self.name + ":";
        for m in self.mappers:
            s += "\n" + str(m)
        return s

    def addMapper(self, mapper):
        self.mappers.append(mapper)
        self.mappers.sort()

    def apply(self, answerSet):
        answersForOtherMappers = []
        answerOutput = []
        # run the answer set through each of the mappers
        for mapper in self.mappers:
            # run each of the answers through this mapper
            # anything transformed goes to the output,
            # anything before/after is still fother for other mappers
            for answer in answerSet:
                (answerBefore, answerTransformed, answerAfter) = mapper.splitAnswer(answer)
                if answerBefore:
                    answersForOtherMappers.append(answerBefore)
                if answerAfter:
                    answersForOtherMappers.append(answerAfter)
                if answerTransformed:
                    answerOutput.append(answerTransformed)

            # this mapper's done, take everything this mapper didn't
            # use and prep it for the other mappers
            answerSet = normalizeAnswerSet(answersForOtherMappers)
            answersForOtherMappers=[]

        # anything left in answerSet when we're done with all mappers
        # gets passed through as-is
        return normalizeAnswerSet(answerOutput + answerSet)

class TestGuts(unittest.TestCase):

    def test_normalizeAnswers(self):
        self.assertEqual(normalizeAnswerSet([(93, 94), (58, 111), (99, 182), (60, 125)]), [(58, 182)])
        self.assertEqual(normalizeAnswerSet([(79, 93), (55, 68)]), [(55, 68), (79, 93)])
        self.assertEqual(normalizeAnswerSet([(29, 53), (86, 168), (41, 44), (21, 37)]), [(21, 53), (86, 168)])
        self.assertEqual(normalizeAnswerSet([(1, 50), (50, 52), (52, 100)]), [(1, 100)])

    def test_Mapper(self):
        m = Mapper(50, 98, 100)
        self.assertEqual(str(m), "98->100 to 50->52")
        # self.assertEqual(m.apply(98), 50)
        # self.assertEqual(m.apply(99), 51)

    def test_MapperSplit(self):
        # test the pen & paper version
        m = Mapper(50, 5, 10)

        self.assertEqual(m.splitAnswer((1,4)), ((1,4),None,None))
        self.assertEqual(m.splitAnswer((11, 13)), (None, None, (11,13)))
        self.assertEqual(m.splitAnswer((3, 13)), ((3,5), (50, 55), (10, 13)))
        self.assertEqual(m.splitAnswer((7, 12)), (None, (52, 55), (10, 12)))

        # test the first example
        m1 = Mapper(50, 98, 100)
        m2 = Mapper(52, 50, 98)
        self.assertEqual(m1.splitAnswer((79, 93)), ((79,93), None, None))
        self.assertEqual(m2.splitAnswer((79, 93)), (None, (81, 95), None))

    def test_Stage(self):
        s = Stage("seed-to-soil")
        s.addMapper(Mapper(50, 98, 100))
        s.addMapper(Mapper(52, 50, 98))
        self.assertEqual(s.apply([(79, 93)]), [(81, 95)])
        self.assertEqual(s.apply([(79, 93),(55,68)]), [(57,70),(81, 95)])
        self.assertEqual(s.apply([(1, 98)]), [(1,50),(52,100)])

if __name__=="__main__":
    # with open("5.txt") as inputFile:
    # with open("5real.txt") as inputFile:
    #     g = Game(inputFile.read())
    #     print(str(g))
    #     print("lowest={:,}".format(g.run()))
    unittest.main()
