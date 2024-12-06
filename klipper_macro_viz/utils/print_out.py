from anytree import Node, RenderTree
from pprint import pprint as pretty

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
