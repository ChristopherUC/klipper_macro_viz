import re

from klipper_macro_viz.utils.find_all_cfg_files import find_all_cfg_files
from klipper_macro_viz.utils.find_macro_definitions import find_macro_definitions
from klipper_macro_viz.utils.print_out import print_output

def search(config_file_dir=None, macro_name_to_search=None):
    files_to_check = find_all_cfg_files(config_file_dir)
    macro_definitions = find_macro_definitions(files_to_check)

    hier, refs, counts = deep_search(files_to_check, macro_definitions)

    print_output(hier, refs, counts, files_to_check, macro_name_to_search, macro_definitions) 


def deep_search(file_name_list=None, macro_sources=None):
    hierarchy = {}
    occurrence_references = {}
    occur_counts = {each_macro.upper(): 0 for each_macro in  macro_sources}

    for cfg_file in file_name_list:  # check all files
        file_lines = 0
        with open(cfg_file["path_object"], 'r') as open_file:
            current_macro = None  # which macro are we currently searching
            print("="*80)  # WHAT FILE ARE WE WORKING
            print(f"JUST OPENED file")
            print(f"\t{open_file.name}")
            for line in open_file:  # line-by-line review
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
                    print(f"\tinside macro {current_macro}")
                    print(f"\t\tin file {open_file.name}")
                except AttributeError:  # this line is NOT a new macro
                    if current_macro is None:
                        continue  # we aren't actually looking inside a macro yet

                    # TODO: this is NOT working correctly yet, review algorithm
                    for name in macro_sources:  # we will look for EVERY macro
                        if name in line.upper():  # check THIS LINE for each of the individual macros
                            print(f"\t\t\tfound reference to {macro_name} in line {line}")
                            try:
                                reference = {'macro_name': name,
                                             'line': line,
                                             'line_no': file_lines,
                                             'file_name': open_file.name,
                                             }
                                hierarchy.setdefault(current_macro, []).append(reference)  # append this line to 
                                occur_counts[name] +=1
                                occurrence_references.setdefault(name, []).append(current_macro)
                            except KeyError as e:
                                print(f"\t\tkey error for {name} in line {line} in file {cfg_file}")
                                print(f"")
                                raise e
    return hierarchy, occurrence_references, occur_counts
