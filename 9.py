
def makeNextSequence(seq):
    return [j-i for i, j in zip(seq, seq[1:])]

def makeSequences(sequence):
    sequences = [sequence]
    while True:
        nextSequence = makeNextSequence(sequences[-1])
        sequences.append(nextSequence)
        # if it's all zeroes, we're done
        if(not list(filter(lambda x:x!=0, nextSequence))):
            return sequences

def addNextColumn(sequences):
    sequences[-1].append(0)
    for sequence, nextSequence in zip(reversed(sequences), reversed(sequences[0:-1])):
        # print("------------------------------\n")
        # print(f"doing:\n {sequence}\n{nextSequence}\n")
        nextSequence.append(sequence[-1]+nextSequence[-1])
        # print(f"now:\n {sequence}\n{nextSequence}\n")
    return sequences

def getNextNum(sequence):
    # print("==============================\n")
    sequences = makeSequences(sequence)
    sequences = addNextColumn(sequences)
    return sequences[0][-1]

def doAdvent(filename):
    total = 0
    with open(filename) as inputFile:
        for line in inputFile.read().splitlines():
            sequence = list(map(int, line.split(" ")))
            nextNum = getNextNum(sequence)
            total += nextNum
            print("{} -> {} total={}".format(sequence, nextNum, total))
    print(f"total={total}")


# doAdvent("9.txt")
doAdvent("9real.txt")
