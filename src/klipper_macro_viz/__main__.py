import sys
import re
from pathlib import Path
from pprint import pprint as pretty

DEFAULT_DIR = Path(Path.home(),"printer_data","config")

def main(macro_directory=None, find_macro=None):
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
    occurrence_references = {}
    occurrences = {}
    for each_macro in macros:
         occurrences[each_macro] = 0

    total_lines = 0  # how many total lines are there in all files
    for cfg_file in files_to_check:  # check all files
        with open(cfg_file, 'r') as open_file:
            file_lines = 0  # how many lines in just THIS file
            current_macro = None  # which macro are we currently searching
            print("="*80)  # WHAT FILE ARE WE WORKING
            print(f"JUST OPENED file")
            print(f"\t{open_file.name}")
            for line in open_file:  # line-by-line review
                total_lines += 1
                file_lines += 1
                is_comment = re.search("^(#).*",line)
                try:
                    if is_comment.group(1):
                        continue  # line was a comment, continue the loop
                except AttributeError:
                    pass  # not a comment, proceed
                line = line.strip(' \t\n\r')  # cleanup the line
                macro_name = re.search("^\[gcode_macro (.*)\]$",line)  # check if we are staring a new macro
                try:
                    current_macro = macro_name.group(1)  # set the new macro name
                    print("-"*20)  # and print the header info
                    print(f"Currently searching line {file_lines}")
                    print(f"inside macro {current_macro}")
                    print(f"\tin file {open_file.name}")
                except AttributeError:  # this line is NOT a new macro
                    if current_macro is None:
                        continue  # we aren't actually looking inside a macro yet
                    for macro_name in macros:  # we will look for EVERY macro
                        if macro_name in line:  # check THIS LINE for each of the individual macros
                            print(f"\t\tfound reference to {macro_name} in line {line}")
                            try:
                                reference = {'line': line, 
                                             'line_no': file_lines,
                                             'file_name': open_file.name,
                                             }
                                hierarchy.setdefault(current_macro, []).append(reference)  # append this line to 
                                occurrences[macro_name] +=1
                                occurrence_references.setdefault(macro_name, []).append(current_macro)
                            except KeyError as e:
                                print(f"\t\tkey error for {macro_name} in line {line} in file {cfg_file}")
                                print(f"")
                                raise e
    print("="*80)
    print(f"{total_lines} total lines searched")
    # print("="*80)
    # print(hierarchy.keys())
    # print("="*80)
    # print(hierarchy)
    print("="*80)
    print(f"{len(occurrences)} total macros")
    print("="*80)
    print(f"{len(files_to_check)} total files")
    print("="*80)
    if find_macro is None:
        pretty(occurrences)
    else:
        print(f"Macro {find_macro} appears {occurrences[find_macro]} times")
        print(f"in the following macros")
        pretty(f"{occurrence_references[find_macro]}")
        print(f"Macro {find_macro} references {len(hierarchy[find_macro])} other macros")
        pretty(hierarchy[find_macro])


if __name__=="__main__":
    try:
        macro_dir = Path(sys.argv[1])
    except IndexError as e:
        print("No macro dir provided, defaulting to:")
        print(DEFAULT_DIR)
        macro_dir = Path(DEFAULT_DIR)
    try:
        macro_search = sys.argv[2]
    except IndexError as e:
        print("No macro to search provided, defaulting to ALL")
        macro_search = None

    main(macro_dir, macro_search)