from collections import deque

class ReservationStation:
    def __init__(self, name, op_type):
        self.name = name
        self.op_type = op_type
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.result = None
        self.cycles = 0

        # To associate the instruction to reservation station
        self.instruction = None
        self.ready = False

class Register:
    def __init__(self):
        self.value = 0
        self.busy = False
        self.reorder = None

class Instruction:
    def __init__(self, inst=""):
        self.inst = inst
        self.op = ""
        self.imm = 0
        self.label = 0
        self.offset = 0
        self.rd = ""
        self.rs1 = ""
        self.rs2 = ""

        # New Attributes added by tawfik:
        self.cycles_left_in_execution = 0
        self.issue_time = 0
        self.start_exec_time = 0
        self.end_exec_time = 0
        self.wb_time = 0

        if inst:
            self.obtain()

    def obtain(self):
        self.inst = self.inst.replace(",", "")
        vec = self.inst.split()
        self.op = vec[0]
        if self.op in ["ADD", "NAND", "MUL"]:  # ADD RD, Rs1, Rs2 // NAND RD, Rs1, Rs2 // DIV RD, Rs1, Rs2
            self.rd = vec[1]
            self.rs1 = vec[2]
            self.rs2 = vec[3]
        elif self.op == "ADDI":  # ADDI RD, Rs1, imm
            self.rd = vec[1]
            self.rs1 = vec[2]
            self.imm = int(vec[3])
        elif self.op == "LOAD":  # LOAD RD, offset(RS1)
            tempvec = self.splitstring(vec[2], "(")
            self.rd = vec[1]
            self.offset = int(tempvec[0])
            self.rs1 = tempvec[1][:-1]
        elif self.op == "STORE":  # STORE RS2, offset(RS2)
            tempvec = self.splitstring(vec[2], "(")
            self.rs2 = vec[1]
            self.offset = int(tempvec[0])
            self.rs1 = tempvec[1][:-1]
        elif self.op == "BNE":  # BNE RS1, RS2, offset
            self.rs1 = vec[1]
            self.rs2 = vec[2]
            self.label = int(vec[3])
        elif self.op == "CALL":  # CALL label
            self.label = int(vec[1])
        elif self.op == "RET":  # RET
            return

        self.cycles_left_in_execution = get_cycles(self.op)

    def splitstring(self, string, delimiter):
        return string.split(delimiter)

def get_cycles(op):
    cycle_dict = {
        "LOAD": 6,
        "STORE": 6,
        "ADD": 2,
        "NAND": 1,
        "MUL": 8,
        "BEQ": 1,
        "CALL": 1,
        "RET": 1
    }
    return cycle_dict.get(op, 1)

class CommonDataBus:
    def __init__(self):
        self.value = None
        self.station = None

class Tomasulo:
    def __init__(self):
        self.instructions = []
        self.remaining_instructions = []
        self.current_cycle = 0
        self.pc = 0
        self.total_write_backs = 0

    def get_instructions(self):
        self.instructions.append(Instruction("ADD R1 R2 R3"))
        self.instructions.append(Instruction("MUL R5 R2 R3"))
        self.instructions.append(Instruction("NAND R4 R2 R3"))
        for inst in self.instructions:
            self.remaining_instructions.append(inst)

    def run(self):
        while self.total_write_backs < len(self.instructions):
            self.current_cycle += 1
            self.write_back()
            self.execute()
            self.issue()
        print_timing_table(self.instructions)
        print_registers(registers)



    def issue(self):
        global reservation_stations, registers

        if 0 <= self.pc < len(self.instructions):
            inst = self.instructions[self.pc]
            rs_list = reservation_stations[inst.op]
            for rs in rs_list:
                if not rs.busy:
                    inst.issue_time = self.current_cycle
                    rs.instruction = inst
                    rs.busy = True
                    rs.op = inst.op
                    rs.cycles = get_cycles(inst.op)

                    if registers[inst.rs1].busy:
                        rs.qj = registers[inst.rs1].reorder
                    else:
                        rs.vj = registers[inst.rs1].value

                    if registers[inst.rs2].busy:
                        rs.qk = registers[inst.rs2].reorder
                    else:
                        rs.vk = registers[inst.rs2].value

                    registers[inst.rd].busy = True
                    registers[inst.rd].reorder = rs.name
                    self.pc += 1  # Move to the next instruction
                    break

    def execute(self):
        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                if rs.busy and rs.qj is None and rs.qk is None:
                    if rs.instruction.start_exec_time == 0:
                        rs.instruction.start_exec_time = self.current_cycle
                    rs.cycles -= 1
                    rs.instruction.cycles_left_in_execution -= 1
                    if rs.instruction.cycles_left_in_execution == 0:
                        if rs.op == "ADD":
                            rs.result = rs.vj + rs.vk
                        elif rs.op == "NAND":
                            rs.result = ~(rs.vj & rs.vk) & 0xFFFF  # Ensure 16-bit result
                        elif rs.op == "MUL":
                            rs.result = (rs.vj * rs.vk) & 0xFFFF  # Ensure 16-bit result

                        # if rs.instruction.cycles_left_in_execution == 0:
                        rs.instruction.end_exec_time = self.current_cycle
                        rs.ready = True
                        rs.busy = False

    def write_back(self):
        station = None
        value = None
        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                if rs.ready:
                    rs.instruction.wb_time = self.current_cycle
                    self.total_write_backs += 1
                    station = rs.name
                    value = rs.result
                    rs.ready = False
                    break

        if station:
            for reg in registers.values():
                if reg.reorder == station:
                    reg.value = value
                    reg.busy = False
                    reg.reorder = None

            for op2, rs_list2 in reservation_stations.items():
                for rs in rs_list2:
                    if rs.qj == station:
                        rs.vj = value
                        rs.qj = None
                    if rs.qk == station:
                        rs.vk = value
                        rs.qk = None
def print_registers(registers):
       print("Registers:")
       for reg_name, reg in registers.items():
           print(f"{reg_name}: {'BUSY' if reg.busy else 'FREE'}, Value: {reg.value}")

def print_timing_table(instructions):
    # Print headers
    print(f"{'Inst':<10} {'Issue':<10} {'Start Execute':<15} {'End Execute':<15} {'WB':<10}")

    # Print each instruction's timing
    for i, inst in enumerate(instructions):
        print(f"{i:<10} {inst.issue_time:<10} {inst.start_exec_time:<15} {inst.end_exec_time:<15} {inst.wb_time:<10}")

# Initialize reservation stations
reservation_stations = {
    'LOAD': [ReservationStation(f"LOAD{i}", 'LOAD') for i in range(2)],
    'STORE': [ReservationStation(f"STORE{i}", 'STORE') for i in range(1)],
    'ADD': [ReservationStation(f"ADD{i}", 'ADD') for i in range(4)],
    'NAND': [ReservationStation(f"NAND{i}", 'NAND') for i in range(2)],
    'MUL': [ReservationStation(f"MUL{i}", 'MUL') for i in range(1)],
    'BEQ': [ReservationStation(f"BEQ{i}", 'BEQ') for i in range(1)],
    'CALL': [ReservationStation(f"CALL{i}", 'CALL') for i in range(1)],
    'RET': [ReservationStation(f"RET{i}", 'RET') for i in range(1)],
}

# Initialize registers
registers = {f"R{i}": Register() for i in range(8)}
registers["R2"].value = 10
registers["R3"].value = 20

# Test the program
tomasulo = Tomasulo()
tomasulo.get_instructions()
tomasulo.run()
