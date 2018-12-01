import numpy as np

def basis_prod(basis1, basis2):
    """
    INPUT
    basis1: list of strings corresponding to an n qubit computational basis
    basis2: same as basis1

    OUTPUT
    List containing the n*m computational basis
    """
    l = len(basis1)*len(basis2)
    out = [None for i in range(l)]
    i = 0
    for v1 in basis1:
        for v2 in basis2:
            out[i] = v1 + v2
            i = i + 1
    return out


def narray(l):
    """
    INPUT:
    l: integer length of returned list
    OUTPUT:
    numpy of length l containing only nan
    """
    nans = np.empty(l)
    nans.fill(np.nan)
    return nans