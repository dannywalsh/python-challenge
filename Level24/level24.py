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

def transit_decorator(Fn):
    def transit(position):
        yield position
    
        for x in transit(Fn(position[0])): 
            yield x

            if len(x) != 1:
                break
    return transit

@transit_decorator
def getNextValidPo(pos, cond = validate, Fn = getMoves):
    if len(pos) == 0:
        return []
    return [getNextPo(pos['nextPo'],v) for v in Fn(pos['nextPo']) if cond(v,pos['currentPo'])]

def getRedValue(current, im = getIm()):
    return im.getpixel(current)[0]

def getNextPo(current, item):
    return dict(nextPo = item, currentPo = current)

def getNextNode(po):
    for i in getNextValidPo(po):
        if len(i) > 1:
            return i
    return []

def walkPath(aList):
    for node in aList:
        for i in getNextValidPo([node[0]]):
            if len(i) == 1:
                yield getRedValue(i[0]['currentPo'])
            else:
                break

def checkList(aList):
    if len(aList[-1]) == 0:
        del aList[-1]
        #print "Deadend : %r"%(aList[-1][0])
        del aList[-1][0]
        return checkList(aList)
    return aList

def getNodeList(aList = [getStartPo()]):
    while aList[-1][0]['currentPo'] != (1,639) or len(aList) != 0:
        aList.append(getNextNode([aList[-1][0]])) 
        aList = checkList(aList)
        print"len aList in getNodelist %r"%(len(aList),)
    return aList

def getOtherPathsGen(aList):
    for item in aList:
        if len(item) > 1:
            yield item[1:]

def main():

    aList = getNodeList()
    with open('resources/save.txt','w') as f:
        for item in aList:
            f.write("%s\n"%item)
    print"len aList : %r"%(aList,)
    for c, node in zip(count(),aList):
        if len(node) > 1:
            newList = aList[:c]
            newList.append(node[1:])
            newList.append(getNodeList(newList))
            print"len newList : %r c : %d"%(len(newList,c))


    #print"len first path %r"%(len(aList),)
    #for item in getOtherPathsGen(aList):
    #    getNodeList(item[0]


    #aList = [getStartPo()]
    #for i in islice(count(),10):
    #    aList.append(getNextNode([aList[-1][0]])) 
    #    aList = checkList(aList)
    #    if aList[-1][0]['currentPo'] == (1,639):
    #        print"END"
    #        break

    #for c, red in zip(count(),walkPath(aList)):,
    #    if c % 2 == 0:
            

    #with open('resources/save.txt','w') as f:
    #    for item in aList:
    #        f.write("%s"%item[0])
    

if __name__ == "__main__" : main()
