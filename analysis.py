import pandas as pd
from classical_analysis import detect_entanglement
from quantum_analysis import pure_analysis

epsilon = 0.1
counts = pure_analysis('bell', epsilon, simulate=True)
print(counts)

data = pd.DataFrame({'c[5]': [s for s in counts], 'n': [counts[s] for s in counts]})
print('dataframe')
print(data)

isEntangled = detect_entanglement(data, epsilon, pure=True, tolerance=epsilon)

print("Entangled? {}".format(isEntangled))
