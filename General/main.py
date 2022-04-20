from machine import QuantumMachine

def do_teleport(package):
    if(package == 0):
        initial_state = 0
    else:
        initial_state = 4

    machine = QuantumMachine(qubits=3,initial_state=initial_state)

    machine.H(1)
    machine.CNOT(1,2)

    machine.CNOT(0,1)
    machine.H(0)

    crz=machine.measure(0)
    crx=machine.measure(1)

    if(crx==1):
        machine.X(2)

    if(crz==1):
        machine.Z(2)

    result = machine.measure(2)

    #return the teleported qubit!
    return result


def main():
    
    for i in range(10):
        print("package: ",i%2," & the teleported Qubit is: ",do_teleport(i%2))


if(__name__ == "__main__"):
    main()





