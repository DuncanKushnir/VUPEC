"""
Calculates the energy requirement for driving
"""
import pandas as pd

from model.vehicle import setup_vehicle, add_idle_behaviour
from model.physics import add_external_physics
from model.accessories import add_accessory_demands
from model.drivetrain import allocate_demands
from model.battery import process_battery_demand
from model.motors import apply_motor_efficiencies
from model.constants import *


def run_model(global_params, vehicle, drive_cycle):
    """
    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param drive_cycle: a drive_cyles.DriveCycle object
    :return: a dataframe with the summary information
    """
    start = pd.Timestamp.utcnow()

    vehicle = setup_vehicle(global_params, vehicle)
    model_df = drive_cycle.to_df()
    model_df = add_external_physics(global_params, vehicle, model_df)
    model_df = add_accessory_demands(global_params, vehicle, model_df)
    model_df = allocate_demands(global_params, vehicle, model_df)
    model_df = process_battery_demand(global_params, vehicle, model_df)
    model_df = apply_motor_efficiencies(global_params, vehicle, model_df)

    model_df["energy_from_engine"] = (
        model_df[model_df["energy_at_wheel"] > 0]["energy_at_wheel"]
    ) / 0.98
    model_df["thermal_input"] = model_df["energy_from_engine"] / 0.25
    model_df["petrol_input"] = model_df["thermal_input"] / 42000000

    end = pd.Timestamp.utcnow()

    print((end - start).total_seconds(), "seconds to run one model pass")
    return model_df


def make_summary(model_df):
    summary = []


if __name__ == "__main__":
    print("start")
    start = pd.Timestamp.utcnow()
    from model.data import data
    from model.common import ObjDict

    vehicle = data["vehicles"]["default"]

    parameters = {
        "simulate_wind": False,
        "wind_speed": 0,
        "wind_angle": 0.0,
        "altitude": 0.0,
        "temperature": 20,
    }

    drive_cycle = data["drive_cycles"]["hwfe"]
    model = run_model(parameters, vehicle, drive_cycle)
    # print(model.head())
    print(model["loss_rolling"].sum(), "J lost to rolling resistance")
    print(model["loss_drag"].sum(), "J lost to drag")

    print(
        model[model["energy_at_wheel"] < 1]["energy_at_wheel"].sum() * -1,
        "J lost to " "braking",
    )

    print(model["energy_from_engine"].sum(), "J from engine at brake")

    print(model.head())

    print("Cycle Economy\n*******************")
    print("petrol:")
    cycle_economy = (
        model["petrol_input"].sum() * 100 * 1000 / drive_cycle.total_distance
    )
    print("cycle_economy:", cycle_economy, "L/100km")
    cycle_economym = GALUS_L / (cycle_economy / 100 * MILE_KM)
    print("cycle_economy:", cycle_economym, "mpg")
    end = pd.Timestamp.utcnow()
    print((end - start).total_seconds(), "total seconds")
