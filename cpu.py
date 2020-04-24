"""CPU functionality."""

import sys # parse the comand line

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100
E = 0b00000001
L = 0b00000100
G = 0b00000010



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8 # the different mailboxes
        # [0,0,0,0,0,0,0,0]
        #self.registers[7] = 0xf4
        self.pc = 0 # program counter
        # In CPU, add method ram_read() and ram_write()
        # that access the RAM inside the CPU object.
        self.ram =  [0b100000000] # memory holds 256 bytes
        self.sp = 7
        self.FL = 0b00000000

    # You don't need to add the MAR or MDR to your CPU class,
    # but they would make handy parameter names for ram_read()
    # and ram_write(), if you wanted
    # mdr - data that was read or data to write
    # mar - data being read or written to
    def ram_read(self, mar):
        # should accept the address
        # to read and return the value stored there
        return self.ram[mar]


    def ram_write(self, mar, mdr):
        # should accept a value to write
        # and the address to write it to
        self.ram[mar]=mdr


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        try:
            with open(program_file_name) as f:
                for line in f:
                    line_string = line.split('#')[0].strip()
                    if line_string == '':
                        continue
                    instruction = int(line_string, 2)

                    self.ram[mar] = instruction
                    address += 1

        except Exception:
            import os
            raise FileNotFoundError(f"No File Name {program_file_name} in {os.getcwd()}")
        print(self.ram[:20])

        #for inst in program:
        #    self.ram[mar] = inst
        #    mar+=1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                print(f"A and B are equal")
                self.FL = 0b00000001 #[0b00000001]
            elif self.reg[reg_a] > self.reg[reg_b]:
                print("A is greater than B")
                self.FL = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                print("A is less than B")
                self.FL = 0b00000100
        else:
            raise Exception("Unsuported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        print("Running")
        while running:
            # read the memory address that is stored in the register pc,
            # then store that result in the IR (instruction register)
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            #else:
            elif IR == HLT:
                print("Execution Finished")
                running =False

            elif IR == PRN:
                # self.reg[r]
                print(self.reg[operand_a])
                self.pc += 2

            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                # decrement (decrease) the stack pointer
                self.reg[self.sp] -= 1
                # copy the value in the given register to the address thats pointed to by SP
                self.ram[self.reg[self.sp]] = val # come back and double check this line

            elif IR == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[self.sp]] # come back and double check this line
                self.reg[reg] = val
                self.reg[self.sp] += 1
                self.pc += 2

            elif IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif IR == JMP:
                # got to get the given register by looking at the nxt op code
                reg = self.ram[self.pc + 1]
                # set the pc to the address that is stored in the register
                self.pc = self.reg[reg]
            # else:
                # self.pc += 2

            elif IR == JNE:
                if self.FL != E:
                    # got to get the given register by looking at the nxt op code
                    reg = self.ram[self.pc + 1]
                    # set the pc to the address that is stored in the register
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2

            if IR == JEQ:
                if self.FL == E:
                    # got to get the given register by looking at the nxt op code
                    reg = self.ram[self.pc + 1]
                    # set the pc to the address that is stored in the register
                    self.pc = self.reg[reg]
                else:
                    self.pc += 2


# Your finished project must include all of the following requirements:

 # Add the CMP instruction and equal flag to your LS-8.

 # Add the JMP instruction.

 # Add the JEQ and JNE instructions.
