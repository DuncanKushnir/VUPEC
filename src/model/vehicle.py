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
    if 'batt_cap' in vehicle:
        vehicle.battery = Battery(vehicle['batt_cap'], 'li-ion')

    return vehicle


def add_idle_behaviour(vehicle, drive_cycle):
    pass


class Vehicle:
    """
    Coordinates the components and calculations for a vehicle
    """

    def __init__(self, **kwargs):
        self.engine = kwargs.get("engine", None)
        self.drive_train = kwargs.get("drive_train", None)
        self.battery = kwargs.get("battery", None)
        self.physical = kwargs.get("physical", None)
        self.locations = None

    def set_constants(self):
        """
        Sets up constant values
        """
        self.rolling_resistance = physics.rolling_resistance_simple(
            self.physical.mass, self.physical.crr
        )

    def f_at_v(self, v):
        """
        :param v:  a velocity in m/s
        :return: the sum of all external forces on the vehicle at velocity v
        """
        return self.rolling_resistance
