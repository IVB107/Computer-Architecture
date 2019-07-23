"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Memory:
        self.ram = [00000000] * 256
        # Registers:
        self.pc = None  # Program Counter: Address of the current instruction
        self.ir = None  # Instruction Register: Copy of self.pc
        self.mar = None # Memory Address Register: Holds memory address being read/written
        self.mdr = None # Memory Data Register: Holds value to write or value just read
        self.fl = None  # Flags: L, G or E (See LS8 Spec)

        self.pointer = None
        self.reg = []

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

        ADD = 0b10100000
        SUB = 0b10100001
        MUL = 0b10100010
        DIV = 0b10100011
        MOD = 0b10100100

        INC = 0b01100101
        DEC = 0b01100110

        CMP = 0b10100111

        AND = 0b10101000
        NOT = 0b01101001
        OR = 0b10101010
        XOR = 0b10101011
        SHL = 0b10101100
        SHR = 0b10101101

        while self.pc is not HLT:
            self.ir = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2)

            if self.ir == ADD:
                self.operand_a += self.operand_b
            elif self.ir == SUB:
                self.operand_a -= self.operand_b
            elif self.ir == MUL:
                self.operand_a *= self.operand_b
            elif self.ir == DIV:
                if self.operand_b == 0:
                    print('Error: Cannot divide by 0')
                    self.ir = HLT
                else:
                    self.operand_a = int(self.operand_a/self.operand_b)
            elif self.ir == MOD:
                if self.operand_b == 0:
                    print('Error: Cannot modulus by 0')
                    self.ir = HLT
                else:
                    self.operand_a %= self.operand_b
            
            # Look at next instruction
            self.pc += 1

            # elif self.ir == INC:
            #     self.ir = self.ram_read(self.pc + 1)
            # elif self.ir == DEC:
            #     self.ir = self.ram_read(self.pc - 1)


    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        if self.ram[address]:
            return self.ram[address]
        return None

    def ram_write(self, value, address):
        # should accept a value to write, and the address to write it to.
        if not value:
            print('Please provide a value to store in memory.')
            return
        if not self.ram[address]:
            print('Please provide a valid memory address.')
            return
        self.ram[address] = value