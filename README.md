# Polymorphic MTNCL Gate Generator

A tool for generating valid combinations of Multi-Threshold Null Convention Logic (MTNCL) gates that can operate polymorphically at different voltage levels.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Polymorphic-MTNCL-Gen.git
cd Polymorphic-MTNCL-Gen
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## What is MTNCL?

Multi-Threshold Null Convention Logic (MTNCL) is a design methodology for building quasi-delay insensitive (QDI) asynchronous circuits. Key features:
- Power-efficient design through built-in power-gating (SLEEP port)
- Delay-insensitive operation
- Based on threshold gates with multiple input combinations

### Gate Naming Convention

MTNCL gates follow a "THmn" naming pattern where:
- TH = Threshold Gate
- m = Threshold value (minimum number of inputs that must be HIGH)
- n = Total number of inputs
- Optional 'w' suffix indicates weighted inputs

For example:
- TH12: 2-input OR gate (threshold=1, inputs=2)
- TH22: 2-input AND gate (threshold=2, inputs=2) 
- TH23: 3-input gate that requires any 2 inputs to be HIGH

### Standard Port Convention

All MTNCL gates use these standard port names:
```
Inputs:  a, b, c, d (as needed)
Output:  z
Control: s (SLEEP signal)
```

## What are Polymorphic MTNCL Gates?

Polymorphic MTNCL gates are special combinations that implement two different logic functions depending on the operating voltage:

- HVDD (High VDD) function: Active at nominal voltage
- LVDD (Low VDD) function: Active at reduced voltage (~50% of HVDD)

For example, in a 1.2V process:
- HVDD = 1.2V: Gate performs first logic function
- LVDD = 0.6V: Gate performs second logic function

### Combination Requirements

When creating polymorphic gate combinations:

1. Both gates must have the same number of inputs
2. Function compatibility depends on your Process Design Kit (PDK):
   - Some PDKs require HVDD function to be a subset of LVDD function
   - Others require LVDD function to be a subset of HVDD function

## Available Standard Gates

Below is the complete list of standard MTNCL gates available for polymorphic combinations:

| Gate Name | Boolean Function |
|-----------|-----------------|
| TH12      | A + B          |
| TH22      | AB             |
| TH13      | A + B + C      |
| TH23      | AB + AC + BC   |
| TH33      | ABC            |
| TH23w2    | A + BC         |
| TH33w2    | AB + AC        |
| TH14      | A + B + C + D  |
| TH24      | AB + AC + AD + BC + BD + CD |
| TH34      | ABC + ABD + ACD + BCD |
| TH44      | ABCD           |
| TH24w2    | A + BC + BD + CD |
| TH34w2    | AB + AC + AD + BCD |
| TH44w2    | ABC + ABD + ACD |
| TH34w3    | A + BCD        |
| TH44w3    | AB + AC + AD   |
| TH24w22   | A + B + CD     |
| TH34w22   | AB + AC + AD + BC + BD |
| TH44w22   | ABC + ABD + ACD + BC |
| TH54w22   | ABC + ABD      |
| TH34w32   | A + B + CD     |
| TH54w32   | AB + ACD + BCD |
| TH44w322  | AB + AC + AD + BC |
| TH54w322  | ABC + ABD + CD |
| THxor0    | AB + CD        |
| THand0    | AB + BC + AD   |
| TH24comp  | AC + BC + AD + BD |

## Identified Polymorphic MTNCL Gates

The following polymorphic gate combinations were identified in "Design of Asynchronous Polymorphic Logic Gates for Hardware Security":

| Gate Name       | HVDD Function               | LVDD Function               |
|-----------------|-----------------------------|-----------------------------|
| TH12-TH22       | A + B                       | AB                          |
| TH23w2-TH23     | A + BC                      | AB + AC + BC                |
| TH24-TH24Comp0  | AB + AC + AD + BC + BD + CD | AC + BC + AD + BD           |
| TH24w2-TH24     | A + BC + BD + CD            | AB + AC + AD + BC + BD + CD |
| TH34-TH44       | ABC + ABD + ACD + BCD       | ABCD                        |
| TH33w2-TH33     | AB + AC                     | ABC                         |
| TH13-TH33       | A + B + C                   | ABC                         |
| TH24w22-TH24w2  | A + B + CD                  | A + BC + BD + CD            |
| TH34w22-TH34w2  | AB + AC + AD + BC + BD      | AB + AC + AD + BCD          |
| TH34w32-TH34w22 | A + BC + BD                 | AB + AC + AD + BC + BD      |
| TH24w2-TH24comp | A + BC + BD + CD            | AC + BC + AD + BD           |
| TH24w22-TH24    | A + B + CD                  | AB + AC + AD + BC + BD + CD | 

## Usage Examples

### Example 1: Basic Gate Combination

```python
# Example code for generating a valid polymorphic gate combination
from poly_mtncl_gen import generate_combinations

# Generate all valid combinations with 2 inputs
combinations = generate_combinations(num_inputs=2)
for combination in combinations:
    print(combination)
```

Expected output:
```
PolymorphicGateCombination(
    HVDD: TH22 (A & B),
    LVDD: TH12 (A | B)
)
```

### Example 2: Checking Compatibility

```python
# Example code for checking if two gates are compatible
from poly_mtncl_gen import check_compatibility

gate1 = "TH22"  # AB
gate2 = "TH12"  # A + B

is_compatible = check_compatibility(gate1, gate2, subset_type="hvdd_subset")
print(f"Gates {gate1} and {gate2} are compatible: {is_compatible}")
```

### Example 3: Generating Truth Tables

```python
from poly_mtncl_gen import generate_combinations

# Generate combinations and show truth tables
combinations = generate_combinations(num_inputs=2)
for combination in combinations:
    print(combination)
    print("Truth Table:")
    print(combination.generate_truth_table())
    print()
```

Expected output:
```
PolymorphicGateCombination(
    HVDD: TH22 (A & B),
    LVDD: TH12 (A | B)
)
Truth Table:
+---+---+--------+--------+
| a | b | TH22   | TH12   |
+===+===+========+========+
| 0 | 0 | 0      | 0      |
+---+---+--------+--------+
| 0 | 1 | 0      | 1      |
+---+---+--------+--------+
| 1 | 0 | 0      | 1      |
+---+---+--------+--------+
| 1 | 1 | 1      | 1      |
+---+---+--------+--------+
```

### Example 4: Using Different Settings

```python
from poly_mtncl_gen import generate_combinations

# Generate combinations with specific settings
combinations = generate_combinations(
    num_inputs=4,      # Number of inputs (2-4)
    subset_type="lvdd_subset"  # or "hvdd_subset"
)
```

### Example 5: Saving Combinations to CSV

```python
from poly_mtncl_gen import generate_combinations, write_combinations_to_csv

# Generate combinations
combinations = generate_combinations(num_inputs=2)

# Save to CSV with auto-generated filename (includes timestamp)
csv_file = write_combinations_to_csv(combinations)
print(f"Combinations saved to: {csv_file}")

# Or specify your own filename
csv_file = write_combinations_to_csv(combinations, filename="my_combinations.csv")
```

The CSV file will contain the following columns:
- HVDD Gate
- HVDD Function
- LVDD Gate
- LVDD Function

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Contact

[Add your contact information here]