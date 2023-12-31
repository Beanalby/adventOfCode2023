import unittest
from enum import Enum
from collections import defaultdict

cardToValue = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
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

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Hand:
    def __init__(self, cards, score=0):
        assert(cards)
        assert(len(cards)==5)
        self.score = score
        self.cards = cards
        self.handType = self.__GetHandType()

    def __str__(self):
        s = str(self.handType) + ": " + self.cards
        if self.score:
            s += " @ " + str(self.score)
        return s
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
        print("+++ " + self.cards)
        # if self.cards == "JJJJJ":
        #     breakpoint()
        # split the cards into their counts
        cardDict = defaultdict(int)
        j=0
        for card in self.cards:
            if card == "J":
                j+=1
            else:
                cardDict[card]+=1
        if not cardDict:
            # no non-joker cards, must be JJJJJ
            return HandType.FiveOfAKind

        cardCounts = sorted(list(cardDict.values()), reverse=True)

        # figure out type based on the most frequent card(s)
        if cardCounts[0]+j ==5:
            return HandType.FiveOfAKind
        if cardCounts[0]+j ==4:
            return HandType.FourOfAKind
        if [cardCounts[0]+j,cardCounts[1]] == [3,2]:
            return HandType.FullHouse
        if cardCounts[0]+j == 3:
            return HandType.ThreeOfAKind
        if [cardCounts[0]+j,cardCounts[1]] == [2,2]:
            return HandType.TwoPair
        if cardCounts[0]+j == 2:
            return HandType.OnePair
        return HandType.HighCard

        print(f"dict={cardDict}, counts={cardCounts}")

class Game:
    def __init__(self, filename):
        self.filename = filename

    def run(self):
        hands = []
        with open(self.filename) as inputFile:
            for line in inputFile.read().splitlines():
                (cards, score) = line.split()
                hands.append(Hand(cards, int(score)))
        hands.sort()

        total = 0
        for (i, hand) in enumerate(hands):
            total += (i+1) * hand.score
        return total

class TestGuts(unittest.TestCase):

    def test_handType(self):
        testData = [
            ("32T3K", HandType.OnePair),
            ("T55J5", HandType.FourOfAKind),
            ("KK677", HandType.TwoPair),
            ("KTJJT", HandType.FourOfAKind),
            ("QQQJA", HandType.FourOfAKind),
            ("AAQQA", HandType.FullHouse),
            ("55555", HandType.FiveOfAKind),
            ("55A55", HandType.FourOfAKind)
        ]
        for testCase in testData:
            self.assertEqual(Hand(testCase[0]).handType, testCase[1])

    def test_handSorting(self):
        testData = ["32T3K", "T55J5", "KK677", "KTJJT", "QQQJA", "AAQQA", "55555", "55A55"]
        testDataSorted = ["32T3K", "KK677", "AAQQA", "55A55", "T55J5", "QQQJA", "KTJJT", "55555" ]
        hands = [Hand(x) for x in testData]
        handsSorted = [Hand(x) for x in testDataSorted]
        self.assertEqual(sorted(hands), handsSorted)

    def test_game(self):
        self.assertEqual(Game("7.txt").run(), 5905)

if __name__ == "__main__":
    # unittest.main()
    print("total=" + str(Game("7real.txt").run()))
