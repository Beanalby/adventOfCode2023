import unittest

# Game contains multiple Stage instances
#
# soil-to-fertilizer map: <- Stage instance
# 0 15 37 <- Mapper instance
# 37 52 2
# 39 0 15

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

class Stage:
    def __init__(self, name):
        self.name = name
        self.mappers = set()
    def __str__(self):
        sortedMappers = sorted(self.mappers)
        s = self.name + ":";
        for m in sortedMappers:
            s += "\n" + str(m)
        return s
        
    def addMapper(self, mapper):
        self.mappers.add(mapper)

    def apply(self, num):
        for m in self.mappers:
            if m.isCorrectMapper(num):
                return m.apply(num)
        # no mapper were right, leave as-is
        return num

class Game:
    def __init__(self):
        self.stages = []

    def __str__(self):
        s = "{} stages:".format(len(self.stages))
        for stage in self.stages:
            s += "\n\n" + str(stage)
        return s

    def addStage(self, stage):
        self.stages.append(stage)

    def apply(self, num):
        for s in self.stages:
            num = s.apply(num)
        return num

    def parse(text):
        pass

class TestGuts(unittest.TestCase):

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

    def test_Stage(self):
        s = Stage("seed-to-soil")
        s.addMapper(Mapper(52, 50, 48))
        s.addMapper(Mapper(50, 98, 2))
        self.assertEqual(str(s), "seed-to-soil:\n50->98 to 52->100\n98->100 to 50->52")

        testCases = [ [0, 0], [1, 1], [48, 48], [49, 49], [50, 52], [51, 53], \
                     [52, 54], [96, 98], [97, 99], [98, 50], [99, 51], [100, 100]]
        for testCase in testCases:
            (testInput, testOutput) = testCase
            self.assertEqual(s.apply(testInput), testOutput)

    def test_Game(self):
        g = Game()

        s1 = Stage("seed-to-soil")
        g.addStage(s1)
        s1.addMapper(Mapper(50, 98, 2))
        s1.addMapper(Mapper(52, 50, 48))

        s2 = Stage("soil-to-fertilizer")
        g.addStage(s2)
        s2.addMapper(Mapper(0, 15, 37))
        s2.addMapper(Mapper(37, 52, 2))
        s2.addMapper(Mapper(39, 0, 15))

        self.assertEqual(str(g), "2 stages:\n\nseed-to-soil:\n50->98 to 52->100\n98->100 to 50->52\n\nsoil-to-fertilizer:\n0->15 to 39->54\n15->52 to 0->37\n52->54 to 37->39")

        testCases = [ [79, 81], [14, 53], [55, 57], [13, 52] ]
        for testCase in testCases:
            (testInput, testOutput) = testCase
            self.assertEqual(g.apply(testInput), testOutput)

if __name__=="__main__":
    unittest.main()
