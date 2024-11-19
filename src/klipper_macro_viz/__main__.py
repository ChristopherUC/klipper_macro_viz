import sys
import re
from pathlib import Path
from pprint import pprint as pretty
from anytree import Node, RenderTree


DEFAULT_DIR = Path(Path.home(),"printer_data","config")

def find_all_cfg_files(dir_for_files): 
    print(f"Directory to check for Macros is: {dir_for_files}")
    cfg_files = Path(dir_for_files).glob('**/*')
    config_file_list = []
    non_config_file_name_list = []
    for a_file in cfg_files:
        file_info = {
            "path_object": a_file,
            "name": a_file.name,
            "line_count": -1,
        }
        if ".cfg" in str(a_file):
            config_file_list.append(file_info)
        else:
            non_config_file_name_list.append(file_info)
    return config_file_list


def is_macro_definition(line_of_file):
    macro_name = re.search("^\[gcode_macro (.*)\]$",line_of_file)
    try:
        name = macro_name.group(1)
    except AttributeError:
        return False
    return name

def find_macro_definitions(file_list_of_dicts):
    macro_references = {}
    file_list = [x for x in file_list_of_dicts]
    for file_dict in file_list_of_dicts:
        with open(file_dict["path_object"], 'r') as open_file:
            line_number = 0
            for config_line in open_file:
                line_number += 1
                found_macro = is_macro_definition(config_line)
                if not found_macro:
                    continue
                source = {"file_name": open_file.name,
                    "definition": config_line,
                    "line_no": line_number,
                    }
                macro_references.setdefault(found_macro, []).append(source)
            file_dict["line_count"] = line_number
    return macro_references

def main(macro_directory=None, find_macro=None):
    
    files_to_check = find_all_cfg_files(macro_directory)
    macro_definitions = find_macro_definitions(files_to_check)

    macro_list = macro_definitions.keys()  # not sure I will keep this

    hierarchy = {}
    occurrence_references = {}
    occurrences = {}
    for each_macro in macro_list:
         occurrences[each_macro] = 0

    total_lines = 0  # how many total lines are there in all files
    for cfg_file in files_to_check:  # check all files
        with open(cfg_file["path_object"], 'r') as open_file:
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
                    for macro_name in macro_list:  # we will look for EVERY macro
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
