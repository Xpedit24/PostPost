import os
import re

def find_first_available_number(directory):
    files = os.listdir(directory)
    numbers = [int(filename.split('.')[0]) for filename in files if filename.split('.')[0].isdigit()]
    numbers = [num for num in numbers if num > 1000]
    if not numbers:
        return 1001 
    first_available_number = next((num for num in range(1001, max(numbers) + 2) if num not in numbers), None)
    return first_available_number

def modify_file(filename, new_heading):
    with open(filename, 'r') as file:
        content = file.read()
    
    # Update the heading
    updated_content = re.sub(r'^O\d+', f'O{new_heading}', content, flags=re.MULTILINE)

    # Add #500=1 after the line containing "G00 G18 G40 G80 G99"
    updated_content = re.sub(r'^(.*M24.*)$', r'\1\n#500=1 (RIGGING = 0, PRODUSKJON = 1)', updated_content, flags=re.MULTILINE)


    # Add M117 after the line containing "M999"
    updated_content = re.sub(r'^(.*M999.*)$', r'\1\nM117', updated_content, flags=re.MULTILINE)

    # SIDE 011 I BOKA
    updated_content = re.sub(r'^(.*M05 P11.*)$', r'\1\n(M244 U5000. W5000. F1000. Q0) (FOR OPPMALING)', updated_content, flags=re.MULTILINE)

    # List of tool codes to check
    tool_codes = [f'T{i:02d}{j:02d}' for i in range(1, 100) for j in range(1, 100)]
    
    # Split content into lines for processing
    lines = updated_content.split('\n')
    updated_lines = []
    line_number = 900
    tool_counter = 1
    
    for line in lines:
        if any(tool_code in line for tool_code in tool_codes) and not line.strip().startswith('('):
            new_tool_code = f'T{tool_counter:02d}99'
            new_tool_code_1 = f'T{tool_counter:02d}{tool_counter:02d}'
            # Add lines above the tool code line
            updated_lines.append(f'IF[#500 EQ 1]GOTO {line_number}\nG10 L3\nP{tool_counter} L100 (L ER TOOL LIFE)\n{new_tool_code_1}\nG11\nN{line_number}')
            line_number += 1
            
            # Modify the tool code line
            modified_line = re.sub(r'T\d{4}', new_tool_code, line)
            updated_lines.append(modified_line)
            
            # Add lines below the tool code line
            next_line_number = line_number + 1
            updated_lines.append(f'#500 = 0.0 (GRUPPE OFFSETT)\n#501 = #4120\nN{line_number}\nIF[#501 LT 100]GOTO {next_line_number}\n#501 = [#501 - 100]\nGOTO {line_number}\nN{next_line_number}\n#501 = [#501 + 2000]\n#[#501] = #500')
            line_number = next_line_number + 1
            
            tool_counter += 1
        else:
            updated_lines.append(line)

    # Recombine the updated lines into a single string
    updated_content = '\n'.join(updated_lines)

    # Further modifications based on the previous script
    # Remove specific lines
    updated_content = re.sub(r'\bM278 \(CHAMFERING OFF\)\n', '', updated_content)
    updated_content = re.sub(r'\bM277 \(CHAMFERING ON\)\n', '', updated_content)
    updated_content = re.sub(r'M289 \(SELECT C1 CLAMP CONTROL\)\n', '', updated_content)

    # Replace specific tool codes with G30 P3 W0.
    specific_tool_codes = ["T0100", "T0200", "T0300", "T0400", "T0500", "T0600", "T0700", "T0800", "T0900", "T1000", 
                           "T1100", "T1200", "T1300", "T1400", "T1500", "T1600", "T1700", "T1800", "T1900", "T2000", 
                           "T2100", "T2200", "T2300", "T2400"]
    for code in specific_tool_codes:
        updated_content = updated_content.replace(code, "G30 P3 W0.")

    # Remove lines after (OPERATION) if they match specific patterns
    lines = updated_content.split('\n')
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('(OPERATION'):
            next_line_index = i + 1
            if next_line_index < len(lines) and ('G00 G28 U0. V0.' in lines[next_line_index] or 'G01 G28 U0. V0.' in lines[next_line_index]):
                del lines[next_line_index]
        i += 1

    # Save the changes
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))


if __name__ == "__main__":
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    directory_path = r'P:\Produksjon\CNCEdit\Programmer\2006 DOOSAN 3100XLY'  
    first_available_number = find_first_available_number(directory_path)
    print("Første tilgjengelige nummer etter 1000 er:", first_available_number)

    # Filen du ønsker å endre
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    modify_file(filename, first_available_number)
    print(f"Endret heading i {filename} til O{first_available_number}.")


