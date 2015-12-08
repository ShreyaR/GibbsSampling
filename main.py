__author__ = 'shreyarajpal'

import sys
from GibbsSampling import GibbsSampler
from math import log
from convergence import GibbsSamplerConvergence, GibbsSamplerRandomisedConvergence
import matplotlib.pyplot as plt

loopWords = 'data/data-loops.dat'
loopWordsWS = 'data/data-loopsWS.dat'
treeWords = 'data/data-tree.dat'
treeWordsWS = 'data/data-treeWS.dat'

trueLoopWords = 'data/truth-loops.dat'
trueLoopWordsWS = 'data/truth-loopsWS.dat'
trueTreeWords = 'data/truth-tree.dat'
trueTreeWordsWS = 'data/truth-treeWS.dat'


def infer(data):
    if data==1:
        dataFile = open(loopWords)
        trueFile = open(trueLoopWords)
    elif data==2:
        dataFile = open(loopWordsWS)
        trueFile = open(trueLoopWordsWS)
    elif data==3:
        dataFile = open(treeWords)
        trueFile = open(trueTreeWords)
    else:
        dataFile = open(treeWordsWS)
        trueFile = open(trueTreeWordsWS)

    words = []
    assignments = []
    while(True):
        chunk = dataFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            w1 = [int(i) for i in w1.rstrip().split('\t')]
            w2 = [int(i) for i in w2.rstrip().split('\t')]
            words.append((w1,w2))
        dataFile.close()
        break

    while(True):
        chunk = trueFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            assignments.append((w1,w2))
        trueFile.close()
        break

    inference = []

    LogLikelihood = []

    timeForDataset = 0
    for i in xrange(len(words)):
        w1,w2 = words[i]
        trueWord1, trueWord2 = assignments[i]
        ass, samples, totalTime = GibbsSampler(w1, w2)
        timeForDataset += totalTime

        logLikelihoodWord1 = 0
        logLikelihoodWord2 = 0

        numOfSamples = sum(samples[0].values())

        #Calculate Log-Prob of True Words
        for x in xrange(len(trueWord1)):
            relevantFrequencies = samples[x]
            letterFrequency = relevantFrequencies[trueWord1[x]]
            if letterFrequency==0:
                letterFrequency = 0.01
            logLikelihoodWord1 += log(float(letterFrequency)/numOfSamples)
        for x in xrange(len(trueWord2)):
            relevantFrequencies = samples[x + len(trueWord1)]
            letterFrequency = relevantFrequencies[trueWord2[x]]
            if letterFrequency==0:
                letterFrequency = 0.01
            logLikelihoodWord2 += log(float(letterFrequency)/numOfSamples)

        LogLikelihood.append(logLikelihoodWord2)
        LogLikelihood.append(logLikelihoodWord1)

        inference1 = ass[:len(w1)]
        inference2 = ass[len(w1):]
        inference.append((inference1,inference2))

    totalWords = 2*len(assignments)
    totalCharacters = 0

    correctWords = 0
    correctCharacters = 0

    for i in xrange(len(assignments)):

        predictedWord1, predictedWord2 = inference[i]
        actualWord1, actualWord2 = assignments[i]
        image1, image2 = words[i]

        if predictedWord1==actualWord1:
            correctWords += 1

        if predictedWord2==actualWord2:
            correctWords += 1

        totalCharacters += len(actualWord1) + len(actualWord2)

        for x in xrange(len(predictedWord1)):
            if predictedWord1[x]==actualWord1[x]:
                correctCharacters += 1

        for x in xrange(len(predictedWord2)):
            if predictedWord2[x]==actualWord2[x]:
                correctCharacters += 1

    print 'charAccuracy = ',float(correctCharacters)/totalCharacters
    print 'wordAccuracy = ', float(correctWords)/totalWords
    print 'logLikelihood = ', sum(LogLikelihood)/len(LogLikelihood)
    print 'totalTime = ', timeForDataset
    return


