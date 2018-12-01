"""
Data analysis to conduct state tomography from
quantum data csv files

TODO: make this get the data directly from runs,
bypassing the csv stuff
"""
import pandas as pd
import numpy as np

# Constructing basis state labels
qb1 = ['0', '1']

def basis_prod(basis1, basis2):
    """
    Takes two lists of strings (i.e. computational
    bases), computes their tensor product with
    operation concatenation.

    Given an n qubit basis and an m qubit basis,
    returns the n+m qubit basis.
    """
    l = len(basis1)*len(basis2)
    out = [None for i in range(l)]
    i = 0
    for v1 in basis1:
        for v2 in basis2:
            out[i] = v1 + v2
            i = i + 1
    return out

qb2 = basis_prod(qb1, qb1)
qb4 = basis_prod(qb2, qb2)
qb5 = basis_prod(qb4, qb1)

def find_weak_values(states, counts, epsilon):
    nan16 = np.empty(16)
    nan16.fill(np.nan)

    imwvs = dict(zip(qb4, nan16))
    rewvs = dict(zip(qb4, nan16))

    n = np.sum(counts)
    
    counts2 = dict(zip(qb2, np.zeros(4)))
    for q in qb2:
        for i in range(len(counts)):
            if states[i][:-2] == q: # only looking at last 2 qb
                counts2[q] = counts2[q] + 1

    counts4 = dict(zip(qb4, np.zeros(16)))
    counts40 = dict(zip(qb4, np.zeros(16)))
    counts41 = dict(zip(qb4, np.zeros(16)))

    for q in qb4:
        for i in range(len(counts)):
            if states[i][:-4] == q: # only looking at first 2 qb
                counts4[q] = counts4[q] + 1
                if states[i][0] == '0':
                    counts40[q] = counts40[q] + 1
                elif states[i][0] == '1':
                    counts41[q] = counts41[q] + 1
                else:
                    # ERror
                    print('woah that was unexpected!')

    prob4 = dict(zip(qb4, np.zeros(16)))
    for q1 in qb2:
        for q2 in qb2:
            state = qb1 + qb2
            prob4[state] = np.float(counts[qb1]*counts[qb2])/(n**2)

    for q in qb4:
        prob4eps = np.float(counts4[q])/n
        imagWvs[q] = (1 - 2 * prob4eps / prob4[q]) / (2 * epsilon)
        
        re0 = (2 * counts40[q] - 1) / (2 * epsilon)
        re1 = (1 - 2 * counts41[q]) / (2 * epsilon)
        print('Difference in real values from 0
        and real values from 1 for state {} is
        {}'.format(q, re0-re1))
        reWvs[qb4] = (re0+re1)/2

    return reWvs + 1j*imagWvs

if __name__ == '__main__':

    yn = input('Treat as pure state? Y/N: ')
    treat_pure = False
    if yn.capitalize()[0] == 'Y':
        treat_pure = True

    datafile = input('Filename: ')
    epsilon = input('Epsilon for this data: ')

    # reading the first column as a string to keep leading zeros
    data = pd.read_csv(datafile, dtype = {'c[5]':str, 'n':int})

    states = data['c[5]']
    counts = data['n']

    wvs = get_weak_values(states, counts, epsilon)
    
    # now to reconstruct wooooo
