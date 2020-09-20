import sys, os

import datetime

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(MODEL_DIR)
sys.path.append(SRC_DIR)

import model.energy_calculator as calc
import model.output as output


def run_model_from_json():
    pass


def run_model_from_control_panel():
    from model.model_setup import config_from_panel

    global_parameters, vehicle, drive_cycle = config_from_panel()
    model_df = calc.run_model(global_parameters, vehicle, drive_cycle)
    output.output_model_run(global_parameters, model_df, drive_cycle)


if __name__ == "__main__":
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    args = sys.argv
    if len(args) == 1:
        run_model_from_control_panel()
    else:
        print("Json not tied in yet")
