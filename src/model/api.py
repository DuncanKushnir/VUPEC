import os
import matplotlib.pyplot as plt

from model import state, data, model_setup

from util.locations import GUI_STATIC_DIR


def get_manufacturer_list():
    return ["generic", "volvo"]

def setup_model(manufacturer, model, drivecycle):
    state.MANUFACTURER = manufacturer
    state.MODEL = model
    state.DRIVE_CYCLE = drivecycle
    if manufacturer == 'generic':
        return {'data': {'mass' : 1644,
                         'coeff_drag': 0.3,
                         'cross_section': 2.5,
                         'coeff_rr': 0.100}}
    return {'data': {'mass': 1344,
                     'coeff_drag': 0.32,
                     'cross_section': 2.7,
                     'coeff_rr': 0.090}}


def get_model_list(manufacturer):
    if manufacturer == "generic":
        return ["generic", "generic_suv"]
    return ["c70", "c80", "v70", "v60"]


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
