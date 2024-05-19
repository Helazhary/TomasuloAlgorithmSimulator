# import tkinter as tk
# from tkinter import ttk, filedialog, StringVar, Listbox, END
# from collections import deque

# class ReservationStation:
#     def __init__(self, name, op_type):
#         self.name = name
#         self.op_type = op_type
#         self.busy = False
#         self.op = None
#         self.vj = None
#         self.vk = None
#         self.qj = None
#         self.qk = None
#         self.result = None
#         self.cycles = 0
#         self.instruction = None
#         self.ready = False

#     def clean(self):
#         self.busy = False
#         self.op = None
#         self.vj = None
#         self.vk = None
#         self.qj = None
#         self.qk = None
#         self.result = None
#         self.cycles = 0
#         self.instruction = None
#         self.ready = False

# class Register:
#     def __init__(self):
#         self.value = 0
#         self.busy = False
#         self.reorder = None

# class Instruction:
#     def __init__(self, inst=""):
#         self.inst = inst
#         self.op = ""
#         self.imm = 0
#         self.label = 0
#         self.offset = 0
#         self.rd = ""
#         self.rs1 = ""
#         self.rs2 = ""
#         self.cycles_left_in_execution = 0
#         self.issue_time = 0
#         self.start_exec_time = 0
#         self.end_exec_time = 0
#         self.wb_time = 0

#         if inst:
#             self.obtain()

#     def obtain(self):
#         self.inst = self.inst.replace(",", "")
#         vec = self.inst.split()
#         self.op = vec[0]

#         if self.op in ["ADD", "NAND", "MUL"]:
#             self.rd = vec[1]
#             self.rs1 = vec[2]
#             self.rs2 = vec[3]
#         elif self.op == "ADDI":
#             self.rd = vec[1]
#             self.rs1 = vec[2]
#             self.imm = int(vec[3])
#         elif self.op == "LOAD":
#             tempvec = self.splitstring(vec[2], "(")
#             self.rd = vec[1]
#             self.offset = int(tempvec[0])
#             self.rs1 = tempvec[1][:-1]
#         elif self.op == "STORE":
#             tempvec = self.splitstring(vec[2], "(")
#             self.rs2 = vec[1]
#             self.offset = int(tempvec[0])
#             self.rs1 = tempvec[1][:-1]
#         elif self.op == "BEQ":
#             self.rs1 = vec[1]
#             self.rs2 = vec[2]
#             self.label = int(vec[3])
#         elif self.op == "CALL":
#             self.label = int(vec[1])
#         elif self.op == "RET":
#             return

#         self.cycles_left_in_execution = get_cycles(self.op)

#     def splitstring(self, string, delimiter):
#         return string.split(delimiter)

# def get_cycles(op):
#     cycle_dict = {
#         "LOAD": 6,
#         "STORE": 6,
#         "ADD": 2,
#         "NAND": 1,
#         "MUL": 8,
#         "BEQ": 1,
#         "CALL": 1,
#         "RET": 1
#     }
#     return cycle_dict.get(op, 1)

# class Tomasulo:
#     def __init__(self):
#         self.instructions = []
#         self.remaining_instructions = []
#         self.current_cycle = 0
#         self.pc = 0
#         self.total_write_backs = 0
#         self.branches = 0
#         self.mispredictions = 0
#         self.execution_flag = True

#     # def get_instructions(self):
#     #     self.instructions.append(Instruction("LOAD R2 1(R0)"))
#     #     self.instructions.append(Instruction("LOAD R3 2(R0)"))
#     #     self.instructions.append(Instruction("CALL 5"))
#     #     self.instructions.append(Instruction("ADD R4 R2 R3"))
#     #     self.instructions.append(Instruction("MUL R5 R2 R3"))
#     #     self.instructions.append(Instruction("NAND R6 R2 R3"))
#     #     self.instructions.append(Instruction("ADD R10 R4 R6"))
#     #     self.instructions.append(Instruction("ADD R11 R10 R3"))
#     #     self.instructions.append(Instruction("ADD R12 R4 R3"))
#     #     self.instructions.append(Instruction("ADDI R14 R14 100"))

