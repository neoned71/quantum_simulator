import numpy as np
import math
import random

class QuantumMachineSingle(object):
    def __init__(self,up=True) -> None:

        # an array with 2 elements, one for UP and one for DOWN state!
        self.state = np.array([0,0],dtype=np.csingle)

        if up:
            #initialize the state up=1, essentially setting it to purely UP state
            self.state[0]=1.+0.j
        else:
            #initialize the state down=1, essentially setting it to purely DOWN state
            self.state[1]=1.+0.j

    #helper function to print current state
    def print_state(self):
        print(self.state)

    #Single Qbit gates
    def X(self) -> None:#the X gate
        operator = np.array([[0,1],[1,0]],dtype=np.csingle)
        self.apply_gate(operator)

    def Y(self) -> None:#the Y gate
        operator = np.array([[0,-1j],[1j,0]],dtype=np.csingle)
        self.apply_gate(operator)

    def Z(self) -> None:#the Z gate
        operator = np.array([[1,0],[0,-1]],dtype=np.csingle)
        self.apply_gate(operator)

    def H(self) -> None:#the Hadamard gate
        operator = 1/math.sqrt(2)*np.array([[1,1],[1,-1]],dtype=np.csingle)
        self.apply_gate(operator)

    def phase_gate(self, phase) -> None:#the General gate
        operator = np.array([[1,0],[0,math.e**(phase*1j)]],dtype=np.csingle)
        self.apply_gate(operator)

    def apply_gate(self,matrix=np.array([[1,0],[0,1]])) -> None:
        self.state = np.matmul(matrix,self.state)

    def measurement(self):
        weights= np.abs(self.state)
        options = range(len(self.state))
        return random.choices(options,weights=weights,k=1)

    # def H(self,position):#the Hadammard gate
    #     self.construct_matrix(position,1/math.sqrt(2)*np.array([[1,1],[1,-1]]))

    # def P(self,position,phase):#the P gate to construct S=P(phase=math.pi/2) and T=P(phase=math.pi/4) gates!! do it yourself if you need those gates.
    #     self.construct_matrix(position,np.array([[1,0],[0,math.e**(phase*1j)]]))

    # 2-consequtive Qbits Gates
    # def CNOT(self,control,target):
    #     if(abs(control-target)==1):
    #         if(control>target):
    #             self.construct_matrix_2(target,np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))
    #         else:
    #             self.construct_matrix_2(control,np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]))
    #     else:
    #         print("Can only be applied to consecutive bits")

    # def SWAP(self,first,second):
    #     if(abs(first-second)==1):
    #         # print("yes")
    #         self.construct_matrix_2(first,np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]))
    #     else:
    #         # print("no")
    #         print("Can only be applied to consecutive bits")
