import unittest
import math

def getRaceCombos(time, distance):
    i = math.floor(time/2)
    j = math.ceil(time/2)
    victories = 0
    while True:
        if i * j <= distance:
            break
        victories+=1
        i-=1
        j+=1
    # if time is even, then the first victory
    # doesn't count for two
    if time % 2 == 0:
        return 1 + (victories-1)*2
    else:
        return victories*2

class Game:
    def __init__(self, filename):
        with open(filename) as inputFile:
            for line in inputFile:
                (label, data) = line.split(":")
                data = list(map(int, data.lstrip().split()))
                if label=="Time":
                    self.times=data
                elif label=="Distance":
                    self.distances=data
                else:
                    print(f"!!! Unexpected line token {label}")
        assert(self.times)
        assert(self.distances)
        assert(len(self.times)==len(self.distances))

    def __str__(self):
        tuples = []
        for time, distance in zip(self.times, self.distances):
            tuples.append(f"({time}, {distance})")
        return "Runs: " + " ".join(tuples)

    def run(self):
        sum = 1
        for time, distance in zip(self.times, self.distances):
            sum *= getRaceCombos(time, distance)
        return  sum

class TestGuts(unittest.TestCase):

    def test_getRaceCombos(self):
        self.assertEqual(getRaceCombos(7, 9), 4)
        self.assertEqual(getRaceCombos(15, 40), 8)
        self.assertEqual(getRaceCombos(30, 200), 9)

    def test_gameParse(self):
        g = Game("6.txt")
        self.assertEqual(str(g),"Runs: (7, 9) (15, 40) (30, 200)")
        
    def test_game(self):
        g = Game("6.txt")
        self.assertEqual(g.run(), 288)

if __name__=="__main__":
    # unittest.main()
    g = Game("6real.txt")
    print(f"real run={g.run()}")
