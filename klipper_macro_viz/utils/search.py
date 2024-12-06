import re

from klipper_macro_viz.utils.find_all_cfg_files import find_all_cfg_files
from klipper_macro_viz.utils.find_macro_definitions import find_macro_definitions

from anytree import Node, RenderTree

from pprint import pprint as pretty


def search(config_file_dir=None, macro_name_to_search=None):
    files_to_check = find_all_cfg_files(config_file_dir)
    macro_definitions = find_macro_definitions(files_to_check)
    # macro_list = macro_definitions.keys()  # not sure I will keep this

    a, b, c = deep_search(files_to_check, macro_definitions)

    print_output(a, b, c, files_to_check, macro_name_to_search, macro_definitions) 


def deep_search(file_name_list=None, macro_sources=None):
    hierarchy = {}
    occurrence_references = {}
    occurrences = {each_macro.lower(): 0 for each_macro in  macro_sources}

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
                    for name in macro_sources:  # we will look for EVERY macro
                        if name in line.lower():  # check THIS LINE for each of the individual macros
                            print(f"\t\t\tfound reference to {macro_name} in line {line}")
                            try:
                                reference = {'line': line,
                                             'line_no': file_lines,
                                             'file_name': open_file.name,
                                             }
                                hierarchy.setdefault(current_macro, []).append(reference)  # append this line to 
                                occurrences[name] +=1
                                occurrence_references.setdefault(name, []).append(current_macro)
                            except KeyError as e:
                                print(f"\t\tkey error for {name} in line {line} in file {cfg_file}")
                                print(f"")
                                raise e
    return hierarchy, occurrence_references, occurrences


def print_output(hierarchy, occurrence_references, occurrences, file_name_list, find_macro, macro_definitions):
    total_lines = sum([each_file["line_count"] for each_file in file_name_list])
    print("="*80)
    print(f"{total_lines} total lines searched")
    # print("="*80)
    # print(hierarchy.keys())
    # print("="*80)
    # print(hierarchy)
    print("="*80)
    print(f"{len(occurrences)} total macros")
    print("="*80)
    print(f"{len(file_name_list)} total files")
    print("="*80)
    if find_macro is None:
        pretty(occurrences)
    else:
        print(f"Macro {find_macro} appears {occurrences[find_macro]} times")
        if int(occurrences[find_macro]) > 0:
            print(f"in the following macros")
            pretty(f"{occurrence_references[find_macro]}")
        try:
            print(f"Macro {find_macro} references {len(hierarchy[find_macro])} other macros")
            pretty(hierarchy[find_macro])
        except KeyError:
            print(f"Macro {find_macro} references 0 other macros")
        try:
            print(macro_definitions[find_macro])
            if len(macro_definitions[find_macro]) > 1:
                print("="*80)
                print("="*80)
                print("="*80)
                print("HOOOOOOOOOOOLLLLLLLLLLEEEEEEEEEEEEEEEE SSSSSHHHHHHHIIIIIIIIIITTTTTTTTTTT")
                print("There should NOT be more than one definition for any macro")
                print("="*80)
                print("="*80)
                print("="*80)
        except KeyError:
            print("definition not found, WTF")

    print("="*80)  # occurrence_references
    file_list = Node("config")
    macro_nodes = []
    for each_macro in occurrence_references:
        macro_nodes.append(Node(each_macro, parent=file_list))
    for pre, fill, node in RenderTree(file_list):
        print("%s%s" % (pre, node.name))

    print("="*80)  # macro_definitions
    macro_list = Node("config_file")
    # print("macdef:/",macro_definitions,"/")
    file_nodes = {}
    for macro_name, macro_data in macro_definitions.items():
        # print(macro_name)
        # print(macro_data[0]['file_name'])
        try:
            file_node = file_nodes[macro_data[0]['file_name']]
        except KeyError:
            file_node = file_nodes[macro_data[0]['file_name']] = Node(macro_data[0]['file_name'], parent=macro_list)
        file_nodes[macro_name] = Node(macro_name, parent=file_node)
    for pre, fill, node in RenderTree(macro_list):
        print("%s%s" % (pre, node.name))
    print("="*80)
