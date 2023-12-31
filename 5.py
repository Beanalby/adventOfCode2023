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
    def __init__(self, text):
        self.stages = []
        self.seeds = set()

        if text:
            self.parse(text)

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

    def parse(self, text):
        currentStage=None
        for line in text.split("\n"):
            if not line:
                currentStage=None
                continue

            if line.startswith("seeds: "):
                self.seeds = set(map(int, line.split(": ")[1].split(" ")))
                continue

            if line.endswith(" map:"):
                currentStage = Stage(line.split(" ")[0])
                self.addStage(currentStage)
                continue

            # should be line of digits parsing a stage
            assert currentStage
            (destStart, sourceStart, rangeLength) = map(int, line.split(" "))
            currentStage.addMapper(Mapper(destStart, sourceStart, rangeLength))

    def run(self):
        lowestLocation = float("inf")
        print("------------------------------")
        for seed in self.seeds:
            location = self.apply(seed)
            print("seed {:,} gives {:,}".format(seed, location))
            lowestLocation = min(location, lowestLocation)
        return lowestLocation

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
        g = Game(None)

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

    def test_GameParse(self):
        g = None
        with open("5.txt") as inputFile:
            g = Game(inputFile.read())
        self.assertEqual(str(g), "7 stages:\n\nseed-to-soil:\n50->98 to 52->100\n98->100 to 50->52\n\nsoil-to-fertilizer:\n0->15 to 39->54\n15->52 to 0->37\n52->54 to 37->39\n\nfertilizer-to-water:\n0->7 to 42->49\n7->11 to 57->61\n11->53 to 0->42\n53->61 to 49->57\n\nwater-to-light:\n18->25 to 88->95\n25->95 to 18->88\n\nlight-to-temperature:\n45->64 to 81->100\n64->77 to 68->81\n77->100 to 45->68\n\ntemperature-to-humidity:\n0->69 to 1->70\n69->70 to 0->1\n\nhumidity-to-location:\n56->93 to 60->97\n93->97 to 56->60")

if __name__=="__main__":
    # with open("5.txt") as inputFile:
    with open("5real.txt") as inputFile:
        g = Game(inputFile.read())
        print(str(g))
        print("lowest={:,}".format(g.run()))
    # unittest.main()
