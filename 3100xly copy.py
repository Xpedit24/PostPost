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

def extract_tool_lines(filename):
    tool_lines = []
    start_extraction = False
    with open(filename, 'r') as file:
        for line in file:
            if start_extraction:
                if line.startswith("G21 G00 G18"):
                    break
                tool_lines.append(line.strip())
            elif "(PROGRAMMER - )" in line:
                start_extraction = True
    return tool_lines

def extract_tool_info(filename):
    tool_info = set()  # Bruker en set for å unngå duplikater
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(r'T(\d{4})\s+\|\s+(.*?)\s+\|', line)
            if match:
                tool_info.add((match.group(1), match.group(2)))
    return tool_info

def generate_translation_table(tool_info, tool_lines):
    translation_table = {}
    tool_number = 500
    for idx, (tool_line, tool) in enumerate(zip(tool_lines, tool_info)):
        translation_table[f"#{tool_number + idx}"] = f"{tool[0]} ({tool_line})"
        tool_number +1
    return translation_table

if __name__ == "__main__":
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    directory_path = r'P:\Produksjon\CNCEdit\Programmer\2006 DOOSAN 3100XLY'  
    first_available_number = find_first_available_number(directory_path)
    print("Første tilgjengelige nummer etter 1000 er:", first_available_number)

    # Filen du ønsker å endre
    filename = 'C:/Users/dan.hov/Documents/Python filer/Postpost prossesor/fil.md'
    tool_lines = extract_tool_lines(filename)
    #print("Verktøylinjer:")
    #print(tool_lines)

    tool_info = extract_tool_info(filename)
    #print("\nVerktøyinformasjon:")
    #print(tool_info)

    translation_table = generate_translation_table(tool_info, tool_lines)
    print("\nVerktøyoversettelsestabell:")
    for key, value in translation_table.items():
        print(f"{key} = {value}")
