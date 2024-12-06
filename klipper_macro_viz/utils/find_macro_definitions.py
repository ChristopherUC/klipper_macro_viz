from klipper_macro_viz.utils.is_macro_definition import is_macro_definition


def find_macro_definitions(file_list_of_dicts):
    macro_references = {}
    for file_dict in file_list_of_dicts:
        with open(file_dict["path_object"], 'r') as open_file:
            line_number = 0
            for config_line in open_file:
                line_number += 1
                found_macro = is_macro_definition(config_line)
                if not found_macro:
                    continue
                macro_source = {
                    "file_name": open_file.name,
                    "line_no": line_number,
                    "definition": config_line,
                    }
                macro_references.setdefault(found_macro, []).append(macro_source)
            file_dict["line_count"] = line_number
    return macro_references
