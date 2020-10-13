from model.data import data
from model.tires import parse_tire_string
from model.battery import Battery
from model.motors import ElectricMotor, PetrolMotor

DATA_ROOT = data["vehicles"]


def setup_vehicle(global_params, vehicle):
    """
    Turns parameters into objects
    """
    # Calculate tire parameters
    vehicle.tires.update(parse_tire_string(vehicle.tires.size))

    # Setup battery
    if vehicle.battery.capacity:
        vehicle.el_motor.obj = ElectricMotor()
        vehicle.battery_obj = Battery(vehicle.battery.capacity, "li-ion")
    else:
        vehicle.battery_obj = None

    if vehicle.ff_motor:
        vehicle.ff_motor.obj = PetrolMotor()

    return vehicle