#     #     for inst in self.instructions:
#     #         self.remaining_instructions.append(inst)

#     def is_finished(self):
#         if self.current_cycle == 0:
#             return False
#         for op, rs_list in reservation_stations.items():
#             for rs in rs_list:
#                 if rs.busy:
#                     return False
#         return True

#     def run(self):
#         while self.total_write_backs < len(self.instructions):
#             self.current_cycle += 1
#             self.write_back()
#             self.execute()
#             self.issue()
#             if self.is_finished():
#                 break
#         print_timing_table(self.instructions)
#         print_registers(registers)

#     def issue(self):
#         global reservation_stations, registers
#         if 0 <= self.pc < len(self.instructions):
#             inst = self.instructions[self.pc]
#             rs_list = reservation_stations["ADD"] if inst.op == "ADDI" else reservation_stations[inst.op]
#             for rs in rs_list:
#                 if not rs.busy:
#                     inst.issue_time = self.current_cycle
#                     rs.instruction = inst
#                     rs.busy = True
#                     rs.op = inst.op
#                     rs.cycles = get_cycles(inst.op)

#                     if inst.rs1:
#                         if registers[inst.rs1].busy:
#                             rs.qj = registers[inst.rs1].reorder
#                         else:
#                             rs.vj = registers[inst.rs1].value

#                     if inst.rs2:
#                         if registers[inst.rs2].busy:
#                             rs.qk = registers[inst.rs2].reorder
#                         else:
#                             rs.vk = registers[inst.rs2].value

#                     if inst.rd:
#                         registers[inst.rd].busy = True
#                         registers[inst.rd].reorder = rs.name
#                     self.pc += 1
#                     break

#     def execute(self):
#         if self.execution_flag:
#             for op, rs_list in reservation_stations.items():
#                 for rs in rs_list:
#                     if rs.busy and rs.qj is None and rs.qk is None:
#                         if rs.instruction.start_exec_time == 0:
#                             rs.instruction.start_exec_time = self.current_cycle
#                             if rs.instruction.op in ["BEQ", "RET", "CALL"]:
#                                 self.execution_flag = False
#                                 if rs.instruction.op == "BEQ":
#                                     registers["R0"].value = self.pc

#                         rs.cycles -= 1
#                         rs.instruction.cycles_left_in_execution -= 1
#                         if rs.cycles == 0:
#                             if rs.op == "LOAD":
#                                 rs.result = Memory[rs.instruction.offset + rs.vj]
#                             elif rs.op == "STORE":
#                                 Memory[rs.instruction.offset + rs.instruction.vj] = rs.instruction.vk
#                             elif rs.op == "BEQ":
#                                 self.branches += 1
#                                 self.execution_flag = True
#                                 if rs.vj == rs.vk:
#                                     self.pc = registers["R0"].value + rs.instruction.label
#                                     self.mispredictions += 1
#                             elif rs.op == "CALL":
#                                 registers["R1"].value = self.pc
#                                 self.pc = rs.instruction.label
#                                 self.execution_flag = True
#                             elif rs.op == "RET":
#                                 self.execution_flag = True
#                                 if registers["R1"].value != -1:
#                                     self.pc = registers["R1"].value
#                                     registers["R1"].value = -1
#                             elif rs.op == "ADD":
#                                 rs.result = rs.vj + rs.vk
#                             elif rs.op == "ADDI":
#                                 rs.result = rs.vj + rs.instruction.imm
#                             elif rs.op == "NAND":
#                                 rs.result = ~(rs.vj & rs.vk) & 0xFFFF
#                             elif rs.op == "MUL":
#                                 rs.result = (rs.vj * rs.vk) & 0xFFFF
#                             rs.instruction.end_exec_time = self.current_cycle
#                             rs.ready = True

#     def write_back(self):
#         station = None
#         value = None

