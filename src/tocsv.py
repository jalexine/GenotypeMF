import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as file:
    data = [line.strip().split(' ') for line in file.readlines()]

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print(f"Converted {input_file} to {output_file}.")
