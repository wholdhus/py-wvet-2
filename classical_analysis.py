"""
Data analysis to conduct state tomography from
quantum data csv files

TODO: make this get the data directly from runs,
bypassing the csv stuff
"""
import pandas as pd
import numpy as np
from utils import basis_prod, narray

#pylint:disable=invalid-name

# Constructing basis state labels
QB1 = ['0', '1']

# Creating 2, 4, and 5 qubit computational bases
QB2 = basis_prod(QB1, QB1)
QB4 = basis_prod(QB2, QB2)
QB5 = basis_prod(QB4, QB1)


def find_weak_values(data, epsilon): #pylint:ignore=too-many-branches
    """
    Determines weak values from quantum computation results.

    INPUT
    epsilon: A small number controlling the interaction strength
    data: A DataFrame that comes from using pandas to read the csvs returned
    by the IBM quantum experience composer.
    OUTPUT
    numpy array containing the complex weak values
    """
    imwvs = dict(zip(QB4, narray(16)))
    rewvs = dict(zip(QB4, narray(16)))

    counts2 = dict(zip(QB2, np.zeros(4)))
    counts4 = dict(zip(QB4, np.zeros(16)))
    counts40 = dict(zip(QB4, np.zeros(16)))
    counts41 = dict(zip(QB4, np.zeros(16)))

    n = np.sum(data['n'])

    counts0 = 0.0 # states starting with 0
    counts1 = 0.0 # states starting with 1

    for q in QB2:
        for i, s in enumerate(data['c[5]']):
            if s[-2:] == q: # only looking at last 2 QB
                counts2[q] = counts2[q] + data['n'][i]
        if s[0] == '0':
            counts0 = counts0 + data['n'][i]
        elif s[0] == '1':
            counts1 = counts1 + data['n'][i]
        else:
            print('WARNING: {}th qubit is not a qubit!'.format(i))

    print('{} counts starting with 0'.format(counts1))
    print('{} counts starting with 1'.format(counts2))

    for q in QB4:
        for i, s in enumerate(data['c[5]']):
            if s[-4:] == q: # only looking at first 4 QB
                counts4[q] = counts4[q] + data['n'][i]
                if s[0] == '0':
                    # could also use q for this TODO: sanity check
                    counts40[q] = counts40[q] + data['n'][i]
                elif s[0] == '1':
                    counts41[q] = counts41[q] + data['n'][i]
                else:
                    print('WARNING: state must start with 0 or 1!')
    for q in QB4:
        if counts41[q] + counts40[q] != counts4[q]:
            print('Woah: different number of counts than the number of counts')
            print(counts41[q])
            print(counts42[q])
            print(counts4[q])

    counts4pre = dict(zip(QB4, np.zeros(16)))
    for q1 in QB2:
        for q2 in QB2:
            state = q1 + q2
            prob = (counts2[q1] / n)*(counts2[q2] / n)
            counts4pre[state] = n * prob

    for q in QB4:
        if counts4pre[q] != 0:
            imwvs[q] = (counts4[q] / counts4pre[q] - 1) / (2 * epsilon)
        else: # Weak values are allowed to be singular
            pass # I already initialized them to nan
        # re0 = (0.5 - counts40[q]/(counts4pre[q])) / epsilon
        # re1 = (counts41[q]/(counts4pre[q]) - 0.5) / epsilon
        re0 = (counts40[q]/counts4pre[q] - 0.5)/(counts0 - 0.5)
        re1 = (counts41[q]/counts4pre[q] - 0.5)/(counts1 - 0.5)
        print(
            'Difference in real values for state {} is {}'.format(
                q, re0-re1))
        print('Difference in counts is {}'.format(
            counts41[q] - counts40[q]))
        rewvs[q] = (re0+re1)/2
    return imwvs, rewvs


def detect_entanglement(data, epsilon, pure, tolerance):
    isProduct = False
    if pure:
        diags = {'0000': 0, '0101': 0, '1010': 0,
                '1111': 0}
        for i, s in enumerate(data['c[5]']):
            for d in diags:
                if s[-4:] == d:
                    diags[d] = diags[d] + data['n'][i]
        print(diags)
        if diags['0000']*diags['1111'] == 0 and diags['1010']*diags['0101'] == 0:
            print('Product state! ad-bc = 0')
            isProduct = True
        else: # Now need to use weak values
            imwvs, rewvs = find_weak_values(data, epsilon)
            b2 = '0001'
            b4 = '0010'
            reDiff = np.abs(rewvs[b2] - rewvs[b4])
            imDiff = np.abs(imwvs[b2] - imwvs[b4])
            print('Difference in weak values: {}, {}'.format(reDiff, imDiff))
            if reDiff < tolerance and imDiff < tolerance:
                print('Product state! a/b = c/d')
                isProduct = True
    else: # TODO: implement this part
        pass
    return isProduct


if __name__ == '__main__':
    # Test of code. Runs on locally stored csv files

    datafile = 'data/plus_0.01_pure.csv'
    eps = 0.01

    # reading the first column as a string to keep leading zeros
    plusData = pd.read_csv(datafile, dtype = {'c[5]':str, 'n':int})

    isProduct = detect_entanglement(plusData, eps, True, eps)
    if isProduct:
        print('PRODUCT')
    else:
        print('ENTANGLED')



    datafile2 = 'data/bell_0.01_pure.csv'
    epsilon = 0.01
    # print(pd.read_csv(datafile2, dtype = {'c[5]':str, 'n':int}))
