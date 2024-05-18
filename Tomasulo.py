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
    def clean(self):
        self.name = None
        self.op_type = None
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
        elif self.op == "STORE":  # STORE RS2, offset(RS1)
            tempvec = self.splitstring(vec[2], "(")
            self.rs2 = vec[1]
            self.offset = int(tempvec[0])
            self.rs1 = tempvec[1][:-1]
        elif self.op == "BEQ":  # BEQ RS1, RS2, offset
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


class Tomasulo:
    def __init__(self):
        self.instructions = []
        self.remaining_instructions = []
        self.current_cycle = 0
        self.pc = 0
        self.total_write_backs = 0

        self.branches=0
        self.mispredictions=0
        self.execution_flag = True # it is false whenever there is a branch or Call and we are waiting for them

    def get_instructions(self):
        self.instructions.append(Instruction("LOAD R2 1(R0)"))
        self.instructions.append(Instruction("LOAD R3 2(R0)"))
        # self.instructions.append(Instruction("BEQ R0 R0 2"))
        self.instructions.append(Instruction("CALL 2"))
        self.instructions.append(Instruction("ADD R4 R2 R3"))
        self.instructions.append(Instruction("MUL R5 R2 R3"))
        self.instructions.append(Instruction("NAND R6 R2 R3"))
        self.instructions.append(Instruction("ADD R10 R4 R6"))
        self.instructions.append(Instruction("ADD R11 R10 R3"))
        self.instructions.append(Instruction("ADD R12 R4 R3"))
        self.instructions.append(Instruction("ADDI R14 R14 100"))

        for inst in self.instructions:
            self.remaining_instructions.append(inst)

    def is_finished(self):
        # Check if current cycle is zero
        if self.current_cycle == 0:
            return False
        # Loop over all reservation stations
        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                # If any reservation station is busy, return False
                if rs.busy:
                    return False

        # If all reservation stations are free, return True
        return True
    def run(self):
        #while self.total_write_backs < len(self.instructions):
        while self.total_write_backs < len(self.instructions):
            self.current_cycle += 1
            self.write_back()
            self.execute()
            self.issue()
            if self.is_finished():
                break
        print_timing_table(self.instructions)
        print_registers(registers)



    def issue(self):
        global reservation_stations, registers
        if 0 <= self.pc < len(self.instructions):
            inst = self.instructions[self.pc]
            if inst.op=="ADDI":
                rs_list = reservation_stations["ADD"]
            else:
                rs_list = reservation_stations[inst.op]
            for rs in rs_list:
                if not rs.busy:
                    inst.issue_time = self.current_cycle
                    print("inst issued", inst.inst)
                    rs.instruction = inst
                    rs.busy = True
                    rs.op = inst.op
                    rs.cycles = get_cycles(inst.op)

                    if inst.rs1!="":
                        if registers[inst.rs1].busy:
                            rs.qj = registers[inst.rs1].reorder
                        else:
                            rs.vj = registers[inst.rs1].value

                    if inst.rs2!="":
                        if registers[inst.rs2].busy:
                            rs.qk = registers[inst.rs2].reorder
                        else:
                            rs.vk = registers[inst.rs2].value

                    if inst.rd != "":
                        registers[inst.rd].busy = True
                        registers[inst.rd].reorder = rs.name
                    self.pc += 1  # Move to the next instruction
                    break

    def execute(self):
        if self.execution_flag:
            for op, rs_list in reservation_stations.items():
                for rs in rs_list:
                    if rs.busy and rs.qj is None and rs.qk is None:
                        if rs.instruction.start_exec_time == 0:
                            rs.instruction.start_exec_time = self.current_cycle
                            if rs.instruction.op in ["BEQ", "RET", "CALL"]:
                                self.execution_flag = False
                                if rs.instruction.op == "BEQ":
                                    registers["R0"].value = self.pc
                        rs.cycles -= 1
                        rs.instruction.cycles_left_in_execution -= 1
                        if rs.cycles == 0 :
                            if rs.op == "LOAD":
                                rs.result = Memory[rs.instruction.offset + rs.vj]
                            if rs.op == "STORE":
                                # rs.resul=None
                                Memory[rs.instruction.offset + rs.instruction.vj] = rs.instruction.vk
                            if rs.op == "BEQ":
                                self.branches += 1
                                self.execution_flag = True
                                if rs.vj == rs.vk:
                                    # self.pc += rs.instruction.label
                                    self.pc = registers["R0"].value+ rs.instruction.label

                                    self.mispredictions += 1
                            if rs.op == "CALL":
                                registers["R1"].value = self.pc+1
                                self.pc = rs.instruction.label
                                self.execution_flag = True
                            if rs.op == "RET":
                                self.pc = registers["R1"].value  # jump to the last call

                            if rs.op == "ADD":
                                rs.result = rs.vj + rs.vk
                            elif rs.op == "ADDI":
                                rs.result = rs.vj + rs.instruction.imm
                            elif rs.op == "NAND":
                                rs.result = ~(rs.vj & rs.vk) & 0xFFFF  # Ensure 16-bit result
                            elif rs.op == "MUL":
                                rs.result = (rs.vj * rs.vk) & 0xFFFF  # Ensure 16-bit result
                            print("done_excution", rs.instruction.inst, "at cycle", self.current_cycle)
                            rs.instruction.end_exec_time = self.current_cycle
                            rs.ready = True


    def write_back(self):
        station = None
        value = None

        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                if rs.ready:
                    print("wb",rs.instruction.inst, "at cycle", self.current_cycle)
                    rs.instruction.wb_time = self.current_cycle
                    self.total_write_backs += 1
                    station = rs.name
                    value = rs.result
                    rs.ready = False
                    rs.busy = False
                    # rs.clean()

                    if(rs.instruction.op=="ADDI"):
                        print(rs.result, rs.vj, rs.vk, rs.instruction.imm)
                    for reg in registers.values():
                        if reg.reorder == station:
                            reg.value = value
                            reg.busy = False
                            reg.reorder = None

        if station:
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
        print(f"{inst.inst:<10} {inst.issue_time:<10} {inst.start_exec_time:<15} {inst.end_exec_time:<15} {inst.wb_time:<10}")

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
# registers = {f"R{i}": Register() for i in range(8)}
# registers["R0"].value = 0
# registers["R2"].value = 10
# registers["R3"].value = 20

registers = {f"R{i}": Register() for i in range(30)}
registers["R0"].value = 0


Memory=[]  #Memory size is 64 slots right now
for i in range(10):
    Memory.append(i*10)

# Test the program
tomasulo = Tomasulo()
tomasulo.get_instructions()
tomasulo.run()

