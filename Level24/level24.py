from PIL import Image
from itertools import *

def debug(name,value):
    for n,v in zip(name,value):
        print"%s : %r" % (n,v,)

def getIm():
    return Image.open('resources/maze.png')

def getStartPo(im = getIm()):
    return [dict(nextPo = (im.size[0]-2, 0), currentPo=(0, 0), redValue=(0))]

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
    return [getNextPo(pos['nextPo'],v) for v in Fn(pos['nextPo']) if cond(v,pos['currentPo'])]

def getRedValue(current, im = getIm()):
    return im.getpixel(current)[0]

def getNextPo(current, item):
    return dict(nextPo = item, currentPo = current, redValue = getRedValue(current))

def transit(position, getNextValue, breakCond):
    yield position
    
    for x in transit(getNextValue(position[0]), getNextValue, breakCond): 
        yield x

        if breakCond(x):
            print "\n BREAK CONDITION"
            break

def getNextNode(po):
    for i in transit(po, getValidMoves, lambda x : True if len(x) > 1 else False):
        if len(i) > 1:
            #print "what is i %r"%(i,)
            return i
        elif len(i) == 0:
            "Deadend : %r"%(po,)
            return []

def process(start):
    yield start
    #print "start : %r"%(start,)
    #print "getstartnode %r"%(getNextNode(start),)
    for nodelist in getNextNode(start):
        #print "node : %r"%(nodelist,)
        for n in process([nodelist]):
            #print "n : %r"%(n,)
            yield n

def main():
    for c, i in islice(izip(count(1),process(getStartPo())),1000):
        print "count %d :  %r " % (c,i,)

if __name__ == "__main__" : main()