def convergenceAnalysis(data):
    if data==1:
        dataFile = open(loopWords)
        trueFile = open(trueLoopWords)
    elif data==2:
        dataFile = open(loopWordsWS)
        trueFile = open(trueLoopWordsWS)
    elif data==3:
        dataFile = open(treeWords)
        trueFile = open(trueTreeWords)
    else:
        dataFile = open(treeWordsWS)
        trueFile = open(trueTreeWordsWS)

    words = []
    assignments = []
    while(True):
        chunk = dataFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            w1 = [int(i) for i in w1.rstrip().split('\t')]
            w2 = [int(i) for i in w2.rstrip().split('\t')]
            words.append((w1,w2))
        dataFile.close()
        break

    while(True):
        chunk = trueFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            assignments.append((w1,w2))
        trueFile.close()
        break

    aggregator = []

    for i in xrange(len(words)):
        w1,w2 = words[i]
        trueWord1, trueWord2 = assignments[i]
        aggregator.append(GibbsSamplerConvergence(w1, w2, trueWord1, trueWord2))

    combinedWdAcc = []
    numOfWords = 2*len(aggregator)

    smallestNumOfSamples = min([len(i) for i in aggregator])

    for i in xrange(smallestNumOfSamples):
        totalCorrectWords = 0
        for accLists in aggregator:
            acc1, acc2 = accLists[i]
            totalCorrectWords += acc1 + acc2
        combinedWdAcc.append(float(totalCorrectWords)/numOfWords)

    plt.plot(xrange(0,len(combinedWdAcc)*10,50),[combinedWdAcc[x] for x in xrange(0,len(combinedWdAcc),5)])
    plt.ylabel('Word Accuracy')
    plt.xlabel('Number of Iterations')
    plt.savefig(str(data) + '.eps')
    plt.close()
    return


def extraCredit(data):
    if data==1:
        dataFile = open(loopWords)
        trueFile = open(trueLoopWords)
    elif data==2:
        dataFile = open(loopWordsWS)
        trueFile = open(trueLoopWordsWS)
    elif data==3:
        dataFile = open(treeWords)
        trueFile = open(trueTreeWords)
    else:
        dataFile = open(treeWordsWS)
        trueFile = open(trueTreeWordsWS)

    words = []
    assignments = []
    while(True):
        chunk = dataFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            w1 = [int(i) for i in w1.rstrip().split('\t')]
            w2 = [int(i) for i in w2.rstrip().split('\t')]
            words.append((w1,w2))
        dataFile.close()
        break

    while(True):
        chunk = trueFile.read().split('\n')
        for i in xrange(len(chunk)/3):
            w1,w2 = chunk[i*3],chunk[i*3 + 1]
            assignments.append((w1,w2))
        trueFile.close()
        break

    aggregator = []
    aggregatorRandom = []

    for i in xrange(len(words)):
        w1,w2 = words[i]
        trueWord1, trueWord2 = assignments[i]
        aggregator.append(GibbsSamplerConvergence(w1, w2, trueWord1, trueWord2))

    for i in xrange(len(words)):
        w1,w2 = words[i]
        trueWord1, trueWord2 = assignments[i]
        aggregatorRandom.append(GibbsSamplerRandomisedConvergence(w1, w2, trueWord1, trueWord2))

    combinedWdAcc = []
    combinedWdAccRandom = []
    numOfWords = 2*len(aggregator)

    smallestNumOfSamples = min([len(i) for i in aggregator])
    numOfSamplesRandom = min([len(i) for i in aggregatorRandom])

    for i in xrange(smallestNumOfSamples):
        totalCorrectWords = 0
        for accLists in aggregator:
            acc1, acc2 = accLists[i]
            totalCorrectWords += acc1 + acc2
        combinedWdAcc.append(float(totalCorrectWords)/numOfWords)

    for i in xrange(numOfSamplesRandom):
        totalCorrectWords = 0
        for accLists in aggregatorRandom:
            acc1, acc2 = accLists[i]
            totalCorrectWords += acc1 + acc2
        combinedWdAccRandom.append(float(totalCorrectWords)/numOfWords)


    plt.plot(xrange(0,len(combinedWdAcc)*10,50),[combinedWdAcc[x] for x in xrange(0,len(combinedWdAcc),5)], label='Sequential Gibbs Sampling')
    plt.plot(xrange(0,len(combinedWdAccRandom)*10,50),[combinedWdAccRandom[x] for x in xrange(0,len(combinedWdAccRandom),5)], color='r', label = 'Randomised Gibbs Sampling')
    plt.legend(loc = 2)
    plt.ylabel('Word Accuracy')
    plt.xlabel('Number of Iterations')
    plt.savefig('Randomised' + str(data) + '.eps')
    plt.close()
    return

infer(2)
#convergenceAnalysis(2)
#extraCredit(2)