#         for op, rs_list in reservation_stations.items():
#             for rs in rs_list:
#                 if rs.ready:
#                     rs.instruction.wb_time = self.current_cycle
#                     self.total_write_backs += 1
#                     station = rs.name
#                     value = rs.result
#                     rs.ready = False
#                     rs.busy = False

#                     for reg in registers.values():
#                         if reg.reorder == station:
#                             reg.value = value
#                             reg.busy = False
#                             reg.reorder = None

#         if station:
#             for op2, rs_list2 in reservation_stations.items():
#                 for rs in rs_list2:
#                     if rs.qj == station:
#                         rs.vj = value
#                         rs.qj = None
#                     if rs.qk == station:
#                         rs.vk = value
#                         rs.qk = None

# def print_registers(registers):
#     for reg in registers.values():
#         if reg.reorder is None:
#             reg.busy = False
#             reg.reorder = None
#     for reg in registers.keys():
#         reg_values[reg].set(f"{registers[reg].value}")
#         print(f"Register {reg} is currently: {registers[reg].busy}, Reorder: {registers[reg].reorder}, Value: {registers[reg].value}")

# def print_timing_table(instructions):
#     print(f"{'Inst':<10} {'Issue':<10} {'Start Execute':<15} {'End Execute':<15} {'WB':<10}")
#     for i, inst in enumerate(instructions):
#         print(f"{inst.inst:<10} {inst.issue_time:<10} {inst.start_exec_time:<15} {inst.end_exec_time:<15} {inst.wb_time:<10}")

# reservation_stations = {
#     'LOAD': [ReservationStation(f"LOAD{i}", 'LOAD') for i in range(2)],
#     'STORE': [ReservationStation(f"STORE{i}", 'STORE') for i in range(1)],
#     'ADD': [ReservationStation(f"ADD{i}", 'ADD') for i in range(4)],
#     'NAND': [ReservationStation(f"NAND{i}", 'NAND') for i in range(2)],
#     'MUL': [ReservationStation(f"MUL{i}", 'MUL') for i in range(1)],
#     'BEQ': [ReservationStation(f"BEQ{i}", 'BEQ') for i in range(1)],
#     'CALL': [ReservationStation(f"CALL{i}", 'CALL') for i in range(1)],
#     'RET': [ReservationStation(f"RET{i}", 'RET') for i in range(1)],
# }

# registers = {f"R{i}": Register() for i in range(8)}
# registers["R0"].value = 0

# Memory = [i * 10 for i in range(10)]

# instructions = []  # Initialize the instructions list globally

# tomasulo = Tomasulo()

# # Tkinter GUI
# def add_instruction():
#     op = op_var.get()
#     dest = dest_var.get()
#     src1 = src1_var.get()
#     src2 = src2_var.get()
#     instr_str = f"{op} {dest} {src1} {src2}"
#     instructions.append(Instruction(instr_str))
#     instruction_list.insert(tk.END, instr_str)
#     tree.insert('', END, values=(instr_str, "", "", ""))

# def load_instructions_from_file():
#     file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
#     if file_path:
#         with open(file_path, 'r') as file:
#             lines = file.readlines()
#             instructions.clear()
#             instruction_list.delete(0, tk.END)
#             tree.delete(*tree.get_children())
#             for line in lines:
#                 parts = line.strip().split()
#                 if len(parts) >= 2:
#                     op = parts[0]
#                     if op in ["LOAD", "STORE", "BEQ", "CALL", "RET", "ADD", "ADDI", "NAND", "MUL"]:
#                         instr_str = " ".join(parts)
#                         instructions.append(Instruction(instr_str))
#                         instruction_list.insert(tk.END, instr_str)
#                         tree.insert('', END, values=(instr_str, "", "", ""))

