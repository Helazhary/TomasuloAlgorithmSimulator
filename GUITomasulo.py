import tkinter as tk
from tkinter import ttk

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

class Register:
    def __init__(self):
        self.value = 0
        self.busy = False
        self.reorder = None

class Instruction:
    def __init__(self, op, dest, src1, src2):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

class CommonDataBus:
    def __init__(self):
        self.value = None
        self.station = None

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
    return cycle_dict[op]

def issue_instruction(instruction):
    rs_list = reservation_stations[instruction.op]
    for rs in rs_list:
        if not rs.busy:
            rs.busy = True
            rs.op = instruction.op
            rs.cycles = get_cycles(instruction.op)
            if registers[instruction.src1].busy:
                rs.qj = registers[instruction.src1].reorder
            else:
                rs.vj = registers[instruction.src1].value

            if registers[instruction.src2].busy:
                rs.qk = registers[instruction.src2].reorder
            else:
                rs.vk = registers[instruction.src2].value

            registers[instruction.dest].busy = True
            registers[instruction.dest].reorder = rs.name
            break

def execute():
    for op, rs_list in reservation_stations.items():
        for rs in rs_list:
            if rs.busy and rs.qj is None and rs.qk is None and rs.cycles > 0:
                rs.cycles -= 1
                if rs.cycles == 0:
                    if rs.op == "ADD":
                        rs.result = rs.vj + rs.vk
                    elif rs.op == "NAND":
                        rs.result = ~(rs.vj & rs.vk) & 0xFFFF  # Ensure 16-bit result
                    elif rs.op == "MUL":
                        rs.result = (rs.vj * rs.vk) & 0xFFFF  # Ensure 16-bit result
                    # Add more operations as needed
                    cdb.value = rs.result
                    cdb.station = rs.name
                    rs.busy = False

def write_result():
    if cdb.value is not None:
        for reg in registers.values():
            if reg.reorder == cdb.station:
                reg.value = cdb.value
                reg.busy = False
                reg.reorder = None

        for op, rs_list in reservation_stations.items():
            for rs in rs_list:
                if rs.qj == cdb.station:
                    rs.vj = cdb.value
                    rs.qj = None
                if rs.qk == cdb.station:
                    rs.vk = cdb.value
                    rs.qk = None
        cdb.value = None  # Reset CDB after broadcasting

def run_simulation():
    global instructions
    # Reset the simulator
    for rs_list in reservation_stations.values():
        for rs in rs_list:
            rs.busy = False
            rs.op = None
            rs.vj = None
            rs.vk = None
            rs.qj = None
            rs.qk = None
            rs.result = None
            rs.cycles = 0
    for reg in registers.values():
        reg.busy = False
        reg.reorder = None
        reg.value = 0


    # Initialize Common Data Bus
    cdb.value = None
    cdb.station = None

    # Simulation loop
    cycle = 0
    while instructions or any(rs.busy for rs_list in reservation_stations.values() for rs in rs_list):
        cycle += 1
        if instructions:
            instr = instructions.pop(0)
            issue_instruction(instr)
        execute()
        write_result()

    result_text.set(f"Total cycles: {cycle}")
    for reg_name, reg in registers.items():
        reg_values[reg_name].set(f"{reg.value}")

def add_instruction():
    op = op_var.get()
    dest = dest_var.get()
    src1 = src1_var.get()
    src2 = src2_var.get()
    instructions.append(Instruction(op, dest, src1, src2))
    instruction_list.insert(tk.END, f"{op} {dest} {src1} {src2}")

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


# Initialize instruction queue (example instructions)
instructions = [
     Instruction("ADD", "R1", "R2", "R3"),
    Instruction("NAND", "R4", "R1", "R2"),
    Instruction("MUL", "R5", "R2", "R3")
    ]

# Initialize Common Data Bus
cdb = CommonDataBus()

# Create the main window
root = tk.Tk()
root.title("Tomasulo's Algorithm Simulator")

# Create a frame for the instruction input
input_frame = ttk.LabelFrame(root, text="Add Instruction")
input_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(input_frame, text="Operation").grid(row=0, column=0)
op_var = tk.StringVar()
ttk.Entry(input_frame, textvariable=op_var).grid(row=0, column=1)

ttk.Label(input_frame, text="Dest").grid(row=1, column=0)
dest_var = tk.StringVar()
ttk.Entry(input_frame, textvariable=dest_var).grid(row=1, column=1)

ttk.Label(input_frame, text="Src1").grid(row=2, column=0)
src1_var = tk.StringVar()
ttk.Entry(input_frame, textvariable=src1_var).grid(row=2, column=1)

ttk.Label(input_frame, text="Src2").grid(row=3, column=0)
src2_var = tk.StringVar()
ttk.Entry(input_frame, textvariable=src2_var).grid(row=3, column=1)

ttk.Button(input_frame, text="Add Instruction", command=add_instruction).grid(row=4, column=0, columnspan=2, pady=5)

# Create a listbox to display instructions
instruction_list = tk.Listbox(root, height=10)
instruction_list.grid(row=1, column=0, padx=10, pady=10)

# Create a frame for the results
result_frame = ttk.LabelFrame(root, text="Simulation Results")
result_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

result_text = tk.StringVar()
ttk.Label(result_frame, textvariable=result_text).grid(row=0, column=0, columnspan=2)

reg_values = {f"R{i}": tk.StringVar(value="0") for i in range(8)}

for i in range(8):
    ttk.Label(result_frame, text=f"R{i}").grid(row=i+1, column=0)
    ttk.Label(result_frame, textvariable=reg_values[f"R{i}"]).grid(row=i+1, column=1)

# Create a button to run the simulation
ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
