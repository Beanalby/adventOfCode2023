sum=0
wordNumbers = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9
}

def processLine(line):
    firstNumIndex=float('inf')
    firstNumValue=None
    lastNumIndex=-2
    lastNumValue=None
    for wordNumber in wordNumbers.keys():
        firstPos = line.find(wordNumber)
        if firstPos!=-1 and firstPos < firstNumIndex:
            firstNumIndex = firstPos
            firstNumValue = wordNumbers[wordNumber]
        lastPos = line.rfind(wordNumber)
        if lastPos!=-1 and lastPos > lastNumIndex:
            lastNumIndex = lastPos
            lastNumValue = wordNumbers[wordNumber]
    return int("{}{}".format(firstNumValue, lastNumValue))

with open("1real.txt") as inputFile:
# with open("2.txt") as inputFile:
    for line in inputFile:
        if not line:
            continue
        lineNum = processLine(line)
        sum += lineNum
        print("got {} from {}, now {}".format(lineNum, line.rstrip(), sum))
print("All done, sum={}".format(sum))
