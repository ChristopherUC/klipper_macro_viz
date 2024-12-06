import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APPLICATION_ROOT = Path(__file__).resolve().parent
sys.path.append(str(APPLICATION_ROOT))
