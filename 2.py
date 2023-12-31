gameLimit = {
    "red": 12,
    "green": 13,
    "blue": 14
}

def isPullPossible(pullText):
    remainingInPull = dict(gameLimit)
    for grab in pullText.split(", "):
        (grabNumber, grabColor) = grab.split(" ")
        num = remainingInPull[grabColor]
        num -= int(grabNumber)
        if num < 0:
            return False
        remainingInPull[grabColor]=num
    return True

def isGamePossible(gameText):
    for pull in gameText.split("; "):
        if not isPullPossible(pull):
            return False
    return True

def getLineSum(line):
    (gameLabel, gameText) = line.split(": ")
    if(isGamePossible(gameText)):
        return int(gameLabel.split(" ")[1])
    else:
        return 0
    
def getSum(text):
    sum=0
    for line in text:
        sum += getLineSum(line.rstrip())
    return sum

if __name__=="__main__":
    with open("2real.txt") as inputFile:
    # with open("2.txt") as inputFile:
        sum = getSum(inputFile)
        print("sum={}".format(sum))


