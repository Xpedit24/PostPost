import os
import re
#
def find_first_available_number(directory):
    files = os.listdir(directory)
    numbers = [int(filename.split('.')[0]) for filename in files if filename.split('.')[0].isdigit()]
    numbers = [num for num in numbers if num > 1000]
    if not numbers:
        return 1001 
    first_available_number = next((num for num in range(1001, max(numbers) + 2) if num not in numbers), None)
    return first_available_number


def find_tool_ranges(content):
    lines = content.splitlines()
    tool_ranges = []
    current_tool_start = None

    # Finn søkeområder (fra T-kode til G00 X300.)
    for i, line in enumerate(lines):
        if re.search(r'(?<!\()\bT\d{4}\b(?!\))', line):  # Finn T-kode utenfor parenteser
            current_tool_start = i
        elif 'G00 X300.' in line and current_tool_start is not None:
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

    # Eendringene
    list1 = ("T0100", "T0200", "T0300", "T0400", "T0500", "T0600", "T0700", "T0800", "T0900", "T1000", "T1100", "T1200", 
             "T1300", "T1400", "T1500", "T1600", "T1700", "T1800", "T1900", "T2000", "T2100", "T2200", "T2300", "T2400")
    for item in list1:
        content = content.replace(item, "G00 Z300.")
 
    # Ulike ting som skal fjernes 
    content = re.sub(r'\bP11\b', '', content)
    content = re.sub(r'\bP12\b', '', content)
    content = re.sub(r'\bM34\n', '', content)
    content = re.sub(r'\bY0\b', '', content)
    content = re.sub(r'\bM278 \(CHAMFERING OFF\)\n', '', content)
    content = re.sub(r'\bM277 \(CHAMFERING ON\)\n', '', content)   
    content = re.sub(r'M24 \(START CHIP CONVEYOR\)\n', '', content) 
    content = re.sub(r'M25 \(STOP CHIP CONVEYOR\)\n', '', content)
    content = re.sub(r'G00 G28 U0\. V0\.', 'G00 X300.', content)
    content = re.sub(r'G28 U0\. V0\.', 'G00 X300.', content)

    # Hent søkeområdene
    tool_ranges = find_tool_ranges(content)
    content = insert_comment_before_operation(content, tool_ranges)  # Bruk den forenklede funksjonen

    # Erstatter de første seks linjene annet
    lines = content.split('\n')
    lines[:6] = ["%", f"O{new_heading} ()",]
    content = '\n'.join(lines)

    # Fjerner linjen etter (OPERATION)
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        #print(line)
        if line.startswith('(OPERATION'):
            next_line_index = i + 2
            if next_line_index < len(lines) and 'G00 X300.' in lines[next_line_index]:
                del lines[next_line_index:next_line_index+2]
        i += 1

    # Lagrer endringene
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))

if __name__ == "__main__":
    filename = r'fil.md'
    directory_path = 'P:/Produksjon/CNCEdit/Programmer/2008 NL 3000-1'  
    first_available_number = find_first_available_number(directory_path)
    print("Første tilgjengelige nummer etter 1000 er:", first_available_number)

    filename = r'fil.md'
    modify_file(filename, first_available_number)
    print(f"Endret heading i {filename} til O{first_available_number}.")

