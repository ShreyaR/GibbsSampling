__author__ = 'shreyarajpal'

from time import time
import basics
from random import choice, seed
from GibbsSampling import getRandomSample

def GibbsSamplerConvergence(w1, w2, actualWord1, actualWord2):
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

    iterationInfo = []

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
                for k in samples:
                    maxMarginal = max(k.values())
                    for l in k.keys():
                        if k[l]==maxMarginal:
                            MLA += l
                            break

                word1 = MLA[:len(w1)]
                word2 = MLA[len(w1):]
                iterationInfo.append((word1==actualWord1, word2==actualWord2))

        if count >= 20000:
            break

    return iterationInfo


def GibbsSamplerRandomisedConvergence(w1, w2, actualWord1, actualWord2):
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

    while(True):
        varSampled = choice(xrange(n1 + n2))
        sample = getRandomSample(varSampled, assignment, w1, w2)
        assignment[varSampled] = sample
        #burnInSamples[varSampled][sample] += 1
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

    #print 'Burn-in ', len(burninInfo)

    iterationInfo = []

    count = 0
    for i in xrange(20000):
        varSampled = choice(xrange(n1 + n2))
        count += 1
        sample = getRandomSample(varSampled, assignment, w1, w2)
        assignment[varSampled] = sample
        if count%10==0:
            for x in xrange(n1 + n2):
                samples[x][assignment[x]] += 1
            MLA = ''
            for k in samples:
                maxMarginal = max(k.values())
                for j in k.keys():
                    if k[j]==maxMarginal:
                        MLA += j
                        break
            word1 = MLA[:len(w1)]
            word2 = MLA[len(w1):]
            iterationInfo.append((word1==actualWord1, word2==actualWord2))

    return iterationInfo


#print GibbsSamplerRandomisedConvergence([542,949,830], [742,981,543,625,830,758], 'ade', 'atoner')