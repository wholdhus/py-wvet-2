import pandas as pd
from classical_analysis import detect_entanglement
from quantum_analysis import pure_analysis, mixed_analysis

epsilon = 0.01
counts = pure_analysis('plusplus', 0.01, simulate=True)
print(counts)

data = pd.DataFrame({'c[5]': [s for s in counts], 'n': [counts[s] for s in counts]})
print('dataframe')
print(data)

isEntangled = detect_entanglement(data, 0.01, pure=True, tolerance=0.01)

print("Entangled? {}".format(isEntangled))
