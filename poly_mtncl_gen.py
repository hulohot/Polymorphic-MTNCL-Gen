# poly_mtncl_gen.py

from sympy import symbols, Or, And, Not, simplify_logic, sympify
from itertools import product
from tabulate import tabulate
import csv
from datetime import datetime

# Define the available gates and their boolean functions
GATES = {
    "TH12": "A | B",
    "TH22": "A & B",
    "TH13": "A | B | C",
    "TH23": "(A & B) | (A & C) | (B & C)",
    "TH33": "A & B & C",
    "TH23w2": "A | (B & C)",
    "TH33w2": "(A & B) | (A & C)",
    "TH14": "A | B | C | D",
    "TH24": "(A & B) | (A & C) | (A & D) | (B & C) | (B & D) | (C & D)",
    "TH34": "(A & B & C) | (A & B & D) | (A & C & D) | (B & C & D)",
    "TH44": "A & B & C & D",
    "TH24w2": "A | (B & C) | (B & D) | (C & D)",
    "TH34w2": "(A & B) | (A & C) | (A & D) | (B & C & D)",
    "TH44w2": "(A & B & C) | (A & B & D) | (A & C & D)",
    "TH34w3": "A | (B & C & D)",
    "TH44w3": "(A & B) | (A & C) | (A & D)",
    "TH24w22": "A | B | (C & D)",
    "TH34w22": "(A & B) | (A & C) | (A & D) | (B & C) | (B & D)",
    "TH44w22": "(A & B & C) | (A & B & D) | (A & C & D) | (B & C)",
    "TH54w22": "A & B & C | A & B & D",
    "TH34w32": "A | B | (C & D)",
    "TH54w32": "A & B | A & C & D | B & C & D",
    "TH44w322": "A & B | A & C | A & D | B & C",
    "TH54w322": "A & B & C | A & B & D | C & D",
    "THxor0": "A & B | C & D",
    "THand0": "A & B | B & C | A & D",
    "TH24comp": "A & C | B & C | A & D | B & D"
}

class PolymorphicGateCombination:
    def __init__(self, hvdd_gate, lvdd_gate):
        self.hvdd_gate = hvdd_gate
        self.lvdd_gate = lvdd_gate
        self.hvdd_function = GATES[hvdd_gate]
        self.lvdd_function = GATES[lvdd_gate]

    def __repr__(self):
        return (f"\n{self.hvdd_gate}_{self.lvdd_gate}\nPolymorphicGateCombination(\n\tHVDD: {self.hvdd_gate} ({self.hvdd_function}),\n"
                f"\tLVDD: {self.lvdd_gate} ({self.lvdd_function})\n)")

    def generate_truth_table(self):
        # Define symbols for inputs
        a, b, c, d = symbols('a b c d')
        input_symbols = [a, b, c, d]

        # Parse the boolean functions
        hvdd_expr = sympify(self.hvdd_function.replace('A', 'a').replace('B', 'b').replace('C', 'c').replace('D', 'd'))
        lvdd_expr = sympify(self.lvdd_function.replace('A', 'a').replace('B', 'b').replace('C', 'c').replace('D', 'd'))

        # Determine the number of inputs based on the gate name (e.g., TH22 has 2 inputs)
        if self.hvdd_gate in ["THxor0", "THand0", "TH24comp"]:
            num_inputs = 4
        else:
            num_inputs = int(self.hvdd_gate[3])  # Get number from THmn naming convention

        # Generate all possible input combinations
        input_combinations = list(product([0, 1], repeat=num_inputs))

        # Generate the truth table
        headers = ['a', 'b', 'c', 'd'][:num_inputs] + [self.hvdd_gate, self.lvdd_gate]
        table = []
        for inputs in input_combinations:
            input_dict = {symbol: value for symbol, value in zip(input_symbols[:num_inputs], inputs)}
            hvdd_result = int(bool(hvdd_expr.subs(input_dict)))
            lvdd_result = int(bool(lvdd_expr.subs(input_dict)))
            table.append(inputs + (hvdd_result, lvdd_result))

        return tabulate(table, headers=headers, tablefmt="grid")

def generate_combinations(num_inputs, subset_type="hvdd_subset"):
    """
    Generate all valid polymorphic gate combinations with the specified number of inputs.
    """
    valid_gates = []
    for gate in GATES:
        # Handle special gates (all 4-input gates)
        if gate in ["THxor0", "THand0", "TH24comp"]:
            if num_inputs == 4:
                valid_gates.append(gate)
        # Handle standard THmn gates
        elif int(gate[3]) == num_inputs:
            valid_gates.append(gate)
    
    combinations = []
    for hvdd_gate in valid_gates:
        for lvdd_gate in valid_gates:
            if hvdd_gate != lvdd_gate and check_compatibility(hvdd_gate, lvdd_gate, subset_type=subset_type):
                combinations.append(PolymorphicGateCombination(hvdd_gate, lvdd_gate))
    
    return combinations

def check_compatibility(gate1, gate2, subset_type="hvdd_subset"):
    """
    Check if two gates are compatible based on the PDK type.
    """
    # Define symbols for inputs
    a, b, c, d = symbols('a b c d')

    # Parse the boolean functions
    hvdd_expr = sympify(GATES[gate1].replace('A', 'a').replace('B', 'b').replace('C', 'c').replace('D', 'd'))
    lvdd_expr = sympify(GATES[gate2].replace('A', 'a').replace('B', 'b').replace('C', 'c').replace('D', 'd'))

    # Check if the LVDD function is a subset of the HVDD function
    if subset_type == "hvdd_subset":
        return simplify_logic(Or(Not(hvdd_expr), lvdd_expr)) == True
    elif subset_type == "lvdd_subset":
        return simplify_logic(Or(Not(lvdd_expr), hvdd_expr)) == True
    else:
        return False

def write_combinations_to_csv(combinations, filename=None):
    """
    Write a list of PolymorphicGateCombination objects to a CSV file.
    If no filename is provided, generates one with timestamp.
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"polymorphic_gates_{timestamp}.csv"

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Polymorphic Gate Combination', 'HVDD Gate', 'HVDD Function', 'LVDD Gate', 'LVDD Function'])
        
        # Write each combination
        for combo in combinations:
            writer.writerow([
                f"{combo.hvdd_gate}_{combo.lvdd_gate}",
                combo.hvdd_gate,
                combo.hvdd_function,
                combo.lvdd_gate,
                combo.lvdd_function
            ])

    return filename

# Example usage
if __name__ == "__main__":

    ### EDIT THESE SETTINGS ###

    SHOW_TRUTH_TABLES = False
    # SHOW_TRUTH_TABLES = True
    NUM_INPUTS = 2
    SUBSET_TYPE = "hvdd_subset"
    # SUBSET_TYPE = "lvdd_subset"
    SAVE_TO_CSV = True
    # SAVE_TO_CSV = False

    ### END OF EDITABLE SETTINGS ###

    # Generate all valid combinations
    combinations = generate_combinations(num_inputs=NUM_INPUTS, subset_type=SUBSET_TYPE)
    
    # Print combinations
    for combination in combinations:
        print(combination)
        if SHOW_TRUTH_TABLES:
            print("Truth Table:")
            print(combination.generate_truth_table())
            print()
    
    # Save to CSV if enabled
    if SAVE_TO_CSV:
        csv_file = write_combinations_to_csv(combinations)
        print(f"\nCombinations saved to: {csv_file}")
