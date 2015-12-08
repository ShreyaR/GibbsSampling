__author__ = 'shreyarajpal'

import basics
from random import choice, random, seed
from time import time, clock
from math import exp, log

import matplotlib.pyplot as plt

factorLookUp = {}

#Returns the combined factor for
def getCombinedFactor(index, assignment, w1, w2):
    global factorLookUp

    sk1, sk2, ps = basics.findingSkips(w1, w2)
    factorLookUp = basics.getFactor(len(w1), len(w2), sk1, sk2, ps)

    relevantFactors = factorLookUp[index]

    if index<len(w1):
        combinedFactor = basics.ocrDat[w1[index]].copy()
    else:
        combinedFactor = basics.ocrDat[w2[index - len(w1)]].copy()

    for factor in relevantFactors:
        typeOfFactor, vars = factor
        if typeOfFactor=='t':
            for i in basics.characterArray:
                if index==vars[0]:
                    fromVar = i
                    toVar = assignment[index + 1]
                else:
                    fromVar = assignment[index - 1]
                    toVar = i

                combinedFactor[i] += basics.transDat[fromVar][toVar]
        elif typeOfFactor=='s' or typeOfFactor=='p':
            for i in basics.characterArray:
                if index==vars[0]:
                    otherVar = assignment[vars[1]]
                else:
                    otherVar = assignment[vars[0]]

                combinedFactor[i] += basics.getPairSkipFactor(i, otherVar)
    return combinedFactor

#Samples probability assignment
def getRandomSample(i, assignment, w1, w2):
    combinedFactors = getCombinedFactor(i, assignment, w1, w2)
    letters = []
    probs = []
    partFunc = sum([exp(x) for x in combinedFactors.values()])

    for i in combinedFactors.keys():
        letters.append(i)
        probs.append(exp(combinedFactors[i])/partFunc)

    cumulative = 0
    samplingProbs = []
    for i in xrange(10):
        samplingProbs.append(cumulative + probs[i])
        cumulative += probs[i]

    chance = random()
    prevProb = 0
    finalSample = -1

    for i in xrange(10):
        if chance>=prevProb and chance<samplingProbs[i]:
            finalSample = letters[i]
            break
        else:
            prevProb = samplingProbs[i]

    if finalSample==-1:
        finalSample = letters[9]

    return finalSample

#Generates Gibbs samples
def GibbsSampler(w1, w2):
    global factorLookUp

    n1 = len(w1)
    n2 = len(w2)

    #Create a factor look-up list
    sk1, sk2, ps = basics.findingSkips(w1, w2)
    factorLookUp = basics.getFactor(n1, n2, sk1, sk2, ps)

    #Generate initial assignment
    seed(time())
    assignment = [choice(basics.characterArray) for i in xrange(n1 + n2)]
    samples = [{t:0 for t in basics.characterArray} for i in xrange(n1 + n2)]

    burnInSamples = [{t:0 for t in basics.characterArray} for i in xrange(n1 + n2)]
    prevLogLikelihoodOfMLA = 500
    burninInfo = []
    count = 0

    for i in xrange(len(assignment)):
        burnInSamples[i][assignment[i]] += 1

    #If burn-in graph is to be generated, uncomment this
    '''
    holyStop = -1
    flag = True
    for i in xrange(300):
        for j in xrange(n1 + n2):
            count += 1
            sample = getRandomSample(j, assignment, w1, w2)
            assignment[j] = sample
            for x in xrange(len(assignment)):
                burnInSamples[x][assignment[x]] += 1
            #burnInSamples[j][sample] += 1
            logLikelihoodOfMLA = 0

            for k in xrange(n1 + n2):
                maxProbAssignment = float(max(burnInSamples[k].values()))/count
                if maxProbAssignment==0:
                    maxProbAssignment = 0.001
                #print maxProbAssignment
                logLikelihoodOfMLA += log(maxProbAssignment)
                #print logLikelihoodOfMLA


            if abs(prevLogLikelihoodOfMLA - logLikelihoodOfMLA) < 0.0002 and count>500 and flag:
                holyStop = count
                flag = False
                print holyStop

            prevLogLikelihoodOfMLA = logLikelihoodOfMLA

            burninInfo.append(logLikelihoodOfMLA)

    set1 = burninInfo[:holyStop]
    set2 = burninInfo[holyStop:]

    plt.plot(set1)
    plt.plot(range(holyStop, len(burninInfo)), set2, '--', color = 'r')
    plt.ylabel('Log-Likelihood of Most Likely Assignment')
    plt.xlabel('Number of Iterations')
    plt.axes([0, len(burninInfo), 0, max(burninInfo) + 2])
    plt.plot([holyStop], [burninInfo[holyStop]], 'r^')
    plt.savefig('burnin.eps')
    '''

    start = clock()
    while(True):
        flag = False
        for j in xrange(n1 + n2):
            sample = getRandomSample(j, assignment, w1, w2)
            assignment[j] = sample
            #burnInSamples[j][sample] += 1
            for x in xrange(len(assignment)):
                burnInSamples[x][assignment[x]] += 1
            count += 1
            if count>100:
                logLikelihoodOfMLA = 0
                for k in xrange(n1 + n2):
                    logLikelihoodOfMLA += float(max(burnInSamples[k].values()))/count
                if abs(logLikelihoodOfMLA - prevLogLikelihoodOfMLA)<0.0002:
                    flag = True
                    break
                else:
                    prevLogLikelihoodOfMLA = logLikelihoodOfMLA
                    burninInfo.append(logLikelihoodOfMLA)
        if flag:
            break
    #print len(burninInfo)


    count = 0
    for i in xrange(10000):
        for j in xrange(n1 + n2):
            count += 1
            sample = getRandomSample(j, assignment, w1, w2)
            assignment[j] = sample
            if count%10==0:
                for x in xrange(n1 + n2):
                    samples[x][assignment[x]] += 1

    MLA = ''
    for i in samples:
        maxMarginal = max(i.values())
        for j in i.keys():
            if i[j]==maxMarginal:
                MLA += j
                break
    end = clock()
    totalTime = end - start

    return MLA, samples,totalTime


