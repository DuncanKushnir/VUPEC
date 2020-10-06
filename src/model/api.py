import os
import matplotlib.pyplot as plt

from model import state, data, model_setup, run
from model.mock_data import mock_data

from util.locations import GUI_STATIC_DIR


def get_manufacturer_list():
    return ["generic", "volvo"]


def setup_model(manufacturer, model, drivecycle):
    base_setup = {'manufacturer' :manufacturer,
                  'model': model,
                  'drivecycle': drivecycle}

    model_setup.setup_base_vehicle(base_setup)
    state.BASE_RESULT = run.single_pass(state.GLOBAL_PARAMS,
                                        state.BASE_VEHICLE,
                                        state.DRIVE_CYCLE)
    result = mock_data(manufacturer, model)
    result.update(run.extract_efficiencies(state.BASE_RESULT,
                                           state.DRIVE_CYCLE))
    return result

def run_model(global_params, vehicles, drive_cycle):
    print(global_params, vehicles, drive_cycle)
    run.run(global_params, vehicles, drive_cycle)

def get_model_list(manufacturer):
    if manufacturer == "generic":
        return ["generic", "generic_suv"]
    return ["s60", "s60_twen", "s90", "s90_twen"]


def get_drivecycle_list():
    return data.data["drive_cycles"].keys()


def update_drivecycle_image(drive_cycle_df, dc_name):
    image_path = os.path.join(GUI_STATIC_DIR, f"{dc_name}.png")
    if not os.path.exists(image_path):
        print("Generating image", image_path)
        drive_cycle_df.plot(x="start_time", y="start_v")
        plt.margins(0)
        plt.savefig(image_path)


def change_drivecycle(drive_cycle_name):
    drive_cycle = data.data["drive_cycles"][drive_cycle_name]
    dc_df = drive_cycle.to_df()
    update_drivecycle_image(dc_df, drive_cycle_name)


def get_basic_state():
    basic_state = {
        "manufacturer": state.MANUFACTURER,
        "model": state.MODEL,
        "drive_cycle": state.DRIVE_CYCLE,
    }
    return basic_state


def process_submit(submit_dict):
    pass
