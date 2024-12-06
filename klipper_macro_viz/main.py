import io
import sys
from pathlib import Path
from klipper_macro_viz.utils.search import search

DEFAULT_CONFIG_DIR = Path(Path.home(),"printer_data","config")


def ensure_encoding():
    if sys.stdout.encoding == "UTF-8" or not isinstance(sys.stdout, io.TextIOWrapper):
        return
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    print("hello")

    ensure_encoding()
    
    try:
        macro_dir = Path(sys.argv[1])
    except IndexError as e:
        print("No macro dir provided, defaulting to:")
        print(DEFAULT_CONFIG_DIR)
        macro_dir = Path(DEFAULT_CONFIG_DIR)
    except KeyboardInterrupt:
        sys.exit(0)
    
    try:
        macro_search = sys.argv[2]
    except IndexError as e:
        print("No macro to search provided, defaulting to ALL")
        macro_search = None
    except KeyboardInterrupt:
        sys.exit(0)

    search(macro_dir, macro_search)
