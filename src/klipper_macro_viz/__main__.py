import sys
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
    
    for cfg_file in files_to_check:
        with open(cfg_file) as open_file:
            print(open_file.read())

if __name__=="__main__":
    try:
        macro_dir = Path(sys.argv[1])
    except IndexError as e:
        print("No macro dir provided, defaulting to:")
        print(DEFAULT_DIR)
        macro_dir = Path(DEFAULT_DIR)

    main(macro_dir)