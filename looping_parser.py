import re
import csv
import os
import ast

# Directory where the log files are located
input_directory = 'logs_directory'  # Replace with your directory path
output_file = 'cleaned_output.csv'

# Regex pattern to capture rate, a, s, lo, c, b, q
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

# Helper function to parse the 'lo' string
def parse_lo(lo_str):
    try:
        lo_list = ast.literal_eval(lo_str)
        return [tup[1] for tup in lo_list]  # Extract the second element of each tuple
    except Exception as e:
        print(f"Error parsing lo: {e}")
        return []

# Initialize an empty list to collect all data
all_data = []

# Loop through all files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.log'):  # Process only .log files
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r') as f:
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

                    # Add the data for this line to the list
                    all_data.append([step, a, s, lo, rate, c_0, c_1, b_0, b_1, q_0, q_1])

# Write all collected data to the CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['step', 'a', 's', 'lo', 'rate', 'c_0', 'c_1', 'b_0', 'b_1', 'q_0', 'q_1'])
    for row in all_data:
        # Convert `lo` list of tuples to a string (e.g. "[(0, 0.0), (1, 1.5)]")
        lo_str = str(row[3])
        writer.writerow([row[0], row[1], row[2], lo_str, row[4], row[5], row[6], row[7], row[8], row[9], row[10]])

print(f"All files processed and cleaned data written to {output_file}")

