import re
import csv
import ast

# Input and output file paths
input_file = 'network_output.log'
output_file = 'cleaned_output.csv'

# Updated regex pattern to capture rate and c
line_pattern = re.compile(
    r"Step\s+(\d+).*?rate=([\d.]+).*?a=([\d.]+),\s+s=([\d.]+),\s+lo=\[([^\]]*)\].*?c=\[([\d.]+),\s*([\d.]+)\],\s+b=\[([\d.]+),\s*([\d.]+)\],\s+q=\[([\d.]+),\s*([\d.]+)\]"
)
tuple_pattern = re.compile(r"\((\d+),\s*([\d.]+)\)")

# Helper function to safely convert strings to floats
def safe_float(value):
    try:
        # Strip any trailing characters (like a dot or space) and convert to float
        return float(value.strip().replace('.', '', 1))
    except ValueError:
        return None

# Extract data
data = []
with open(input_file, 'r') as f:
    for line in f:
        line_match = line_pattern.search(line)
        if line_match:
            step = int(line_match.group(1))
            rate = safe_float(line_match.group(2))
            a = safe_float(line_match.group(3))
            s = safe_float(line_match.group(4))
            lo_raw = line_match.group(5)
            c_0 = safe_float(line_match.group(6))
            c_1 = safe_float(line_match.group(7))
            b_0 = safe_float(line_match.group(8))
            b_1 = safe_float(line_match.group(9))
            q_0 = safe_float(line_match.group(10))
            q_1 = safe_float(line_match.group(11))

            # Parse the lo list of tuples
            lo_matches = tuple_pattern.findall(lo_raw)
            lo = [(int(x), float(y)) for x, y in lo_matches]

            data.append([step, a, s, lo, rate, c_0, c_1, b_0, b_1, q_0, q_1])

# Write to CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['step', 'a', 's', 'lo', 'rate', 'c_0', 'c_1', 'b_0', 'b_1', 'q_0', 'q_1'])
    for row in data:
        # Convert `lo` list of tuples to a string (e.g. "[(0, 0.0), (1, 1.5)]")
        lo_str = str(row[3])
        writer.writerow([row[0], row[1], row[2], lo_str, row[4], row[5], row[6], row[7], row[8], row[9], row[10]])

print(f"CSV written to {output_file}")

