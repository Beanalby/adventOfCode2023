import unittest

class Guide:
    def __init__(self, filename):
        self.filename = filename
        self.parse()

    def parse(self):
        self.dirs = None
        self.nodes = {}
        
        with open(self.filename) as inputFile:
            for line in inputFile.read().splitlines():
                # first line is directions
                if not self.dirs:
                    self.dirs = line
                    continue
                if not line:
                    continue
                (nodeKey, nodeValue) = line.split(" = ")
                nodeValue = tuple(nodeValue[1:-1].split(", "))
                self.nodes[nodeKey] = nodeValue
                print(f"{nodeKey}: {nodeValue}")
        assert(self.dirs)
        assert(self.nodes)

    def walk(self):
        count=0
        i=0
        pos="AAA"

        while(True):
            oldPos = pos
            val = self.nodes[pos]
            if self.dirs[i]=="L":
                pos = val[0]
            else:
                pos = val[1]
            count+=1
            print(f"step #{count}: {oldPos} -> {self.dirs[i]}@{val} = {pos}")
            if pos == "ZZZ":
                return count

            i = (i + 1) % len(self.dirs)

if __name__ == "__main__":
    # g = Guide("8sample2.txt")
    g = Guide("8real.txt")
    print(f"Took {g.walk()} steps")
