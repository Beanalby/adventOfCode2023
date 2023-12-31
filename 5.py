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

    def doesMapperApply(self, num):
        return num >= self.sourceStart \
            and num < self.sourceStart+self.rangeLength

    def apply(self, num):
        if not self.doesMapperApply(num):
            error = "num {} shouldn't be used in mapper {}-{}"\
                .format(num, self.sourceStart, self.sourceStart+self.rangeLength)
            raise ValueError(error)
        return num + (self.destStart-self.sourceStart)

class TestGuts(unittest.TestCase):
    def test_Mapper(self):
        m = Mapper(50, 98, 2)
        self.assertEqual(m.doesMapperApply(-1), False)
        self.assertEqual(m.doesMapperApply(0), False)
        self.assertEqual(m.doesMapperApply(1), False)
        self.assertEqual(m.doesMapperApply(49), False)
        self.assertEqual(m.doesMapperApply(50), False)
        self.assertEqual(m.doesMapperApply(51), False)
        self.assertEqual(m.doesMapperApply(97), False)
        self.assertEqual(m.doesMapperApply(98), True)
        self.assertEqual(m.doesMapperApply(99), True)
        self.assertEqual(m.doesMapperApply(100), False)

        self.assertEqual(m.apply(98), 50)
        self.assertEqual(m.apply(99), 51)

if __name__=="__main__":
    unittest.main()