# def run_simulation():
#     tomasulo.instructions = instructions.copy()
#     tomasulo.run()
#     result_text.set(f"Total cycles: {tomasulo.current_cycle}")
#     for reg_name, reg in registers.items():
#         reg_values[reg_name].set(f"{reg.value}")
#     instruction_list.delete(0, tk.END)
#     tree.delete(*tree.get_children())
#     for inst in tomasulo.instructions:
#         tree.insert('', END, values=(inst.inst, inst.issue_time, inst.start_exec_time, inst.end_exec_time,  inst.wb_time))

# # Initialize GUI
# root = tk.Tk()
# root.title("Tomasulo's Algorithm Simulator")

# input_frame = ttk.LabelFrame(root, text="Add Instruction")
# input_frame.grid(row=0, column=0, padx=10, pady=10)

# ttk.Label(input_frame, text="Operation").grid(row=0, column=0)
# op_var = StringVar()
# ttk.Entry(input_frame, textvariable=op_var).grid(row=0, column=1)

# ttk.Label(input_frame, text="Dest").grid(row=1, column=0)
# dest_var = StringVar()
# ttk.Entry(input_frame, textvariable=dest_var).grid(row=1, column=1)

# ttk.Label(input_frame, text="Src1").grid(row=2, column=0)
# src1_var = StringVar()
# ttk.Entry(input_frame, textvariable=src1_var).grid(row=2, column=1)

# ttk.Label(input_frame, text="Src2").grid(row=3, column=0)
# src2_var = StringVar()
# ttk.Entry(input_frame, textvariable=src2_var).grid(row=3, column=1)

# ttk.Button(input_frame, text="Add Instruction", command=add_instruction).grid(row=4, column=0, columnspan=2, pady=5)
# ttk.Button(input_frame, text="Load Instructions", command=load_instructions_from_file).grid(row=5, column=0, columnspan=2, pady=5)

# instruction_list = Listbox(root, height=10)
# instruction_list.grid(row=1, column=0, padx=10, pady=10)

# result_frame = ttk.LabelFrame(root, text="Simulation Results")
# result_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

# result_text = StringVar()
# ttk.Label(result_frame, textvariable=result_text).grid(row=0, column=0, columnspan=2)

# reg_values = {f"R{i}": StringVar(value="0") for i in range(8)}

# for i in range(8):
#     ttk.Label(result_frame, text=f"R{i}").grid(row=i + 1, column=0)
#     ttk.Label(result_frame, textvariable=reg_values[f"R{i}"]).grid(row=i + 1, column=1)

# table_frame = ttk.LabelFrame(root, text="Cycle Table")
# table_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

# columns = ('instruction', 'issue', 'execute','done_execute', 'write_result')
# tree = ttk.Treeview(table_frame, columns=columns, show='headings')
# tree.heading('instruction', text='Instruction')
# tree.heading('issue', text='Issue')
# tree.heading('execute', text='Execute')
# tree.heading('done_execute', text='Done_Execute')
# tree.heading('write_result', text='Write Result')
# tree.grid(row=0, column=0)

# ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=2, column=0, columnspan=2, pady=10)

# root.mainloop()

import tkinter as tk
from tkinter import ttk, filedialog, StringVar, Listbox, END
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
        self.instruction = None
        self.ready = False

    def clean(self):
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.result = None
        self.cycles = 0
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

        if self.op in ["ADD", "NAND", "MUL"]:
            self.rd = vec[1]
            self.rs1 = vec[2]
            self.rs2 = vec[3]
        elif self.op == "ADDI":
            self.rd = vec[1]
            self.rs1 = vec[2]
            self.imm = int(vec[3])
        elif self.op == "LOAD":
            tempvec = self.splitstring(vec[2], "(")
            self.rd = vec[1]
            self.offset = int(tempvec[0])
            self.rs1 = tempvec[1][:-1]
        elif self.op == "STORE":
            tempvec = self.splitstring(vec[2], "(")
            self.rs2 = vec[1]
            self.offset = int(tempvec[0])
            self.rs1 = tempvec[1][:-1]
        elif self.op == "BEQ":
            self.rs1 = vec[1]
            self.rs2 = vec[2]
            self.label = int(vec[3])
        elif self.op == "CALL":
            self.label = int(vec[1])
        elif self.op == "RET":
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
        "RET": 1,
        "ADDI": 2
    }
    return cycle_dict.get(op, 1)

