sum=0
# with open("real.txt") as inputFile:
with open("1real.txt") as inputFile:
    for line in inputFile:
        if not line:
            continue
        firstNum=None
        lastNum=None
        for c in line:
            if c >= "0" and c <= "9":
                if not firstNum:
                    firstNum=c
                lastNum=c
                continue
        lineNum = int("{}{}".format(firstNum, lastNum))
        sum += lineNum
        print("Looking at first={} last={} makes {}, total={}".format(firstNum, lastNum, lineNum, sum))
print("All done, sum={}".format(sum))
