import os
import matplotlib.pyplot as plt

from model import state, data, model_setup

from util.locations import GUI_STATIC_DIR


def get_manufacturer_list():
    return ["generic", "volvo"]

def mock_data(manufacturer, model):
    if manufacturer == "generic":
        if model == "generic":
            result = {
                "data": {
                    "mass": 1644,
                    "coeff_drag": 0.3,
                    "cross_section": 2.4,
                    "coeff_rr": 0.100,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "tires": {'size': 'P255/65R16'},
                }
            }

        elif model == "generic_suv":
            result = {
                "data": {
                    "mass": 2200,
                    "coeff_drag": 0.34,
                    "cross_section": 3.1,
                    "coeff_rr": 0.100,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "tires": {'size': 'P255/65R16'},
                }
            }

    elif manufacturer == "volvo":
        if model == "s60":
            result = {
                "data": {
                    "mass": 1600,
                    "coeff_drag": 0.27,
                    "cross_section": 2.22,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "tires": {'size': 'P255/65R16'},
                }
            }

        elif model == "s60_twen":
            result = {
                "data": {
                    "mass": 1950,
                    "coeff_drag": 0.27,
                    "cross_section": 2.22,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": 11.6,
                    "tires": {'size': 'P255/65R16'},
                }
            }

        elif model == "s90":
            result = {
                "data": {
                    "mass": 1700,
                    "coeff_drag": 0.26,
                    "cross_section": 2.29,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "tires": {'size': 'P255/65R16'},
                }
            }

        elif model == "s90_twen":
            result = {
                "data": {
                    "mass": 2000,
                    "coeff_drag": 0.26,
                    "cross_section": 2.29,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": 11.6,
                    "tires": {'size': 'P255/65R16'},
                }
            }

    return result



def setup_model(manufacturer, model, drivecycle):
    state.MANUFACTURER = manufacturer
    state.MODEL = model
    state.DRIVE_CYCLE = drivecycle
    return mock_data(manufacturer, model)

def run_model(global_params, vehicles, drive_cycle):
    print(global_params,vehicles,drive_cycle)

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