class Tomasulo:
    def __init__(self):
        self.instructions = []
        self.remaining_instructions = []
        self.current_cycle = 0
        self.pc = 0
        self.total_write_backs = 0
        self.branches = 0
        self.mispredictions = 0
        self.execution_flag = True

    def is_finished(self):
        if self.current_cycle == 0:
            return False
        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                if rs.busy:
                    return False
        return True

    def run(self):
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
            rs_list = reservation_stations["ADD"] if inst.op == "ADDI" else reservation_stations[inst.op]
            for rs in rs_list:
                if not rs.busy:
                    inst.issue_time = self.current_cycle
                    rs.instruction = inst
                    rs.busy = True
                    rs.op = inst.op
                    rs.cycles = get_cycles(inst.op)

                    if inst.rs1:
                        if registers[inst.rs1].busy:
                            rs.qj = registers[inst.rs1].reorder
                        else:
                            rs.vj = registers[inst.rs1].value

                    if inst.rs2:
                        if registers[inst.rs2].busy:
                            rs.qk = registers[inst.rs2].reorder
                        else:
                            rs.vk = registers[inst.rs2].value

                    if inst.rd:
                        registers[inst.rd].busy = True
                        registers[inst.rd].reorder = rs.name
                    self.pc += 1
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
                        if rs.cycles == 0:
                            if rs.op == "LOAD":
                                rs.result = Memory[rs.instruction.offset + rs.vj]
                            elif rs.op == "STORE":
                                Memory[rs.instruction.offset + rs.instruction.vj] = rs.instruction.vk
                            elif rs.op == "BEQ":
                                self.branches += 1
                                self.execution_flag = True
                                if rs.vj == rs.vk:
                                    self.pc = registers["R0"].value + rs.instruction.label
                                    self.mispredictions += 1
                            elif rs.op == "CALL":
                                registers["R1"].value = self.pc
                                self.pc = rs.instruction.label
                                self.execution_flag = True
                            elif rs.op == "RET":
                                self.execution_flag = True
                                if registers["R1"].value != -1:
                                    self.pc = registers["R1"].value
                                    registers["R1"].value = -1
                            elif rs.op == "ADD":
                                rs.result = rs.vj + rs.vk
                            elif rs.op == "ADDI":
                                rs.result = rs.vj + rs.instruction.imm
                            elif rs.op == "NAND":
                                rs.result = ~(rs.vj & rs.vk) & 0xFFFF
                            elif rs.op == "MUL":
                                rs.result = (rs.vj * rs.vk) & 0xFFFF
                            rs.instruction.end_exec_time = self.current_cycle
                            rs.ready = True

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
                    rs.busy = False

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
    for reg in registers.values():
        if reg.reorder is None:
            reg.busy = False
            reg.reorder = None
    for reg in registers.keys():
        reg_values[reg].set(f"{registers[reg].value}")
        print(f"Register {reg} is currently: {registers[reg].busy}, Reorder: {registers[reg].reorder}, Value: {registers[reg].value}")

def print_timing_table(instructions):
    print(f"{'Inst':<10} {'Issue':<10} {'Start Execute':<15} {'End Execute':<15} {'WB':<10}")
    for i, inst in enumerate(instructions):
        print(f"{inst.inst:<10} {inst.issue_time:<10} {inst.start_exec_time:<15} {inst.end_exec_time:<15} {inst.wb_time:<10}")

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

registers = {f"R{i}": Register() for i in range(8)}
registers["R0"].value = 0

Memory = [i * 10 for i in range(10)]

instructions = []  # Initialize the instructions list globally

tomasulo = Tomasulo()

