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

 
   # Finn strengen "G00 G28 U0. V0." og legg til "GOO G30 P3 W0." under den
    #content = re.sub(r'(G00 G28 U0\. V0\.)\n', r'\1\nG00 G30 P3 W0.\n', content)
    content = re.sub(r'\bM278 \(CHAMFERING OFF\)\n', '', content)
    content = re.sub(r'\bM277 \(CHAMFERING ON\)\n', '', content)  
    content = re.sub(r'M289 \(SELECT C1 CLAMP CONTROL\)\n', '', content)
    content = re.sub(r'M289 \(SELECT C1 CLAMP CONTROL\)\n', '', content)
    content = re.sub(r'M24 \(START CHIP CONVEYOR\)\n', '', content) 
    content = re.sub(r'M25 \(STOP CHIP CONVEYOR\)\n', '', content)
    content = re.sub(r'M89\n', '', content)
    content = re.sub(r'M08', 'M21', content)
    content = re.sub(r'M8', 'M21', content)
#    content = re.sub(r'G00 G28 U0\. V0\.', 'G00 X300.', content)

    # Gjør endringene
    list1 = ("T0100", "T0200", "T0300", "T0400", "T0500", "T0600", "T0700", "T0800", "T0900", "T1000", "T1100", "T1200", 
             "T1300", "T1400", "T1500", "T1600", "T1700", "T1800", "T1900", "T2000", "T2100", "T2200", "T2300", "T2400")
    for item in list1:
        content = content.replace(item, "G65 P9029 A50.")
        
    
    # Erstatter de første seks linjene annet
    lines = content.split('\n')
    lines[:6] = ["%", f"O{new_heading} ()", ""]
    content = '\n'.join(lines)
    # Lagrer endringene
    with open(filename, 'w') as file:
        file.write(content)


    # Fjerner linjen etter (OPERATION)
 #   i = 1
 #   while i < len(lines):
 #       line = lines[i].strip()
 #       if line.startswith('(OPERATION'):
 #           next_line_index = i + 1
 #           if next_line_index < len(lines) and ('G00 G28 U0. V0.' in lines[next_line_index] or 'G01 G28 U0. V0.' in lines[next_line_index]):
 #               del lines[next_line_index:next_line_index+2]
 #       i += 1

    # Lagrer endringene
    with open(filename, 'w') as file:
        file.write('\n'.join(lines))


if __name__ == "__main__":
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    filename = r'P:\Produksjon\python\test\fil.md'
    directory_path = r'P:\Produksjon\CNCEdit\Programmer\2101 PUMA 700LY'  
    first_available_number = find_first_available_number(directory_path)
    print("Første tilgjengelige nummer etter 1000 er:", first_available_number)

    # Filen du ønsker å endre
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    filename = r'P:\Produksjon\python\test\fil.md'
    modify_file(filename, first_available_number)
    print(f"Endret heading i {filename} til O{first_available_number}.")


