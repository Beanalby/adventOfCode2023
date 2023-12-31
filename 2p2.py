import pprint

def addPullToBag(bag, pull):
    for cubes in pull.split(", "):
        (cubesNumber, cubesColor) = cubes.split(" ")
        cubesNumber = int(cubesNumber)
        if cubesColor in bag:
            if cubesNumber > bag[cubesColor]:
                bag[cubesColor] = cubesNumber
        else:
            bag[cubesColor] = cubesNumber

def getGamePower(gameText):
    bag = {}
    for pull in gameText.split("; "):
        addPullToBag(bag, pull)
    # pprint.pprint(bag)
    power=1
    for count in bag.values():
        power *= count
    print("power={} for {}".format(power, gameText))
    return power

def getSum(filename):
    sum = 0
    with open(filename) as inputFile:
        for line in inputFile:
            gameText = line.split(": ")[1].rstrip()
            sum += getGamePower(gameText)
    return sum
if __name__=="__main__":
    print("sum={}".format(getSum("2p2.txt")))
    print("sum={}".format(getSum("2real.txt")))
    # gameText = "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
    # gameText = "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    # print("Power={} for {}".format(getGamePower(gameText), gameText))
    # 1 red, 4 blue, 3 green
    #     sum = getSum(inputFile)
    #     print("sum={}".format(sum))


