import numpy as np
import math
import random

class QuantumMachine(object):
    def __init__(self,initial_state=0,qubits=1) -> None:
        self.qubits= qubits
        # an array with 4 elements to represent a state of 2 spin particles
        self.state = np.array([0]*(2**qubits),dtype=np.csingle)

        self.state[initial_state]=1.0 + 0.0j;

    #helper function to print current state
    def print_state(self):
        print(self.state)

    def I(self,position=0) -> None:#the X gate
        operator = np.array([[1,0],[]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)

    def X(self,position=0) -> None:#the X gate
        operator = np.array([[0,1],[1,0]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)

    def Y(self,position=0) -> None:#the Y gate
        operator = np.array([[0,-1j],[1j,0]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)

    def Z(self,position=0) -> None:#the Z gate
        operator = np.array([[1,0],[0,-1]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)

    def H(self,position=0) -> None:#the Hadamard gate
        operator = 1/math.sqrt(2)*np.array([[1,1],[1,-1]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)

    def phase_gate(self, phase,position=0) -> None:#the General gate
        operator = np.array([[1,0],[0,math.e**(phase*1j)]],dtype=np.csingle)
        operator = self.construct_matrix_for_single_qubit_op(position,operator)
        self.apply_gate(operator)
    
    def measure(self,qubit=0):
        # 0=up, 1=down
        m_0 = np.array([[1,0],[0,0]],dtype=np.csingle)
        m_1 = np.array([[0,0],[0,1]],dtype=np.csingle)

        # step 1
        m0_matrix = self.construct_matrix_for_single_qubit_op(qubit,m_0)
        m1_matrix = self.construct_matrix_for_single_qubit_op(qubit,m_1)
        statevector_clone_0 = np.copy(self.state)
        statevector_clone_1 = np.copy(self.state)

        # step 2
        vec_0 = np.matmul(m0_matrix,statevector_clone_0)
        vec_1 = np.matmul(m1_matrix,statevector_clone_1)

        #step 3: calculating probabilities
        prob_0 = (np.abs(vec_0)**2).sum()
        prob_1 = (np.abs(vec_1)**2).sum()


        weights=[prob_0,prob_1]
        options =[0,1]

        #result of the measurement for the qubit
        result=random.choices(options,weights=weights,k=1)
        #for this result calculate the next state vector
        if (result[0]==0):
            operator = m0_matrix
        else:
            operator = m1_matrix

        self.apply_gate(operator)
        self.normalize()
        return result[0]

    # 2-consequtive qubits Gates
    def CNOT(self,control,target):
        operator=None
        cnot_forward = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
        cnot_reverse = np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])

        if(abs(control-target)==1):
            if(control<target):
                operator=self.construct_matrix_for_double_qubit_op(control,cnot_forward)
            else:
                operator=self.construct_matrix_for_double_qubit_op(target,cnot_reverse)
        else:
            print("Can only be applied to consecutive bits")
            exit(1)
        self.apply_gate(operator)

    def SWAP(self,first,second):
        operator=None
        if(abs(first-second)==1):
            operator=self.construct_matrix_for_double_qubit_op(first,np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]))
        else:
            print("Can only be applied to consecutive bits")
            exit(1)
        self.apply_gate(operator)

    def apply_gate(self,matrix) -> None:
        self.state = np.matmul(matrix,self.state)

    def construct_matrix_for_single_qubit_op(self,position,matrix):
        #performing Kronecker product to evaluate a full system matrix
        # for this particular single qbit gate and then multiply with the state vector to transform it!
        final_matrix = None
        for i in range(0,self.qubits):
            if(i != position):
                if(final_matrix is None):
                    final_matrix = np.eye(2)
                else:
                    final_matrix = np.kron(final_matrix,np.eye(2))#tensor product of matrices
            else:
                if(final_matrix is None):
                    final_matrix = matrix
                else:
                    final_matrix = np.kron(final_matrix,matrix)#tensor product of matrices

        return final_matrix

    def construct_matrix_for_double_qubit_op(self,position,matrix):
        #performing Kronecker product to evaluate a full system matrix
        # for this particular single qbit gate and then multiply with the state vector to transform it!
        final_matrix = None
        for i in range(0,self.qubits):
            if( i!=position and i!=(position+1) ):
                if(final_matrix is None):
                    final_matrix = np.eye(2)
                else:
                    final_matrix = np.kron(final_matrix,np.eye(2))#tensor product of matrices
            elif(i!=(position+1)):
                if(final_matrix is None):
                    final_matrix = matrix
                else:
                    final_matrix = np.kron(final_matrix,matrix)#tensor product of matrices

        return final_matrix

    def construct_matrix_for_triple_qubit_op(self,position,matrix):
        #performing Kronecker product to evaluate a full system matrix
        # for this particular single qbit gate and then multiply with the state vector to transform it!
        final_matrix = None
        for i in range(0,self.qubits):
            if( i!=position and i!=(position+1) and i!=(position+2) ):
                if(final_matrix is None):
                    final_matrix = np.eye(2)
                else:
                    final_matrix = np.kron(final_matrix,np.eye(2))#tensor product of matrices
            elif(i!=(position+1) and i!=(position+2)):
                if(final_matrix is None):
                    final_matrix = matrix
                else:
                    final_matrix = np.kron(final_matrix,matrix)#tensor product of matrices

        return final_matrix


    def normalize(self):
        factor = np.sqrt((np.abs(self.state)**2).sum())
        self.state = self.state/factor
