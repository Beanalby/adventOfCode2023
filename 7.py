import unittest
from enum import Enum
from collections import defaultdict

class HandType(Enum):
    HighCard = 1,
    OnePair = 2,
    TwoPair = 3,
    ThreeOfAKind = 4,
    FullHouse = 5,
    FourOfAKind = 6,
    FiveOfAKind = 7


class Hand:
    def __init__(self, cards):
        assert(cards)
        assert(len(cards)==5)
        self.cards = cards
        self.handType = self.__GetHandType()

    def __GetHandType(self):
        # split the cards into their counts
        cardDict = defaultdict(int)
        for card in self.cards:
            cardDict[card]+=1
        cardCounts = sorted(list(cardDict.values()), reverse=True)

        # figure out type based on the most frequent card(s)
        if cardCounts[0]==5:
            return HandType.FiveOfAKind
        if cardCounts[0]==4:
            return HandType.FourOfAKind
        if cardCounts[0:2]== [3,2]:
            return HandType.FullHouse
        if cardCounts[0] == 3:
            return HandType.ThreeOfAKind
        if cardCounts[0:2] == [2,2]:
            return HandType.TwoPair
        if cardCounts[0] == 2:
            return HandType.OnePair
        return HandType.HighCard

        print(f"dict={cardDict}, counts={cardCounts}")
        
class TestGuts(unittest.TestCase):

    def test_handType(self):
        testData = [
            ("32T3K", HandType.OnePair),
            ("T55J5", HandType.ThreeOfAKind),
            ("KK677", HandType.TwoPair),
            ("KTJJT", HandType.TwoPair),
            ("QQQJA", HandType.ThreeOfAKind),
            ("AAQQA", HandType.FullHouse),
            ("55555", HandType.FiveOfAKind),
            ("55A55", HandType.FourOfAKind)
        ]
        for testCase in testData:
            self.assertEqual(Hand(testCase[0]).handType, testCase[1])

if __name__ == "__main__":
    unittest.main()
