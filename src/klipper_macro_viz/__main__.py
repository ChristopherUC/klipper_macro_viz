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

    total_lines = 0
    for cfg_file in files_to_check:
        current_macro = ""
        file_lines = 0
        with open(cfg_file, 'r') as open_file:
            for line in open_file:
                total_lines += 1
                file_lines += 1
                macro_name = re.search("^\[gcode_macro (.*)\]$",line)
                try:
                    current_macro = macro_name.group(1)
                    print("="*80)
                    print(f"Currently searching inside macro {current_macro}")
                    print(f"\tin file {open_file}")
                    print(f"\ton line {file_lines}")
                except AttributeError:
                    for macro_name in macros:
                        if macro_name in line:
                            # print(f"found {macro_name} in line {line}")
                            try:
                                hierarchy[current_macro].append(str(line))
                            except KeyError:
                                print(f"\t\tkey error for {macro_name} in line {line} in file {cfg_file}")
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