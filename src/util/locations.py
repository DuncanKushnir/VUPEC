import os

UTIL_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(UTIL_DIR)
ROOT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
GUI_DIR = os.path.join(SRC_DIR, "gui")
GUI_STATIC_DIR = os.path.join(GUI_DIR, "static")
CTL_PANEL_FILE = os.path.join(ROOT_DIR, "control_panel.xlsx")

print(f"working with data found in {DATA_DIR}")
