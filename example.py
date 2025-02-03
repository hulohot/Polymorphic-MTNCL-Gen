# Import the poly_mtncl_gen module
import poly_mtncl_gen as pmtg


def print_two_input_combinations(subset_type):
    return pmtg.generate_combinations(num_inputs=2, subset_type=subset_type)

def print_three_input_combinations(subset_type):
    return pmtg.generate_combinations(num_inputs=3, subset_type=subset_type)

def print_four_input_combinations(subset_type):
    return pmtg.generate_combinations(num_inputs=4, subset_type=subset_type)

if __name__ == "__main__":

    # HVDD Subset means HVDD Gate is a subset of LVDD Gate
    # subset_type = "hvdd_subset"
    # LVDD Subset means LVDD Gate is a subset of HVDD Gate
    subset_type = "lvdd_subset"


    gates = []
    gates.extend(print_two_input_combinations(subset_type))
    gates.extend(print_three_input_combinations(subset_type))
    gates.extend(print_four_input_combinations(subset_type))

    print(f"Number of Combinations: {len(gates)}")

    for gate in gates:
        print(gate)
        # print(gate.generate_truth_table())

    # Save the gates to a file
    csv_file = pmtg.write_combinations_to_csv(gates, filename="polymorphic_gates_all.csv")
    print(f"\nCombinations saved to: {csv_file}")