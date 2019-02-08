# py-wvet-v2
In [this paper](https://arxiv.org/abs/1808.08246), S. Goswami et. al.
propose a method for detecting entanglement in a general (pure or
mixed) 2-qubit quantum state using weak measurements on two copies. 
This repository implements the method
on the 
[IBM Quantum Experience](https://quantumexperience.ng.bluemix.net/qx) using 
[Qiskit](https://github.com/Qiskit/qiskit-terra).

Additional work (which is in the included notes pdf) was done to utilize
one qubit additional qubit for making the weak measurements.

# Requirements
This code requires the Python packages [numpy](http://www.numpy.org/), 
[pandas](https://pandas.pydata.org/), and
[Qiskit](https://github.com/Qiskit/qiskit-terra).

# Usage
The file quantum\_analysis.py contains all code for interfacing with
the IBM Quantum Experience, either as a simulation or a real quantum
computer. classical\_analysis.py processes the results from
the quantum computations. analysis.py wraps the process.

# Credentials
To run on IBM Quantum Experience, you must provide valid IBM credentials
in a JSON named ibm\_creds.json. An example is provided as
example\_creds.json.