# Tkinter GUI
def update_fields(*args):
    op = op_var.get()
    for widget in input_frame.winfo_children():
        widget.grid_forget()
    ttk.Label(input_frame, text="Operation").grid(row=0, column=0)
    op_menu.grid(row=0, column=1)
    ttk.Button(input_frame, text="Add Instruction", command=add_instruction).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(input_frame, text="Load Instructions", command=load_instructions_from_file).grid(row=5, column=0, columnspan=2, pady=5)
    if op in ["ADD", "NAND", "MUL"]:
        ttk.Label(input_frame, text="Dest (rd)").grid(row=1, column=0)
        dest_entry.grid(row=1, column=1)
        ttk.Label(input_frame, text="Src1 (rs1)").grid(row=2, column=0)
        src1_entry.grid(row=2, column=1)
        ttk.Label(input_frame, text="Src2 (rs2)").grid(row=3, column=0)
        src2_entry.grid(row=3, column=1)
    elif op == "ADDI":
        ttk.Label(input_frame, text="Dest (rd)").grid(row=1, column=0)
        dest_entry.grid(row=1, column=1)
        ttk.Label(input_frame, text="Src1 (rs1)").grid(row=2, column=0)
        src1_entry.grid(row=2, column=1)
        ttk.Label(input_frame, text="Immediate (imm)").grid(row=3, column=0)
        imm_entry.grid(row=3, column=1)
    elif op in ["LOAD", "STORE"]:
        ttk.Label(input_frame, text="Dest (rd)" if op == "LOAD" else "Src2 (rs2)").grid(row=1, column=0)
        dest_entry.grid(row=1, column=1)
        ttk.Label(input_frame, text="Offset").grid(row=2, column=0)
        offset_entry.grid(row=2, column=1)
        ttk.Label(input_frame, text="Src1 (rs1)").grid(row=3, column=0)
        src1_entry.grid(row=3, column=1)
    elif op == "BEQ":
        ttk.Label(input_frame, text="Src1 (rs1)").grid(row=1, column=0)
        src1_entry.grid(row=1, column=1)
        ttk.Label(input_frame, text="Src2 (rs2)").grid(row=2, column=0)
        src2_entry.grid(row=2, column=1)
        ttk.Label(input_frame, text="Label").grid(row=3, column=0)
        label_entry.grid(row=3, column=1)
    elif op == "CALL":
        ttk.Label(input_frame, text="Label").grid(row=1, column=0)
        label_entry.grid(row=1, column=1)

def add_instruction():
    op = op_var.get()
    dest = dest_var.get()
    src1 = src1_var.get()
    src2 = src2_var.get()
    imm = imm_var.get()
    offset = offset_var.get()
    label = label_var.get()

    if op in ["ADD", "NAND", "MUL"]:
        instr_str = f"{op} {dest} {src1} {src2}"
    elif op == "ADDI":
        instr_str = f"{op} {dest} {src1} {imm}"
    elif op in ["LOAD", "STORE"]:
        instr_str = f"{op} {dest if op == 'LOAD' else src2} {offset}({src1})"
    elif op == "BEQ":
        instr_str = f"{op} {src1} {src2} {label}"
    elif op == "CALL":
        instr_str = f"{op} {label}"
    elif op == "RET":
        instr_str = f"{op}"

    instructions.append(Instruction(instr_str))
    instruction_list.insert(tk.END, instr_str)
    tree.insert('', END, values=(instr_str, "", "", ""))

def load_instructions_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            instructions.clear()
            instruction_list.delete(0, tk.END)
            tree.delete(*tree.get_children())
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 2:
                    op = parts[0]
                    if op in ["LOAD", "STORE", "BEQ", "CALL", "RET", "ADD", "ADDI", "NAND", "MUL"]:
                        instr_str = " ".join(parts)
                        instructions.append(Instruction(instr_str))
                        instruction_list.insert(tk.END, instr_str)
                        tree.insert('', END, values=(instr_str, "", "", ""))

