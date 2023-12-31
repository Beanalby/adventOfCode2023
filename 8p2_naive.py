import unittest
from datetime import datetime

class Guide:
    def __init__(self, filename):
        self.filename = filename
        self.parse()

    def parse(self):
        self.dirs = None
        self.nodes = {}
        self.startNodes = []

        with open(self.filename) as inputFile:
            for line in inputFile.read().splitlines():
                # first line is directions
                if not self.dirs:
                    self.dirs = list(map(lambda x: 0 if x=="L" else 1, line))
                    continue
                if not line: # blank space after dirs
                    continue
                (nodeKey, nodeValue) = line.split(" = ")
                nodeValue = tuple(nodeValue[1:-1].split(", "))
                self.nodes[nodeKey] = nodeValue
                if nodeKey.endswith("A"):
                    self.startNodes.append(nodeKey)
                print(f"{nodeKey}: {nodeValue}")
        print (f"Starting at: {self.startNodes}")
        assert(self.dirs)
        assert(self.nodes)

    def walkStep(self, pos, direction):
        return self.nodes[pos][direction]

    def walk(self):
        count=0
        i=0
        positions=self.startNodes

        while(True):
            oldPositions = positions
            positions = list(map(lambda x: self.walkStep(x, self.dirs[i]), positions))
            if count % 1000000 == 0:
                print("\n{}: {: 10,}: ".format(datetime.now().strftime("%Y:%m:%d %H:%M:%S"), count), end="", flush=True)
            # if count % 10000 == 0:
            #     # for sanity, print the number currently on z
            #     num = len(list(filter(lambda x: x[2]!="Z",  positions)))
            #     print(f"{num}", end="", flush=True)
            count+=1

            # print("--------------------")
            # for (oldPos, pos) in zip(oldPositions, positions):
            #     print(f"step #{count}: {oldPos} -> {self.dirs[i]}@{self.nodes[oldPos]} = {pos}")
            
            # if none of the current positions DON'T end in Z, we're done
            if not any(filter(lambda x: x[2]!="Z",  positions)):
                return count
            # +++ if ANY of them ARE z, print it?
            num = len(list(filter(lambda x: x[2]!="Z",  positions)))
            if num <=  3:
                print(f"{num}", end="", flush=True)

            i = (i + 1) % len(self.dirs)

if __name__ == "__main__":
    # g = Guide("8sample2.txt")
    # g = Guide("8.txt")
    # g = Guide("8p2.txt")
    g = Guide("8real.txt")
    print(f"Took {g.walk()} steps")
