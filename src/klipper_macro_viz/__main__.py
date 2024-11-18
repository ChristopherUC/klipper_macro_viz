import sys
from pathlib import Path

DEFAULT_DIR = "~/printer_data/config/"

def main(macro_directory=None):
    print(f"Directory to check for Macros is: {macro_directory}")
    
    cfg_files = Path(macro_directory).glob('**/*')
    files_to_check = []
    
    for a_file in cfg_files:
        if ".cfg" in str(a_file):
            files_to_check.append(a_file)
            print(f"Added {a_file} to list")
        else:
            print(f"skipping file {a_file}")


if __name__=="__main__":
    try:
        macro_dir = Path(sys.argv[1])
    except IndexError as e:
        print("No macro dir provided, defaulting to:")
        print(DEFAULT_DIR)
        macro_dir = Path(DEFAULT_DIR)

    main(macro_dir)