def run_simulation():
    tomasulo.instructions = instructions.copy()
    tomasulo.run()
    result_text.set(f"Total cycles: {tomasulo.current_cycle}")
    for reg_name, reg in registers.items():
        reg_values[reg_name].set(f"{reg.value}")
    instruction_list.delete(0, tk.END)
    tree.delete(*tree.get_children())
    for inst in tomasulo.instructions:
        tree.insert('', END, values=(inst.inst, inst.issue_time, inst.start_exec_time, inst.end_exec_time,  inst.wb_time))

def reset_simulation():
    # Clear instructions and UI elements
    instructions.clear()
    instruction_list.delete(0, tk.END)
    tree.delete(*tree.get_children())

    # Reset Tomasulo and cycle results
    tomasulo.instructions = []
    tomasulo.current_cycle = 0
    tomasulo.pc = 0
    tomasulo.total_write_backs = 0
    tomasulo.execution_flag = True
    result_text.set("")

    # Reset reservation stations
    for rs_list in reservation_stations.values():
        for rs in rs_list:
            rs.clean()

    # Reset registers
    for reg in registers.values():
        reg.value = 0
        reg.busy = False
        reg.reorder = None
        reg_values[f"R{reg}"].set("0")

    print_registers(registers)

# Initialize GUI
root = tk.Tk()
root.title("Tomasulo's Algorithm Simulator")

input_frame = ttk.LabelFrame(root, text="Add Instruction")
input_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(input_frame, text="Operation").grid(row=0, column=0)
op_var = StringVar()
op_var.trace('w', update_fields)
op_menu = ttk.Combobox(input_frame, textvariable=op_var)
op_menu['values'] = ["ADD", "NAND", "MUL", "ADDI", "LOAD", "STORE", "BEQ", "CALL", "RET"]
op_menu.grid(row=0, column=1)

dest_var = StringVar()
src1_var = StringVar()
src2_var = StringVar()
imm_var = StringVar()
offset_var = StringVar()
label_var = StringVar()

dest_entry = ttk.Entry(input_frame, textvariable=dest_var)
src1_entry = ttk.Entry(input_frame, textvariable=src1_var)
src2_entry = ttk.Entry(input_frame, textvariable=src2_var)
imm_entry = ttk.Entry(input_frame, textvariable=imm_var)
offset_entry = ttk.Entry(input_frame, textvariable=offset_var)
label_entry = ttk.Entry(input_frame, textvariable=label_var)

ttk.Button(input_frame, text="Add Instruction", command=add_instruction).grid(row=4, column=0, columnspan=2, pady=5)
ttk.Button(input_frame, text="Load Instructions", command=load_instructions_from_file).grid(row=5, column=0, columnspan=2, pady=5)

instruction_list = Listbox(root, height=10)
instruction_list.grid(row=1, column=0, padx=10, pady=10)

result_frame = ttk.LabelFrame(root, text="Simulation Results")
result_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

result_text = StringVar()
ttk.Label(result_frame, textvariable=result_text).grid(row=0, column=0, columnspan=2)

reg_values = {f"R{i}": StringVar(value="0") for i in range(8)}

for i in range(8):
    ttk.Label(result_frame, text=f"R{i}").grid(row=i + 1, column=0)
    ttk.Label(result_frame, textvariable=reg_values[f"R{i}"]).grid(row=i + 1, column=1)

table_frame = ttk.LabelFrame(root, text="Cycle Table")
table_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)

columns = ('instruction', 'issue', 'execute','done_execute', 'write_result')
tree = ttk.Treeview(table_frame, columns=columns, show='headings')
tree.heading('instruction', text='Instruction')
tree.heading('issue', text='Issue')
tree.heading('execute', text='Execute')
tree.heading('done_execute', text='Done_Execute')
tree.heading('write_result', text='Write Result')
tree.grid(row=0, column=0)

ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=2, column=0, columnspan=2, pady=10)
ttk.Button(root, text="Reset Simulation", command=reset_simulation).grid(row=2, column=2, pady=10)

root.mainloop()
