import re

def is_macro_definition(line_of_file):
    macro_name = re.search("^\[gcode_macro (.*)\]$",line_of_file)
    try:
        name = macro_name.group(1).lower()
    except AttributeError:
        return False
    return name
