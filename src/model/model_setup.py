"""
Default parameters for various parts
"""
import datetime
import copy

from model.common import ObjDict
from model.battery import Battery
from model.data import data
from model.config import *
from model import api, state

def initialize_vehicle(manufacturer, model, year):
    vehicle = api.mock_data(manufacturer, model)['data']
    vehicle = ObjDict.wrap_dict(vehicle.copy())
    return vehicle


def initialize_drivecycle(name):
    drive_cycle = data["drive_cycles"].get(name, None)
    if drive_cycle is None:
        raise KeyError(f"{name} not found in drive cycles")
    drive_cycle_df = drive_cycle.to_df()
    return drive_cycle_df

def setup_base_vehicle(basic_setup):
    drive_cycle = initialize_drivecycle(basic_setup['drivecycle'])
    global_parameters={'setup': basic_setup}
    global_parameters['config_type'] = 'web_api'
    global_parameters["run_datetime"] = datetime.datetime.utcnow().strftime(
        "%y-%m-%d-%H-%M-%S"
    )

    manufacturer = basic_setup["manufacturer"]
    model = basic_setup["model"]
    year = 2020
    base_vehicle = initialize_vehicle(manufacturer, model, year)
    base_vehicle["_output_name"] = "base_vehicle"
    state.MANUFACTURER = manufacturer
    state.MODEL = model
    state.DRIVE_CYCLE = drive_cycle
    state.BASE_VEHICLE = base_vehicle
    state.DRIVE_CYCLE = drive_cycle
    state.GLOBAL_PARAMS = global_parameters

    return base_vehicle


def basic_setup_from_web_api(submitted_dict):
    print(submitted_dict)
    basic_setup = submitted_dict.pop('setup')
    print('* leftover after setup pop', submitted_dict)
    base_vehicle = setup_base_vehicle(basic_setup)
    return_vehicles = [base_vehicle]

    # Extra, overwritten parameters
    if submitted_dict:
        vehicle_b = setup_scenario_vehicle(base_vehicle, submitted_dict)
        return_vehicles.append(vehicle_b)

    return state.GLOBAL_PARAMS, return_vehicles, state.DRIVE_CYCLE

def setup_scenario_vehicle(base_vehicle, submitted_dict):
    new_vehicle=base_vehicle.copy()
    print(new_vehicle)
    print(submitted_dict)
    new_vehicle['_relative_setup'] = submitted_dict
    for _,v in submitted_dict.items():
        for key, val in v.items():
            new_vehicle[key] = val

    new_vehicle['_output_name'] = 'modified_vehicle'
    return ObjDict.wrap_dict(new_vehicle)

if __name__ == "__main__":
    pass
