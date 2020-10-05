"""
Calculates the energy requirement for driving
"""
import pandas as pd
import os

from model.vehicle import setup_vehicle, add_idle_behaviour
from model.physics import add_external_physics
from model.accessories import add_accessory_demands
from model.drivetrain import allocate_demands
from model.battery import process_battery_demand
from model.motors import apply_motor_efficiencies
from model.labels import OUTPUT_DF_DESC
from model.constants import *


STANDARD_PIPELINE = [
    add_external_physics,
    add_accessory_demands,
    allocate_demands,
    process_battery_demand,
    apply_motor_efficiencies,
]


def run_pipeline_trace(pipeline, global_parameters, vehicle, model_df):
    """
    """
    pipeline_summary = ["Pipeline summary and trace"]
    cols = set(model_df.columns)
    pipeline_summary.append(f"Initial columns: {sorted(cols)}")
    for operation in pipeline:
        start_time = pd.Timestamp.utcnow()
        pipeline_summary.append(f"\nEntering function: {operation.__name__}")
        model_df = operation(global_parameters, vehicle, model_df)
        pipeline_summary.append(
            f"-> function output: {sorted(set(model_df.columns) - cols)}"
        )
        cols = set(model_df.columns)
        pipeline_summary.append(
            f"-> execution time: "
            f"{(pd.Timestamp.utcnow()-start_time).total_seconds()*1000} milliseconds"
        )

    for line in pipeline_summary:
        print(line)
    return model_df


def run_pipeline(pipeline, global_parameters, vehicle, model_df):
    """
    """
    for operation in pipeline:
        model_df = operation(global_parameters, vehicle, model_df)
    return model_df


def run_model(global_params, vehicle, drive_cycle, func_trace=False):
    """
    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param drive_cycle: a drive_cyles.DriveCycle object
    :return: a dataframe with the summary information
    """
    start = pd.Timestamp.utcnow()
    model_df = drive_cycle.copy()

    vehicle = setup_vehicle(global_params, vehicle)

    if func_trace:
        model_df = run_pipeline_trace(
            STANDARD_PIPELINE, global_params, vehicle, model_df
        )
    else:
        model_df = run_pipeline(STANDARD_PIPELINE, global_params, vehicle, model_df)

    model_df["energy_from_engine"] = (
        model_df[model_df["energy_wheel"] > 0]["energy_wheel"]
    ) / 0.98

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

    drive_cycle = data["drive_cycles"]["nedc"]
    dc = drive_cycle.to_df()

    drive_cycle = dc

    model = run_model(parameters, vehicle, drive_cycle)
    # print(model.head())
    print(model["loss_rolling"].sum(), "J lost to rolling resistance")
    print(model["loss_drag"].sum(), "J lost to drag")

    print(model["loss_friction_brake"].sum(), "J lost to braking")

    print(model["energy_from_engine"].sum(), "J from engine at brake")

    print(model.head())

    print("Cycle Economy\n*******************")
    print("petrol:")
    cycle_economy = model["input_petrol"].sum() * 100 * 1000 / drive_cycle.delta_d.sum()
    print("cycle_economy:", cycle_economy, "L/100km")
    cycle_economym = GALUS_L / (cycle_economy / 100 * MILE_KM)
    print("cycle_economy:", cycle_economym, "mpg")
    end = pd.Timestamp.utcnow()
    print((end - start).total_seconds(), "total seconds")

    print("\nDEV: Changes in labels")
    print("ADD LABELS:")
    for item in model.columns:
        if item not in OUTPUT_DF_DESC:
            print(f'"{item}": ("", ""),')
    print("REMOVE LABELS:")
    for item in OUTPUT_DF_DESC:
        if item not in model.columns:
            print(f'"{item}": ("", ""),')

    print(vehicle.to_json())
    import json

    print(json.dumps(parameters))