def GibbsSamplerRandomized(w1, w2):
    global factorLookUp

    n1 = len(w1)
    n2 = len(w2)

    #Create a factor look-up list
    sk1, sk2, ps = basics.findingSkips(w1, w2)
    factorLookUp = basics.getFactor(n1, n2, sk1, sk2, ps)

    #Generate initial assignment
    seed(time())
    assignment = [choice(basics.characterArray) for i in xrange(n1 + n2)]
    samples = [{t:0 for t in basics.characterArray} for i in xrange(n1 + n2)]

    burnInSamples = [{t:0 for t in basics.characterArray} for i in xrange(n1 + n2)]
    prevLogLikelihoodOfMLA = 500
    burninInfo = []
    count = 0

    for i in xrange(len(assignment)):
        burnInSamples[i][assignment[i]] += 1

    start = clock()
    while(True):
        varSampled = choice(xrange(n1 + n2))
        sample = getRandomSample(varSampled, assignment, w1, w2)
        assignment[varSampled] = sample
        for x in xrange(len(assignment)):
            burnInSamples[x][assignment[x]] += 1
        count += 1
        if count>100:
            logLikelihoodOfMLA = 0
            for j in xrange(n1 + n2):
                logLikelihoodOfMLA += float(max(burnInSamples[j].values()))/count
            if abs(logLikelihoodOfMLA - prevLogLikelihoodOfMLA)<0.0002:
                break
            else:
                prevLogLikelihoodOfMLA = logLikelihoodOfMLA
                burninInfo.append(logLikelihoodOfMLA)


    count = 0
    for i in xrange(10000):
        varSampled = choice(xrange(n1 + n2))
        count += 1
        sample = getRandomSample(varSampled, assignment, w1, w2)
        assignment[varSampled] = sample
        if count%10==0:
            for x in xrange(n1 + n2):
                samples[x][assignment[x]] += 1

    MLA = ''
    for i in samples:
        maxMarginal = max(i.values())
        for j in i.keys():
            if i[j]==maxMarginal:
                MLA += j
                break
    end = clock()
    totalTime = end - start

    return MLA, samples,totalTime



#GibbsSampler([82,338,293,484,505,211], [776,477,10,82,338])
#GibbsSampler([542,949,830], [742,981,543,625,830,758])
#GibbsSamplerRandomized([542,949,830], [742,981,543,625,830,758])[0]