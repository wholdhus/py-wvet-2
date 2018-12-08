"""
Data analysis to conduct state tomography from
quantum data csv files
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
        else:
            counts1 = counts1 + data['n'][i]

    for q in QB4:
        for i, s in enumerate(data['c[5]']):
            if s[-4:] == q: # only looking at first 4 QB
                counts4[q] = counts4[q] + data['n'][i]
                if s[0] == '0':
                    # could also use q for this TODO: sanity check
                    counts40[q] = counts40[q] + data['n'][i]
                else:
                    counts41[q] = counts41[q] + data['n'][i]

    counts4pre = dict(zip(QB4, np.zeros(16)))
    precounts = 0
    for q1 in QB2:
        for q2 in QB2:
            state = q1 + q2
            prob = (counts2[q1] / n)*(counts2[q2] / n)
            counts4pre[state] = n * prob
            precounts = precounts + n * prob

    print('Total of precounts is {}'.format(precounts))

    for q in QB4:
        if counts4pre[q] != 0:
            imwvs[q] = (counts4[q] / counts4pre[q] - 1) / (2 * epsilon)

            re0 = (counts40[q]/counts4pre[q] - 0.5)/(counts0 - 0.5)
            re1 = (counts41[q]/counts4pre[q] - 0.5)/(counts1 - 0.5)
            rewvs[q] = (re0 + re1) / 2
        else: # handling singular cases
            print('No predicted counts for {}'.format(q))
            if counts4[q] == 0:
                print('Also no real counts, so guessing 0/0 = 1')
                imwvs[q] = -1/(2*epsilon)

                re0 = (1 - 0.5)/(counts0 - 0.5)
                re1 = (1 - 0.5)/(counts1 - 0.5)
                rewvs[q] = (re0 + re1) / 2
    wvs = pd.DataFrame({'state': [s for s in rewvs],
        'rewv': [rewvs[s] for s in rewvs],
        'imwv': [imwvs[s] for s in imwvs]})
    return rewvs, imwvs, wvs


def detect_entanglement(data, epsilon, pure, tolerance):
    isEntangled = True
    if pure:
        diags = {'0000': 0, '0101': 0, '1010': 0,
                '1111': 0}
        for i, s in enumerate(data['c[5]']):
            for d in diags:
                if s[-4:] == d:
                    diags[d] = diags[d] + data['n'][i]
        if diags['0000']*diags['1111'] == 0 and diags['1010']*diags['0101'] == 0:
            print('Product state! ad-bc = 0')
            isEntangled = False
        else: # Now need to use weak values
            rewvs, imwvs, wvs = find_weak_values(data, epsilon)
            b2 = '0001' # unit vector '2' in paper
            b4 = '0011' # unit vector '4' in paper
            print('Weak values for k=2:')
            print('{} + i {}'.format(rewvs[b2], imwvs[b2]))
            print('Weak values for k=4:')
            print('{} + i {}'.format(rewvs[b4], imwvs[b4]))
            diff = rewvs[b4] + 1j * imwvs[b4] - rewvs[b2] - 1j * imwvs[b2];
            print('Difference in weak values: {}'.format(diff))
            if np.abs(diff) < tolerance:
                print('Product state! a/b = c/d')
                isEntangled = False
    else: # TODO: implement this part
        print('Woops! I have trouble with mixed states right now!')
        pass
    return isEntangled


if __name__ == '__main__':
    # Test of code. Runs on locally stored csv files

    datafile = 'data/plus_0.01_pure.csv'
    eps = 0.01

    # reading the first column as a string to keep leading zeros
    plusData = pd.read_csv(datafile, dtype = {'c[5]':str, 'n':int})

    isEntangled = detect_entanglement(plusData, eps, True, eps)
    if isEntangled:
        print('ENTANGLED')
    else:
        print('UNENTANGLED')



    datafile2 = 'data/bell_0.01_pure.csv'
    epsilon = 0.01
    # print(pd.read_csv(datafile2, dtype = {'c[5]':str, 'n':int}))
