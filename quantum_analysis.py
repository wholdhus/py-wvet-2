from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, IBMQ
import qiskit as qk

IBMQ.enable_account(QX_TOKEN, QX_URL)

simulate = True

class ExtendedQuantumCircuit(QuantumCircuit):
    
    def crx(self, theta, ctl, tgt):
        self.h(tgt)
        self.crz(theta, ctl, tgt)
        self.h(tgt)

    def ccrx(self, theta, ctl1, ctl2, tgt):
        """ Based on fig. 4.8 in text with
        V = rx(theta/2) """
        self.crx(theta/2, ctl2, tgt)
        self.cx(ctl1, ctl2)
        self.crx(-theta/2, ctl2, tgt)
        self.cx(ctl1, ctl2)
        self.crx(theta/2, ctl1, tgt)

    def cch(self, ctl1, ctl2, tgt):
        """ Based on cH but turning cnots into ccnots """
        self.h(ctl1)
        self.h(ctl2)
        self.s(ctl1)
        self.s(ctl2)
        self.h(tgt)
        self.sdg(tgt) # S^dagger
        self.ccx(ctl1, ctl2, tgt)
        self.h(tgt)
        self.t(tgt)
        self.ccx(ctl1, ctl2, tgt)
        self.t(tgt)
        self.h(tgt)
        self.s(tgt)
        self.x(tgt)

    def cccrx(self, theta, ctl1, ctl2, ctl3, tgt):
        self.crx(theta/2, ctl3, tgt)
        self.ccx(ctl1, ctl2, ctl3)
        self.crx(-theta/2, ctl3, tgt)
        self.ccx(ctl1, ctl2, ctl3)
        self.ccrx(theta/2, ctl2, ctl3, tgt)
        

qr = QuantumRegister(5) # we need 5 qbits
c = ClassicalRegister(5)
qc = ExtendedQuantumCircuit(qr, c)

epsilon = 0.001
theta = -2*epsilon

# Building bell state
qc.h(qr[0])
qc.cx(qr[0], qr[1])
qc.h(qr[2])
qc.cx(qr[2], qr[3])

# Building the circuit
qc.rx(-theta, qr[3])
qc.crx(theta, qr[0], qr[3])
qc.crx(-theta, qr[0], qr[2])
qc.ccrx(theta, qr[0], qr[1], qr[2])
qc.ccrx(-theta, qr[0], qr[1], qr[3])
qc.cch(qr[0], qr[1], qr[2])
qc.cccrx(2*theta, qr[0], qr[1], qr[2], qr[3])
qc.cch(qr[0], qr[1], qr[2])


# Measure
qc.measure(qr, c)

# Optimizing if possible
qc.optimize_gates()


# print available backends
# print("IBMQ backends: ", IBMQ.backends())

if simulate:
    backend = IBMQ.get_backend('ibmq_qasm_simulator')
    job = execute(qc, backend)
    result = job.result()

    print(result)
    print(result.get_counts())

else:
    backend_ibmq = IBMQ.get_backend('ibmqx4')
    job_ibmq = execute(qc, backend_ibmq)
    result_ibmq = job_ibmq.result()

    print("real execution results: ", result_ibmq)
    print(result_ibmq.get_counts(qc))