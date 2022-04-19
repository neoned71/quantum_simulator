import numpy as np
import math
import random

class QuantumMachineDouble(object):
    def __init__(self,initial_state=0) -> None:
        # an array with 4 elements to represent a state of 2 spin particles
        self.state = np.array([0,0,0,0],dtype=np.csingle)

        self.state[initial_state]=1.0 + 0.0j;

    #helper function to print current state
    def print_state(self):
        print(self.state)

    def I(self,position=0) -> None:#the X gate
        operator = np.array([[1,0],[]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def X(self,position=0) -> None:#the X gate
        operator = np.array([[0,1],[1,0]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def Y(self,position=0) -> None:#the Y gate
        operator = np.array([[0,-1j],[1j,0]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def Z(self,position=0) -> None:#the Z gate
        operator = np.array([[1,0],[0,-1]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def H(self,position=0) -> None:#the Hadamard gate
        operator = 1/math.sqrt(2)*np.array([[1,1],[1,-1]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def phase_gate(self, phase,position=0) -> None:#the General gate
        operator = np.array([[1,0],[0,math.e**(phase*1j)]],dtype=np.csingle)
        self.apply_gate(operator,position)

    def apply_gate(self,matrix=np.array([[1,0],[0,1]]),position=0) -> None:
        identity =np.array([[1,0],[0,1]])
        f=None
        if position==0:
            f=np.kron(matrix,identity)
        else:
            f=np.kron(identity,matrix)
        self.state = np.matmul(f,self.state)

    #this measuement does not collapse the wave function. This is not a single qubit measurement but the whole system measurement!
    def measurement(self):
        weights= np.abs(self.state)
        options = range(len(self.state))
        return random.choices(options,weights=weights,k=1)

    
    # def measure(self,qubit=0):
    #     m_0 = np.array([[1,0],[0,1]],dtype=csingle)
    #     m_1 = np.array([[1,0],[0,1]],dtype=csingle)
    #     weights= np.abs(self.state)
    #     options = range(len(self.state))
    #     return random.choices(options,weights=weights,k=1)

    # 2-consequtive Qbits Gates
    def CNOT(self,control,target):
        if(control<target):
            self.state = np.matmul(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]),self.state)
        else:
            self.state = np.matmul(np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]),self.state)

    def SWAP(self):
            self.state = np.matmul(np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]),self.state)
