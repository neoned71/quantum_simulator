import numpy as np
import math

class QuantumMachine(object):
    def __init__(self,qbits=2) -> None:
        self.qbits = qbits

        #state describes probability amplitudes for different possible states of the machine
        #e.g. if the state is => a|00> + b|01> + c|10> + d|11>, then state vector = [a,b,c,d]
        self.state = np.array([0]*(2**qbits),dtype=np.csingle)


        # starting with state with probability amplitude = 1
        self.state[4]=1.+0.j


    def construct_matrix(self,position,matrix):
        #performing Kronecker product to evaluate a full system matrix
        # for this particular single qbit gate and then multiply with the state vector to transform it!
        final_matrix = None
        for i in range(0,self.qbits):
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

        self.state = np.matmul(final_matrix,self.state)

    def construct_matrix_2(self,position,matrix):
        #performing Kronecker product to evaluate a full system matrix
        # for this particular single qbit gate and then multiply with the state vector to transform it!
        final_matrix = None
        for i in range(0,self.qbits):
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
        #print(final_matrix)
        self.state = np.matmul(final_matrix,self.state)

    #helper function to print current state
    def print_state(self):
        print(self.state)

    #Single Qbit gates
    def X(self,position):#the X gate
        self.construct_matrix(position,np.array([[0,1],[1,0]]))
    
    def Y(self,position):#the Y gate
        self.construct_matrix(position,np.array([[0,-1j],[1j,0]]))

    def Z(self,position):#the Z gate
        self.construct_matrix(position,np.array([[1,0],[0,-1]]))

    def H(self,position):#the Hadammard gate
        self.construct_matrix(position,1/math.sqrt(2)*np.array([[1,1],[1,-1]]))

    def P(self,position,phase):#the P gate to construct S=P(phase=math.pi/2) and T=P(phase=math.pi/4) gates!! do it yourself if you need those gates.
        self.construct_matrix(position,np.array([[1,0],[0,math.e**(phase*1j)]]))

    # 2-consequtive Qbits Gates
    def CNOT(self,control,target):
        if(abs(control-target)==1):
            if(control>target):
                self.construct_matrix_2(target,np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))
            else:
                self.construct_matrix_2(control,np.array([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]]))
        else:
            print("Can only be applied to consecutive bits")

    def SWAP(self,first,second):
        if(abs(first-second)==1):
            # print("yes")
            self.construct_matrix_2(first,np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]]))
        else:
            # print("no")
            print("Can only be applied to consecutive bits")

def main():
    machine = QuantumMachine(qbits=3)

    #CNOT (0,2) can be applied using 2 swaps!
    machine.SWAP(0,1)
    machine.CNOT(1,2)
    machine.SWAP(0,1)

    # machine.X(0)# use NOT gate on qbit n
    # machine.H(1)# use Haddamard gate on qbit n
    print("Final State of the Quantum Machine:")
    machine.print_state()#printing the state of the machine!!

if(__name__ == "__main__"):
    main()