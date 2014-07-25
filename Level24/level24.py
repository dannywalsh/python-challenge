from PIL import Image
from itertools import *
from pprint import pprint

def debug(name,value):
    for n,v in zip(name,value):
        print"%s : %r" % (n,v,)

def getIm():
    return Image.open('resources/maze.png')

def getStartPo(im = getIm()):
    return [dict(nextPo = (im.size[0]-2, 0), currentPo=(0, 0))]

def hasHitWall(position):
    return getIm().getpixel(position) == getWallP() 

def isOutOfBounds(position, lower = (0,0), higher = getIm().size):
    for i in range(0,2):
        if position[i] < lower[i] or position[i] >= higher[i]:
            return True
    return False
 
def validate(nextPo, currentPo , im = getIm()):
    if nextPo == currentPo or isOutOfBounds(nextPo) or hasHitWall(nextPo):
        return False 
    return True

def getWallP(im = getIm()):
    return im.getpixel((im.size[0]-1, 0))

def addT(a,b):
    return tuple(map(sum,zip(a,b)))

def getMoves(po, moves = [(-1,0),(0,1),(1,0),(0,-1)]):
    return [addT(po,m) for m in moves]
    
def getValidMoves(pos, cond = validate, Fn = getMoves):
    if len(pos) == 0:
        return []
    return [getNextPo(pos['nextPo'],v) for v in Fn(pos['nextPo']) if cond(v,pos['currentPo'])]

def getRedValue(current, im = getIm()):
    return im.getpixel(current)[0]

def getNextPo(current, item):
    return dict(nextPo = item, currentPo = current)

def transit(position, getNextValue, breakCond):
    yield position
    
    for x in transit(getNextValue(position[0]), getNextValue, breakCond): 
        yield x

        if breakCond(x):
            break

def getNextNode(po):
    for i in transit(po, getValidMoves, lambda x : True if len(x) != 1 else False):
        if len(i) > 1:
            return i
    return []

def checkList(aList):
    if len(aList[-1]) == 0:
        del aList[-1]
        print "Deadend : %r"%(aList[-1][0])
        del aList[-1][0]
        return checkList(aList)
    return aList

def main():
    aList = [getStartPo()]
    for i in islice(count(),10050):
        aList.append(getNextNode([aList[-1][0]])) 
        aList = checkList(aList)
        if aList[-1][0]['currentPo'] == (1,639):
            print"END"
            break

    with open('resources/save.txt','w') as f:
        for item in aList:
            f.write("%s\n"%item[0])

if __name__ == "__main__" : main()
