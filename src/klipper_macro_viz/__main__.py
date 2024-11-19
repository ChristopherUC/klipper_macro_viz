import sys
import re
from pathlib import Path

DEFAULT_DIR = Path(Path.home(),"printer_data","config")

def main(macro_directory=None):
    print(f"Directory to check for Macros is: {macro_directory}")
    
    cfg_files = Path(macro_directory).glob('**/*')
    files_to_check = []
    files_to_skip = []
    
    for a_file in cfg_files:
        if ".cfg" in str(a_file):
            files_to_check.append(a_file)
            # print(f"Added {a_file} to list")
        else:
            files_to_skip.append(a_file)
            # print(f"skipping file {a_file}")
    
    macros = []
    seen = set()
    for cfg_file in files_to_check:
        with open(cfg_file, 'r') as open_file:
            for line in open_file:
                macro_name = re.search("^\[gcode_macro (.*)\]$",line)
                try:
                    name = macro_name.group(1)
                    if name not in seen:
                        macros.append(name)
                        seen.add(name)
                except AttributeError:
                    pass
    
    hierarchy = {}
    for each_macro in macros:
        hierarchy[each_macro] = [""]

    total_lines = 0  # how many total lines are there in all files
    for cfg_file in files_to_check:  # check all files
        current_macro = ""  # which macro are we currently searching
        file_lines = 0  # how many lines in just THIS file
        with open(cfg_file, 'r') as open_file:
            print("="*80)  # WHAT FILE ARE WE WORKING
            print(f"JUST OPENED file")
            print(f"\t{open_file.name}")
            for line in open_file:  # line-by-line review
                total_lines += 1
                file_lines += 1
                is_comment = re.search("^(#).*",line)
                try:
                    if is_comment.group(1):
                        continue
                except AttributeError:
                    pass
                line = line.strip(' \t\n\r')
                macro_name = re.search("^\[gcode_macro (.*)\]$",line)  # check if we are staring a new macro
                try:
                    current_macro = macro_name.group(1)  # set the new macro name
                    print("-"*20)  # and print the header info
                    print(f"Currently searching line {file_lines}")
                    print(f"inside macro {current_macro}")
                    print(f"\tin file {open_file.name}")
                except AttributeError:  # this line is NOT a new macro
                    for macro_name in macros:  # we will look for EVERY macro
                        if macro_name in line:  # check THIS LINE for each of the individual macros
                            print(f"found reference to {macro_name} in line {line}")
                            try:
                                print(f"BEFORE about to add {macro_name} to hierarchy[{current_macro}]")
                                print(hierarchy[current_macro])
                                hierarchy[current_macro].append(str(line))  # append this line to 
                                print(f"AFTER about to add to hierarchy[{current_macro}]")
                                print(hierarchy[current_macro])
                            except KeyError as e:
                                print(f"\t\tkey error for {macro_name} in line {line} in file {cfg_file}")
                                print(f"")
                                raise e
    print("="*80)
    print(f"{total_lines} total lines searched")
    print("="*80)
    print(hierarchy.keys())
    print("="*80)
    print(hierarchy)
    print("="*80)

if __name__=="__main__":
    try:
        macro_dir = Path(sys.argv[1])
    except IndexError as e:
        print("No macro dir provided, defaulting to:")
        print(DEFAULT_DIR)
        macro_dir = Path(DEFAULT_DIR)

    main(macro_dir)