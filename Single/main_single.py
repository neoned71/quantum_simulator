from single_qubit_machine import QuantumMachineSingle


def main():
    machine = QuantumMachineSingle()
    print("\n Initial State:")
    machine.print_state()#printing the state of the machine!!

    machine.H()

    print(machine.measurement())
    print(machine.measurement())
    print(machine.measurement())
    print(machine.measurement())
    

    print("\n Final State:")
    machine.print_state()#printing the state of the machine!!

if(__name__ == "__main__"):
    main()