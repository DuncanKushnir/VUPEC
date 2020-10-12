from model import physics
from model.data import data
from model.tires import parse_tire_string
from model.battery import Battery
from model.model_setup import initialize_vehicle

DATA_ROOT = data["vehicles"]

def setup_vehicle(global_params, vehicle):
    """
    Turns parameters into objects
    """
    # Calculate tire parameters
    vehicle.tires.update(parse_tire_string(vehicle.tires.size))

    # Setup battery
    if vehicle.batt_cap != 'None':
        vehicle.battery = Battery(vehicle['batt_cap'], 'li-ion')
    else:
        vehicle.battery = None
    return vehicle



class Vehicle:
    init_type = 'base'

    def __init__(self, make, model, year=2020, modifications=None):
        self._data = initialize_vehicle(make, model, year)







    def make_variation(self, variation_dict):
        pass


    def calculate_dc(self, drivecycle):
        pass


    def __call__(self, drive_cycle_df):
        if isinstance(drive_cycle_df, DriveCycle):
            drive_cycle_df = DriveCycle.to_df()




    @staticmethod
    def from_manu_model(manufacturer, model):
        pass


def add_idle_behaviour(vehicle, drive_cycle):
    pass

