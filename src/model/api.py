import os
import matplotlib.pyplot as plt
from collections import defaultdict

from model import state, data, model_setup, run
from model.mock_data import mock_data

from util.locations import GUI_STATIC_DIR


def get_manufacturer_list():
    return ["generic", "volvo"]


def setup_model(manufacturer, model, drivecycle):
    base_setup = {
        "manufacturer": manufacturer,
        "model": model,
        "drivecycle": drivecycle,
    }

    model_setup.setup_base_vehicle(base_setup)
    state.BASE_RESULT = run.single_pass(
        state.GLOBAL_PARAMS, state.BASE_VEHICLE, state.DRIVE_CYCLE
    )
    result = mock_data(manufacturer, model)
    result["data"] = flatten_vehicle_dict(result["data"])
    result.update(run.extract_efficiencies(state.BASE_RESULT, state.DRIVE_CYCLE))
    clearing_result = {}
    for k, v in result["result"].items():
        clearing_result[f"alt_{k}"] = v
    result["result"].update(clearing_result)
    return result


def setup_alternate_model(new_params):
    base_vehicle = state.BASE_VEHICLE.copy()
    model_setup.setup_scenario_vehicle(base_vehicle, new_params)
    print("****", state.ALT_VEHICLE)
    state.ALT_RESULT = run.single_pass(
        state.GLOBAL_PARAMS, state.ALT_VEHICLE, state.DRIVE_CYCLE
    )
    result = {}
    result.update(
        run.extract_efficiencies(state.ALT_RESULT, state.DRIVE_CYCLE, prefix="alt_")
    )
    return result


def run_model(global_params, vehicles, drive_cycle, output_result=False):
    print(global_params, vehicles, drive_cycle)
    run.run(global_params, vehicles, drive_cycle, output_result=output_result)


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


def flatten_vehicle_dict(vehicle, base_key=""):
    result = {}
    for k, v in vehicle.items():
        if isinstance(v, dict):
            result.update(flatten_vehicle_dict(v, base_key=f"{k}_"))
        else:
            result[f'{base_key}{k}'] = v
    return result


def inflate_vehicle_dict(vehicle):
    result = defaultdict(dict)
    for k, v in vehicle.items():
        components = k.lsplit("_", 1)
        result[components[0]][components[1]] = v
    return result
