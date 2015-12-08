__author__ = 'shreyarajpal'

from math import log, exp
from collections import deque
import time
import networkx as nx

#global ocrDat, transDat
characterArray = ['e','t','a','o','i','n','s','h','r','d']
ocrDat = []
transDat = {}

def readOCRPotentials():
    global ocrDat
    ocrDat = [{} for _ in xrange(1000)]#*numOfImages
    ocrInfo = open('data/ocr.dat', 'r')
    for line in ocrInfo:
        info = line.rstrip().split('\t')
        ocrDat[int(info[0])][info[1]] = log(float(info[2]))
    ocrInfo.close()
    return

def readTransPotentials():
    global transDat
    transInfo = open('data/trans.dat', 'r')

    for item in characterArray:
        transDat[item] = {}
        for i in characterArray:
            transDat[item][i]=-1

    for line in transInfo:
        info = line.rstrip().split('\t')
        transDat[info[0]][info[1]] = log(float(info[2]))

    transInfo.close()
    return

def getSkipFactor(a1, a2):
    if (a1==a2):
        return log(5)
    else:
        return 0

def getPairSkipFactor(a1, a2):
    if a1==a2:
        return log(5)
    else:
        return 0

def assignmentToNumber(a):
    lenOfWord = len(a)
    index = 0
    for i in xrange(lenOfWord):
        multiplier = characterArray.index(a[i])
        index += multiplier * (pow(10, i))
    return index

def numberToAssignment(x, l):
    a = []
    i = 1
    for j in xrange(l):
        if x:
            a.append(x%10)
            x=x/10
        else:
            a.append(0)

    b = [characterArray[t] for t in a]
    return b

#Returns 3 lists -> skip edges in w1, skip edges in w2 and pair skip edges
def findingSkips(w1, w2):


    skipEdge1 = []
    skipEdge2 = []
    pairSkip = []

    n1 = len(w1)
    n2 = len(w2)

    #Finding Skip Edge in Word 1
    for i in xrange(n1):
        for j in range(i+1, n1):
            if w1[i]==w1[j]:
                skipEdge1.append((i,j))

    #Finding Skip Edge in Word 2
    for i in xrange(n2):
        for j in range(i+1, n2):
            if w2[i]==w2[j]:
                skipEdge2.append((i,j))

    #Finding Pair Skip Edges
    for i in xrange(n1):
        for j in xrange(n2):
            if w1[i]==w2[j]:
                pairSkip.append((i, j))

    return skipEdge1, skipEdge2, pairSkip

#Returns undirected graph as a networkX graph
def getFactor(n1, n2, sk1, sk2, ps):
    graph = nx.Graph()

    factorLookUp = {i:{('o', i)} for i in xrange(n1 + n2)}
    for i in xrange(n1 - 1):
        factorLookUp[i].add(('t', (i, i+1)))
        factorLookUp[i + 1].add(('t', (i, i+1)))
    for i in xrange(n2 - 1):
        factorLookUp[n1 + i].add(('t', (n1 + i, n1 + i+1)))
        factorLookUp[n1 + i + 1].add(('t', (n1 + i, n1 + i+1)))
    for skipFactor in sk1:
        a,b = skipFactor
        factorLookUp[a].add(('s', skipFactor))
        factorLookUp[b].add(('s', skipFactor))
    for skipFactor in sk2:
        a,b = skipFactor
        factorLookUp[n1 + a].add(('s', (n1 + a, n1 + b)))
        factorLookUp[n1 + b].add(('s', (n1 + a, n1 + b)))
    for pairSkip in ps:
        a,b = pairSkip
        factorLookUp[a].add(('p', (a, n1 + b)))
        factorLookUp[n1 + b].add(('p', (a, n1 + b)))


    #Graph created has nodes from 0 to (n1 + n2 - 1). First n1 nodes are nodes in w1, next n2 are nodes in w2.
    '''graph.add_nodes_from(xrange(n1 + n2))
    graph.add_edges_from([(i, i+1) for i in xrange(n1 - 1)])
    graph.add_edges_from([(n1 + i, n1 + i+1) for i in xrange(n2 - 1)])
    graph.add_edges_from(sk1)
    graph.add_edges_from([(n1 + i[0], n1 + i[1]) for i in sk2])
    graph.add_edges_from([(i[0], n1 + i[1]) for i in ps])'''
    return factorLookUp



readOCRPotentials()
readTransPotentials()