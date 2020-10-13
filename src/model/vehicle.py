from model import physics
from model.data import data
from model.tires import parse_tire_string
from model.battery import Battery

DATA_ROOT = data["vehicles"]


def setup_vehicle(global_params, vehicle):
    """
    Turns parameters into objects
    """
    # Calculate tire parameters
    vehicle.tires.update(parse_tire_string(vehicle.tires.size))

    # Setup battery
    if vehicle.battery:
        vehicle.battery_obj = Battery(vehicle.battery.capacity, "li-ion")
    else:
        vehicle.battery_obj = None
    return vehicle


def add_idle_behaviour(vehicle, drive_cycle):
    pass
