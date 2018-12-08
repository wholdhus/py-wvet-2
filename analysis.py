import pandas as pd
import numpy as np
from classical_analysis import detect_entanglement
from quantum_analysis import pure_analysis
simulate = True

epsilon = float(input('Epsilon: '))
state = input('State (bell, plusplus, zerozero): ')
sim = input('If you want to run for real, type rfr: ')
if sim == 'rfr':
    simulate = False
counts = pure_analysis(state, epsilon, simulate=True)

# print('Here are the counts!')
# print(counts)

data = pd.DataFrame({'c[5]': [s for s in counts], 'n': [counts[s] for s in counts]})

N = np.sum(data['n'])
print('Total counts: {}'.format(N))

tol = np.sqrt(2.0/N)/epsilon
print('Statistical error is about {}'.format(tol))

isEntangled = detect_entanglement(data, epsilon, pure=True, tolerance=tol)

print("Entangled? {}".format(isEntangled))
