import unittest
from enum import Enum
from collections import defaultdict

cardToValue = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

class HandType(Enum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class Hand:
    def __init__(self, cards):
        assert(cards)
        assert(len(cards)==5)
        self.cards = cards
        self.handType = self.__GetHandType()

    def __str__(self):
        return self.cards
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.cards == other.cards
        return NotImplemented

    def __lt__(self, other):
        if self.handType != other.handType:
            return self.handType < other.handType
        # go through the cards, returning when we find
        # two that differ
        for i, j in zip(self.cards, other.cards):
            if i != j:
                return cardToValue[i] < cardToValue[j]


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

    def test_handSorting(self):
        testData = ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA", "AAQQA", "55555", "55A55"]
        testDataSorted = ["32T3K", "KTJJT", "KK677", "T55J5", "QQQJA", "AAQQA", "55A55", "55555"]
        hands = [Hand(x) for x in testData]
        handsSorted = [Hand(x) for x in testDataSorted]
        self.assertEqual(sorted(hands), handsSorted)

if __name__ == "__main__":
    unittest.main()
