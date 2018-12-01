"""
Data analysis to conduct state tomography from
quantum data csv files

TODO: make this get the data directly from runs,
bypassing the csv stuff
"""
import pandas as pd
import numpy as np
from utils import *

# Constructing basis state labels
qb1 = ['0', '1']

# Creating 2, 4, and 5 qubit computational bases
qb2 = basis_prod(qb1, qb1)
qb4 = basis_prod(qb2, qb2)
qb5 = basis_prod(qb4, qb1)


def find_weak_values(states, counts, epsilon):
    """
    Determines weak values from quantum computation results.

    INPUT
    states: List of computational 5-qubit basis states i.e. '10101'
    counts: The number of results corresponding to each state
    epsilon: A small number controlling the interaction strength
    OUTPUT
    numpy array containing the complex weak values
    """

    imwvs = dict(zip(qb4, narray(16)))
    rewvs = dict(zip(qb4, narray(16)))

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
        if prov4[q] != 0:
            imagWvs[q] = (1 - 2 * prob4eps / prob4[q]) / (2 * epsilon)
        else: # Weak values are allowed to be singular
            pass # I already initialized them to nan
        re0 = (2 * counts40[q] - 1) / (2 * epsilon)
        re1 = (1 - 2 * counts41[q]) / (2 * epsilon)
        print('Difference in real values from 0
        and real values from 1 for state {} is
        {}'.format(q, re0-re1))
        reWvs[qb4] = (re0+re1)/2

    return reWvs + 1j*imagWvs

if __name__ == '__main__':
    """Test of code. Runs on locally stored csv files"""
    yn = input('Treat as pure state? Y/N: ')
    treat_pure = False
    if yn.capitalize()[0] == 'Y':
        treat_pure = True

    datafile = input('Filepath: ')
    epsilon = input('Epsilon for this data: ')

    # reading the first column as a string to keep leading zeros
    data = pd.read_csv(datafile, dtype = {'c[5]':str, 'n':int})

    states = data['c[5]']
    counts = data['n']

    wvs = get_weak_values(states, counts, epsilon)
    
    # now to reconstruct wooooo
