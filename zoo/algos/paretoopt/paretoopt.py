# the python version is 2.7
import numpy as np
from random import randint
from math import ceil
from math import exp
from copy import deepcopy


class ParetoOpt:
    def __init__(self):
        pass

    # every bit will be flipped with probability 1/n
    def mutation(self, s ,n):
        s_temp=deepcopy(s)
        for i in range(1,n+1):
            # the probability is 1/n
            if randint(1,n)==i:
                s_temp[0,i-1]=(s[0,i-1]+1)%2
        return s_temp

    # This function is to find the index of s where element is 1
    def position(self,s):
        n=np.shape(s)[1]
        result=[]
        for i in range(0,n):
            if s[0,i]==1:
                result.append(i)
        return result   
            
    def opt(self, X, y, k):
        C = X.T * X
        b = X.T * y
        # row and column number of the matrix
        [m,n] = np.shape(X)
        # initiate the population
        population = np.mat(np.zeros([1,n], 'int8'))
        fitness = np.mat(np.zeros([1, 2]))
        fitness[0,0] = float('inf')
        popSize = 1
        # the current iterate count
        t = 0
        T = long(ceil(n * k * k * 2 * exp(1)))
        while t < T:
            # choose a individual from population randomly
            s = population[randint(1, popSize)-1, :]
            # every bit will be flipped with probability 1/n
            offSpring = self.mutation(s, n)
            offSpringFit = np.mat(np.zeros([1,2]))
            offSpringFit[0, 1] = offSpring[0, :].sum()
            if offSpringFit[0, 1] == 0.0 or offSpringFit[0, 1] >= 2.0 * k:
                offSpringFit[0, 0] = float("inf")
            else:
                pos = self.position(offSpring)
                alpha = (C[pos, :])[:, pos].I*b[pos, :]
                err = y - X[:, pos]*alpha
                offSpringFit[0, 0] = err.T * err/m
            # now we need to update the population
            hasBetter = False
            for i in range(0, popSize):
                if (fitness[i, 0] < offSpringFit[0, 0] and fitness[i, 1] <= offSpringFit[0, 1]) or \
                        (fitness[i, 0] <= offSpringFit[0, 0] and fitness[i,1]<offSpringFit[0,1]):
                    hasBetter = True
                    break
            # there is no better individual than offSpring
            if hasBetter == False:
                Q = []
                for j in range(0,popSize):
                    if offSpringFit[0, 0] <= fitness[j, 0] and offSpringFit[0, 1] <= fitness[j, 1]:
                        continue
                    else:
                        Q.append(j)
                Q.sort()
                # update fitness
                fitness=np.vstack((offSpringFit, fitness[Q, :]))
                # update population
                population=np.vstack((offSpring,population[Q,:]))
            t += 1
            popSize = np.shape(fitness)[0]
        resultIndex = -1
        maxSize=-1 
        for p in range(0, popSize):
            if fitness[p, 1] <= k and fitness[p, 1] > maxSize:
                maxSize = fitness[p, 1]
                resultIndex = p
        return population[resultIndex, :]

'''
if __name__=="__main__":
    print "start"
    orginX=NormlizeDate("../housing.txt")
    n=np.shape(orginX)[1]
    X=orginX[:,0:n-1]
    y=orginX[:,n-1]
    paretoopt=ParetoOpt()
    selectIndex=paretoopt.opt(X, y, 8)
    print selectIndex
    print "end"
'''
