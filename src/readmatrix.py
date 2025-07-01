import numpy as np
import sys

def read_input_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    header = lines[0].strip().split()
    matrix_data = []
    for line in lines[1:]:
        matrix_data.append([int(x) for x in line.strip().split()])
    I = np.array(matrix_data, dtype=bool)
    return I, header

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\033[95m♡ pls use : python readmatrix.py <input_filename> <output_filename> \033[0m")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    I, header = read_input_file(input_filename)

    # Save the matrix and header to a numpy file
    np.savez(output_filename, matrix=I, header=header)

