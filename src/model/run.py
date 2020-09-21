import sys, os

import datetime

import model.energy_calculator as calc
import model.output as output
from model.constants import *


MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(MODEL_DIR)
sys.path.append(SRC_DIR)


def run_model_from_json():
    pass


def run_model_from_control_panel():
    from model.model_setup import config_from_panel

    global_parameters, vehicles, drive_cycle = config_from_panel()

    results = []
    for vehicle in vehicles:
        model_df = calc.run_model(global_parameters, vehicle, drive_cycle)
        model_df.drop("segment_type", axis=1, inplace=True)
        model_df._output_name = vehicle._output_name
        results.append(model_df)

        print(vehicle.to_json())
        print(
            f"\n{model_df._output_name}: cycle economy on "
            f"(insert name)\n*******************"
        )
        print("petrol:")
        cycle_economy = (
            model_df["input_petrol"].sum() * 100 * 1000 / drive_cycle.delta_d.sum()
        )
        print("cycle_economy:", cycle_economy, "L/100km")
        cycle_economym = GALUS_L / (cycle_economy / 100 * MILE_KM)
        print("cycle_economy:", cycle_economym, "mpg")

        if len(results) == 2:
            diff = results[1] - results[0]
            diff._output_name = "difference"
            results.append(diff)

            print(
                f"\ndifference : cycle economy on "
                f"(insert name)\n*******************"
            )
            print("petrol:")
            cycle_economy = (
                diff["input_petrol"].sum() * 100 * 1000 / drive_cycle.delta_d.sum()
            )
            print("cycle_economy:", cycle_economy, "L/100km")
            cycle_economym = GALUS_L / (cycle_economy / 100 * MILE_KM)
            print("cycle_economy:", cycle_economym, "mpg")

    output.output_model_run(global_parameters, results)


if __name__ == "__main__":
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    args = sys.argv
    if len(args) == 1:
        run_model_from_control_panel()
    else:
        print("Json not tied in yet")
