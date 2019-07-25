"""CPU functionality."""

import sys
import re

# PC Mutators:
# CALL = 0b01010000
# RET = 0b00010001
# INT = 0b01010010
# IRET = 0b00010011
# JMP = 0b01010100
# JEQ = 0b01010101
# JNE = 0b01010110
# JGT = 0b01010111
# JLT = 0b01011000
# JLE = 0b01011001
# JGE = 0b01011010

# Other
# NOP = 0b00000000
# LD = 0b10000011
# ST = 0b10000100
# PUSH = 0b01000101 
# POP = 0b01000110 
# PRA = 0b01001000 


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Memory:
        self.ram = [0] * 256
        # Registers:
        self.pc = 0  # Program Counter: Address of the current instruction
        self.ir = 0  # Instruction Register: Copy of self.pc
        self.mar = 0 # Memory Address Register: Holds memory address being read/written
        self.mdr = 0 # Memory Data Register: Holds value to write or value just read
        self.fl = 0  # Flags: L, G or E (See LS8 Spec)
        # Branch Table
        self.branchtable = {
            0b10100000: 'ADD',
            0b10100001: 'SUB',
            0b10100010: 'MUL',
            0b10100011: 'DIV',
            0b10100100: 'MOD',
            0b01100101: 'INC',
            0b01100110: 'DEC',
            0b10100111: 'CMP',
            0b10101000: 'AND',
            0b01101001: 'NOT',
            0b10101010: 'OR',
            0b10101011: 'XOR',
            0b10101100: 'SHL',
            0b10101101: 'SHR',
            0b00000001: 'HLT', 
            0b10000010: 'LDI',  
            0b01000111: 'PRN'
        }

        self.halted = False
        self.pointer = 0
        self.reg = [0]*8

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print('ERROR: No program specified from command line')
            self.halted = True
            return
    
        with open(f'{sys.argv[1]}') as f:
            raw_file = f.read()
        program = [int('0b'+s, 2) for s in raw_file.split() if re.match(r'\d{8}', s)]
        print(f'PROGRAM: {program}')
        
        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if self.branchtable[op] == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif self.branchtable[op] == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif self.branchtable[op] == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif self.branchtable[op] == 'DIV':
            if reg_b == 0:
                print('Error: Cannot divide by 0')
                # Break loop
                self.halted = True
            else:
                self.reg[reg_a] = int(self.reg[reg_a] / self.reg[reg_b])
        elif self.branchtable[op] == 'MOD':
            if reg_b == 0:
                print('Error: Cannot modulus by 0')
                # Break loop
                self.halted = True
            else:
                self.reg[reg_a] %= self.reg[reg_b]
        elif self.branchtable[op] == 'INC':
            self.reg[reg_a] += 1
        elif self.branchtable[op] == 'DEC':
            self.reg[reg_a] -= 1
        else:
            raise Exception("Unsupported ALU operation")

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

        # Run through program
        self.halted = False
        while not self.halted:
            self.ir = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2)

            if self.branchtable[self.ir] in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'INC', 'DEC']:
                self.alu(self.ir, self.operand_a, self.operand_b)
                if self.branchtable[self.ir] in ['INC', 'DEC']:
                    self.pc += 2
                else:
                    self.pc += 3

            elif self.branchtable[self.ir] == 'LDI':
                # Set the value or a register to an integer
                self.reg[self.operand_a] = self.operand_b
                self.pc += 3
            elif self.branchtable[self.ir] == 'PRN':
                print(self.reg[self.operand_a])
                self.pc += 2

            # Look at next instruction (if one exists)
            if self.branchtable[self.ram[self.pc]] == 'HLT' or not self.ram[self.pc]:
                self.halted = True
        return


    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, value, address):
        # should accept a value to write, and the address to write it to.
        if not value:
            print('Please provide a value to store in memory.')
            return
        if not self.ram[address]:
            print('Please provide a valid memory address.')
            return
        self.ram[address] = value