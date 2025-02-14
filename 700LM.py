import os
import re
import math
#
def find_first_available_number(directory):
    files = os.listdir(directory)
    numbers = [int(filename.split('.')[0]) for filename in files if filename.split('.')[0].isdigit()]
    numbers = [num for num in numbers if num > 1000]
    if not numbers:
        return 1001 
    first_available_number = next((num for num in range(1001, max(numbers) + 2) if num not in numbers), None)
    return first_available_number

def find_largest_coordinates(content):
    x_values = re.findall(r'X(-?\d+\.?\d*)', content)  # Finner alle X-verdier
    z_values = re.findall(r'Z(-?\d+\.?\d*)', content)  # Finner alle Z-verdier

    # Fjern X191016 fra listen over X-verdier
    x_values = [x for x in x_values if x != "191016"]

    if x_values:
        largest_x = max(float(x) for x in x_values)  # Finn største X-verdi
    else:
        largest_x = 0.0

    if z_values:
        largest_z = max(abs(float(z)) for z in z_values)  # Finn største Z-verdi (tar absoluttverdien)
    else:
        largest_z = 0.0

    rounded_x = math.ceil(largest_x)  # Runder opp X
    rounded_z = math.ceil(largest_z)  # Runder opp absoluttverdien av Z

    return rounded_x, rounded_z


def find_tool_ranges(content):
    lines = content.splitlines()
    tool_ranges = []
    current_tool_start = None

    # Finn søkeområder (fra T-kode til G28 U0.)
    for i, line in enumerate(lines):
        if re.search(r'(?<!\()\bT\d{4}\b(?!\))', line):  # Finn T-kode utenfor parenteser
            current_tool_start = i
        elif 'G28 U0.' in line and current_tool_start is not None:
            # Lagre start- og sluttindeks for området
            tool_ranges.append((current_tool_start, i))
            current_tool_start = None

    return tool_ranges


def insert_comment_before_operation(content, tool_ranges):
    lines = content.splitlines()
    new_lines = []

    last_insert_index = 0  # To keep track of where we left off in new_lines

    for start, end in tool_ranges:
        x_max, x_min = float('-inf'), float('inf')
        z_max, z_min = float('-inf'), float('inf')

        # Calculate max and min for X and Z within the tool range
        for i in range(start, end + 1):
            line = lines[i]
            x_match = re.search(r'X([-\d.]+)', line)
            z_match = re.search(r'Z([-\d.]+)', line)

            if x_match:
                x_value = float(x_match.group(1))
                x_max, x_min = max(x_max, x_value), min(x_min, x_value)

            if z_match:
                z_value = float(z_match.group(1))
                z_max, z_min = max(z_max, z_value), min(z_min, z_value)

        # Form the comment with the calculated extreme values
        comment = f"(X: MAX = {x_max}, MIN = {x_min})\n(Z: MAX = {z_max}, MIN = {z_min})"
        
        # Insert the comment directly before the operation, 4 lines above
        insertion_point = max(0, start - 3)
        new_lines.extend(lines[last_insert_index:insertion_point])  # Add lines up to insertion point
        new_lines.append(comment)  # Insert the comment at the calculated position
        new_lines.extend(lines[insertion_point:start])  # Add lines from start of the range

        # Add the lines from start to end (the tool operation itself)
        new_lines.extend(lines[start:end + 1])
        last_insert_index = end + 1  # Update the last processed line index

    # Add any remaining lines after the last range
    new_lines.extend(lines[last_insert_index:])
    
    # Rejoin all lines into the updated content
    new_content = '\n'.join(new_lines)
    
    return new_content





def modify_file(filename, new_heading):
    with open(filename, 'r') as file:
        content = file.read()

    # Endringer for fresing
    blocks = content.split('\n\n')  
    for i, block in enumerate(blocks):
        if 'P12' in block:
            block = block.replace('M03', 'M33')
            block = block.replace('M05', 'M35')      
            blocks[i] = block
    content = '\n\n'.join(blocks)



   # Finn strengen "G00 G28 U0. V0." og legg til "GOO G30 P3 W0." under den
    #content = re.sub(r'(G00 G28 U0\. V0\.)\n', r'\1\nG00 G30 P3 W0.\n', content)
    content = re.sub(r'\bP11\b', '', content)
    content = re.sub(r'\bP12\b', '', content)
    content = re.sub(r'\bM34\n', '', content)
    content = re.sub(r'\bG17\n', '', content)
    content = re.sub(r'Y0\.', '', content)
    content = re.sub(r'\bM278 \(CHAMFERING OFF\)\n', '', content)
    content = re.sub(r'\bM277 \(CHAMFERING ON\)\n', '', content)  
    content = re.sub(r'M289 \(SELECT C1 CLAMP CONTROL\)\n', '', content)
    content = re.sub(r'M289 \(SELECT C1 CLAMP CONTROL\)\n', '', content)
    content = re.sub(r'M24 \(START CHIP CONVEYOR\)\n', '', content) 
    content = re.sub(r'M25 \(STOP CHIP CONVEYOR\)\n', '', content)
    content = re.sub(r'G00 G28 U0\. V0\.', 'G28 U0.', content)
    content = re.sub(r'G28 U0\. V0\.', 'G28 U0.', content)

    # Changes
    list1 = ("T0100", "T0200", "T0300", "T0400", "T0500", "T0600", "T0700", "T0800", "T0900", "T1000", "T1100", "T1200", 
            "T1300", "T1400", "T1500", "T1600", "T1700", "T1800", "T1900", "T2000", "T2100", "T2200", "T2300", "T2400")

    first_replacement = True  # Flag to check if it's the first replacement
    for item in list1:
        if first_replacement:
            content = content.replace(item, "G65 P9029 A50. B1.")
            first_replacement = False  # After the first replacement, set flag to False
        else:
            content = content.replace(item, "G65 P9029 A50. B0.")

    # Finn største X- og Z-verdi
    rounded_x, rounded_z = find_largest_coordinates(content)

    # Legg til "G1901 D[rounded_x] K2. L[rounded_z] E2." etter linjen "G40 G80 G99"
    content = re.sub(r'(G40 G80 G99)', rf'\1\nG1901 D{rounded_x}. K2. L{rounded_z + 10}. E2.\nM42\n', content)    
    
       # Hent søkeområdene
    tool_ranges = find_tool_ranges(content)
    content = insert_comment_before_operation(content, tool_ranges)  # Bruk den forenklede funksjonen

    # Erstatter de første seks linjene annet
    lines = content.split('\n')
    lines[:6] = ["%", f"O{new_heading} ()", ""]
    content = '\n'.join(lines)
    # Lagrer endringene
    with open(filename, 'w') as file:
        file.write(content)


    # Lagrer endringene
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))


if __name__ == "__main__":
    filename = r'fil.md'
    directory_path = r'P:\Produksjon\CNCEdit\Programmer\2103 PUMA 700L LM'  
    first_available_number = find_first_available_number(directory_path)
    print("Første tilgjengelige nummer etter 1000 er:", first_available_number)

    # Filen du ønsker å endre
    filename = r'fil.md'
    modify_file(filename, first_available_number)
    print(f"Endret heading i {filename} til O{first_available_number}.")


