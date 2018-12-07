import json
import time
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
import qiskit as qk

with open('ibm_creds.json') as json_file:
    IBMDict = json.load(json_file)
    QX_TOKEN = IBMDict['qx_token']
    QX_URL = IBMDict['qx_url']

qk.IBMQ.enable_account(QX_TOKEN, QX_URL)

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


def bell_state(qc, qr1, qr2):
    # Building bell state that entangles the qubits at given quantum registers
    qc.h(qr1)
    qc.cx(qr1, qr2)


def finish_and_run(qr, c, qc, simulate=True):
    # Measure
    qc.measure(qr, c)
    # Optimizing if possible
    qc.optimize_gates()
    if simulate:
        backend = qk.IBMQ.get_backend('ibmq_qasm_simulator')
    else:
        backend= qk.IBMQ.get_backend('ibmqx4')
    # job = qk.execute(qc, backend)
    qobj = qk.compile(qc, backend, shots=8192)
    job = backend.run(qobj)
    start_time = time.time()

    job_status = job.status()
    while job_status.name != 'DONE':
        print(f'Status @ {time.time()-start_time:0.0f} s: {job_status.name},'
              f' est. queue position: {job.queue_position()}')
        time.sleep(10)
        job_status = job.status()

    result = job.result()
    # print('Results: {}'.format(result))
    # print(result.get_counts())
    return result.get_counts()


def mixed_analysis(state1, state2, epsilon, simulate=True):
    theta = -2*epsilon

    qr = QuantumRegister(5)
    c = ClassicalRegister(5)
    qc = ExtendedQuantumCircuit(qr, c)

    if state1 == 'bell':
        bell_state(qc, qr[0], qr[1])
    elif state1 == 'plusplus':
        qc.h(qr[0])
        qc.h(qr[1])

    if state2 == 'bell':
        bell_state(qc, qr[2], qr[3])
    elif state1 == 'plusplus':
        qc.h(qr[2])
        qc.h(qr[3])

    # Building the circuit
    qc.rx(-theta, qr[3])
    qc.crx(theta, qr[0], qr[3])
    qc.crx(-theta, qr[0], qr[2])
    qc.ccrx(theta, qr[0], qr[1], qr[2])
    qc.ccrx(-theta, qr[0], qr[1], qr[3])
    qc.cch(qr[0], qr[1], qr[2])
    qc.cccrx(2*theta, qr[0], qr[1], qr[2], qr[3])
    qc.cch(qr[0], qr[1], qr[2])

    return finish_and_run(qr, c, qc, simulate)


def pure_analysis(state, epsilon, simulate=True):
    theta = 2*epsilon # so rotations are e^-i*epsilon

    qr = QuantumRegister(5)
    c = ClassicalRegister(5)
    qc = ExtendedQuantumCircuit(qr, c)

    if state == 'bell':
        bell_state(qc, qr[0], qr[1])
        bell_state(qc, qr[2], qr[3])
    elif state == 'plusplus':
        for i in range(4):
            qc.h(qr[i])

    qc.rx(theta, qr[3])
    qc.h(qr[4])
    qc.ry(theta, qr[4])

    return finish_and_run(qr, c, qc, simulate)
