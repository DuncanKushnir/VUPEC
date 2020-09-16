"""
Default parameters for various parts
"""
import datetime

from model.data import data
from model.config import *


def basic_setup(basic_dict):
    vehicle = {}
    global_parameters = {}
    drive_cycle = {}
    manufacturer = basic_dict.get("preset_manufacturer", "default")
    model = basic_dict.get("preset_model", "default")
    year = basic_dict.get("year", "default")
    vehicle = data["vehicles"].get(model, None)
    drive_cycle = basic_dict.get("drive_cycle", "nedc")
    if drive_cycle == "default":
        drive_cycle = DEFAULT_DRIVE_CYCLE
    drive_cycle = data["drive_cycles"].get(drive_cycle, None)

    return global_parameters, vehicle, drive_cycle


def config_from_panel():
    from util.excel_utils import extract_control_panel_values

    panel_dict = extract_control_panel_values()
    global_parameters, vehicle, drive_cycle = basic_setup(panel_dict["basic"])

    global_parameters["config_type"] = "control_panel.xlsx"
    global_parameters["run_datetime"] = datetime.datetime.utcnow().strftime(
        "%y-%m-%d-%H-%M"
    )
    return global_parameters, vehicle, drive_cycle


if __name__ == "__main__":
    print(config_from_panel())
