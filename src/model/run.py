import sys, os

import datetime

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(MODEL_DIR)
sys.path.append(SRC_DIR)

import model.energy_calculator as calc
from util.locations import *


def run_model_from_json():
    pass


def run_model_from_control_panel():
    from model.model_setup import config_from_panel

    global_parameters, vehicle, drive_cycle = config_from_panel()
    model_df = calc.run_model(global_parameters, vehicle, drive_cycle)

    output_stem = global_parameters["run_datetime"] + "_"
    output_data = os.path.join(OUTPUT_DIR, output_stem + "data.csv")

    output_summ = os.path.join(OUTPUT_DIR, output_stem + "summary.txt")
    model_df.to_csv(output_data, index=False)


if __name__ == "__main__":
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    args = sys.argv
    if len(args) == 1:
        run_model_from_control_panel()
    else:
        print("Json not tied in yet")
