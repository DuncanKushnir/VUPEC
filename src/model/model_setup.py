"""
Default parameters for various parts
"""
import datetime
import copy

from model.common import ObjDict
from model.vehicle import setup_vehicle
from model.data import data
from model.config import *

PRESET_MAN = ["default"]
PRESET_MOD = [
    "default",
    "sedan" "coupe",
    "suv",
    "compact",
    "bev",
]
PRESET_CYCLE = [
    "nedc",
    "eudc",
    "hwfe",
    "ftp",
    "wltp 3a",
    "wltp 3b",
    "wltp 2",
    "wltp 1",
]


def initialize_vehicle(manufacturer, model, year):
    vehicle = data["vehicles"].get(PRESET_MOD[model], None)
    if vehicle is None:
        raise KeyError(f"{model} not found in vehicle models")
    vehicle = ObjDict.wrap_dict(vehicle.copy())
    if "battery" in vehicle:
        pass
    return vehicle


def initialize_drivecycle(name):

    drive_cycle = data["drive_cycles"].get(PRESET_CYCLE[name], None)
    if drive_cycle is None:
        raise KeyError(f"{name} not found in drive cycles")
    drive_cycle_df = drive_cycle.to_df()
    return drive_cycle_df


def basic_setup_from_panel(basic_dict):
    global_parameters = ObjDict()

    manufacturer = basic_dict.get("preset_manufacturer", 0)
    model = basic_dict.get("preset_model", 0)
    year = basic_dict.get("year", 2020)
    vehicle = initialize_vehicle(manufacturer, model, year)
    vehicle = ObjDict.wrap_dict(vehicle)

    drive_cycle = basic_dict.get("drive_cycle", DEFAULT_DRIVE_CYCLE)
    if drive_cycle == "default":
        drive_cycle = DEFAULT_DRIVE_CYCLE
    drive_cycle = initialize_drivecycle(drive_cycle)

    # At this point we have a copy of the vehicle, and a dataframe constructed from
    # the drive cycle.

    return global_parameters, vehicle, drive_cycle


def config_from_panel():
    from util.excel_utils import extract_control_panel_values

    panel_dict = extract_control_panel_values()

    global_parameters, vehicle, drive_cycle = basic_setup_from_panel(
        panel_dict["basic"]
    )
    vehicle["_output_name"] = "base_vehicle"

    return_vehicles = [vehicle]
    if panel_dict["vehicle"]:
        vehicle_b = ObjDict.wrap_dict(vehicle.copy())
        vehicle_b.update(panel_dict["vehicle"])
        vehicle_b["_output_name"] = "modified_vehicle"
        return_vehicles.append(vehicle_b)

    global_parameters["config_type"] = "control_panel.xlsx"
    global_parameters["run_datetime"] = datetime.datetime.utcnow().strftime(
        "%y-%m-%d-%H-%M-%S"
    )

    return global_parameters, return_vehicles, drive_cycle


if __name__ == "__main__":
    from util.excel_utils import extract_control_panel_values

    # Tests raw panel results
    print(extract_control_panel_values())

    # Tests the results after configuring
    print(config_from_panel())
