import sys, os

from model import energy_calculator as calc
from model.constants import *
from model import output, state

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(MODEL_DIR)
sys.path.append(SRC_DIR)


def single_pass(global_parameters, vehicle, drive_cycle):
    model_df = calc.run_model(global_parameters, vehicle, drive_cycle)
    model_df.drop("segment_type", axis=1, inplace=True)
    model_df._output_name = vehicle._output_name
    return model_df


def extract_efficiencies(model_df, drive_cycle, prefix=""):
    petrol_economy = (
        model_df["input_petrol"].sum() * 100 * 1000 / drive_cycle.delta_d.sum()
    )
    if "el_input_total" in model_df.columns:
        el_economy = (
            model_df["el_input_total"][0]
            * 100
            * 1000
            / drive_cycle.delta_d.sum()
            / KWH_J
        )
    else:
        el_economy = 0.0

    petrol_economy = "{:g}".format(float("{:.{p}g}".format(petrol_economy, p=3)))
    el_economy = "{:g}".format(float("{:.{p}g}".format(el_economy, p=3)))
    return {
        "result": {
            f"{prefix}ff_consumption": petrol_economy,
            f"{prefix}fossil_fuel": "Petrol",
            f"{prefix}el_consumption": el_economy,
        }
    }


def run(global_parameters, vehicles, drive_cycle, output_result=False):
    results = []
    for vehicle in vehicles:
        model_df = single_pass(global_parameters, vehicle, drive_cycle)
        results.append(model_df)

        # print(vehicle.to_json())
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

    if output_result:
        output.output_model_run(global_parameters, results)
    return results


if __name__ == "__main__":
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    args = sys.argv
    print(args)
    print("cmdline use not supported yet, and json server is disabled for this release")
