from double_qubit_machine import QuantumMachineDouble


def main():
    machine = QuantumMachineDouble()
    print("\n Initial State:")
    machine.print_state()#printing the state of the machine!!
    machine.H(0)
    machine.CNOT(0,1)
    

    print("\n Entangled state State:")
    machine.print_state()#printing the state of the machine!!

    print("\n Measurements")
    
    for i in range(20):
        print(str(i)+" index:"+str(machine.measurement()))


if(__name__ == "__main__"):
    main()
