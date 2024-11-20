import sys
from pathlib import Path

from klipper_macro_viz.search import search


DEFAULT_DIR = Path(Path.home(),"printer_data","config")


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

    search(macro_dir, macro_search)
