import unittest
from datetime import datetime
from math import lcm

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
                    # print(f"dirs: {self.dirs}")
                    continue
                if not line: # blank space after dirs
                    continue
                (nodeKey, nodeValue) = line.split(" = ")
                nodeValue = tuple(nodeValue[1:-1].split(", "))
                self.nodes[nodeKey] = nodeValue
                if nodeKey.endswith("A"):
                    self.startNodes.append(nodeKey)
                # print(f"{nodeKey}: {nodeValue}")
        # print (f"Starting at: {self.startNodes}")
        assert(self.dirs)
        assert(self.nodes)

    def walkStep(self, pos, direction):
        return self.nodes[pos][direction]

    def run(self):
        solutions=[]
        for start in self.startNodes:
            solution = self.getSolutions(start, 1)
            solutions.append(solution)
            print(f"for {start}: {solution}")
        print(f"solutions: {solutions}")
        print(f"lcm: {lcm(*solutions)}")

    def getSolutions(self, start, numSolutions):
        count=0
        i=0
        position=start
        solutions = []
        while(True):
            oldPosition = position
            position = self.walkStep(position, self.dirs[i])
            count+=1
            if position[2]=="Z":
                if numSolutions==1:
                    return count
                solutions.append(count)
                if len(solutions) >= numSolutions:
                    return solutions
            i = (i + 1) % len(self.dirs)

if __name__ == "__main__":
    # g = Guide("8sample2.txt")
    # g = Guide("8.txt")
    # g = Guide("8p2.txt")
    g = Guide("8real.txt")
    g.run()
    # print(f"Took {g.walk()} steps")
