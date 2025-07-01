import numpy as np
import matplotlib.pyplot as plt
import sys

if len(sys.argv) != 3:
    print("\033[95mUsage: python coverage.py <input_filename> <output_filename>\033[0m")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Load the coverage results
coverage_list = np.loadtxt(input_filename)

# Plot the coverage
plt.figure(figsize=(10, 5))
plt.plot(range(1, len(coverage_list) + 1), coverage_list, marker='.', color='pink', linestyle='-', label='GreConD')
plt.xlabel('Number of Factors')
plt.ylabel('Coverage')
plt.title('Coverage vs Number of Factors')
plt.legend()
plt.grid(True)
plt.savefig(output_filename)

plt.show()
