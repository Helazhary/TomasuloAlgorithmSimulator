Student Names and IDs:

Hussein Elazhary, ID: 900211733
Eslam Tawfik, ID: 900215295

Issues:

1. **GUI Responsiveness:** The GUI may become unresponsive during long simulations due to the single-threaded nature of Tkinter. Optimizations or threading may be required for better performance.
2. **Instruction Format Handling:** The current implementation assumes a strict format for instructions. Incorrect formatting may lead to unexpected behavior or errors.
3. **Error Handling:** Limited error handling is implemented. Invalid inputs or configurations may cause the program to crash or behave unpredictably.

4. Assumptions:

1. **Correct Instruction Format**: It is assumed that all instructions provided by the user are correctly formatted according to the expected syntax.
2.** Finite Loop** Execution: The loop in the test case is assumed to have a clear termination condition to prevent infinite loops.
3.** Memory Size**: The memory size is assumed to be sufficient for the given test cases and simulations.

   What Works:

**Dynamic Configuration:** Users can dynamically configure the number of reservation stations and cycles for each functional unit before starting the simulation.
**Instruction Addition and Loading:** Users can add individual instructions through the GUI or load a set of instructions from a file.
**Cycle-by-Cycle Simulation:** The simulation correctly executes instructions cycle-by-cycle, updating issue, execute, and write-back times.
**Branch Handling:** The simulation correctly handles branch instructions (BEQ) to control the flow of the program.
**Loop Execution**: The loop in the test case executes as expected, demonstrating dynamic instruction scheduling and out-of-order execution.
**Program Results statistics:** Displaying IPC, Branching, and Branch Mispredictions accurately post run.


README.txt
Student Names and IDs:

James, ID: 1123
Arthur, ID: 4353
Release Notes:

Version 1.0

Date: 2024-05-19

Issues:

GUI Responsiveness: The GUI may become unresponsive during long simulations due to the single-threaded nature of Tkinter. Optimizations or threading may be required for better performance.
Instruction Format Handling: The current implementation assumes a strict format for instructions. Incorrect formatting may lead to unexpected behavior or errors.
Error Handling: Limited error handling is implemented. Invalid inputs or configurations may cause the program to crash or behave unpredictably.
Assumptions:

Correct Instruction Format: It is assumed that all instructions provided by the user are correctly formatted according to the expected syntax.
Finite Loop Execution: The loop in the test case is assumed to have a clear termination condition to prevent infinite loops.
Memory Size: The memory size is assumed to be sufficient for the given test cases and simulations.
What Works:

Dynamic Configuration: Users can dynamically configure the number of reservation stations and cycles for each functional unit before starting the simulation.
Instruction Addition and Loading: Users can add individual instructions through the GUI or load a set of instructions from a file.
Cycle-by-Cycle Simulation: The simulation correctly executes instructions cycle-by-cycle, updating issue, execute, and write-back times.
Branch Handling: The simulation correctly handles branch instructions (BEQ) to control the flow of the program.
Loop Execution: The loop in the test case executes as expected, demonstrating dynamic instruction scheduling and out-of-order execution.

What Does Not Work:

**Advanced Error Handling:** The current implementation lacks comprehensive error handling and may not gracefully handle invalid inputs or configurations.


