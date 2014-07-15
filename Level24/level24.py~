from PIL import Image
from itertools import *

def debug(name,value):
    for n,v in zip(name,value):
        print"%s : %r" % (n,v,)

def getIm():
    return Image.open('resources/maze.png')

def getStartPo(im = getIm()):
    return dict(nextPo = [(im.size[0]-2, 0)], currentPo=(0,0))

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
    #print "a : %r b : %r" % (a,b,)
    return tuple(map(sum,zip(a,b)))

def getMoves(po, moves = ((-1,0),(0,1),(1,0),(0,-1))):
    return ( addT(po, move) for move in moves)
    
def getValidMoves(pos, cond = validate, Fn = getMoves):
    return getNextPo(pos['nextPo'][0] ,[valid for valid in Fn(pos['nextPo'][0]) if cond(valid,pos['currentPo'])])

def getNextPo(current, item):
    return dict(nextPo = item, currentPo = current)

def transit(position, getNextValue, breakCond):
    yield position

    for x in transit(getNextValue(position), getNextValue, breakCond):
        yield x
        if breakCond(x):
            break

def getNodes(start):
    for trans in transit(start, getValidMoves, lambda x: False ):
        if len(trans['nextPo']) > 1:
            yield trans    
            for po in trans['nextPo']:
                getNodes(po)    
   
def main():
    #for i in islice(transit(getStartPo(), getValidMoves, lambda x: True if len(x['nextPo']) != 1 else False), 50):
    #    print(i)
    for i in islice(getNodes(getStartPo()),50):
        print(i)


if __name__ == "__main__" : main()
