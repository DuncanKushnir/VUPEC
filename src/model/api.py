import os
import matplotlib.pyplot as plt

import model.data

from util.locations import GUI_STATIC_DIR


def get_manufacturer_list():
    return ["generic", "volvo"]


def get_model_list(manufacturer):
    if manufacturer == "generic":
        return ["generic", "generic_suv"]
    return ["c70", "c80", "v70", "v60"]


def get_drivecycle_list():
    return model.data.data["drive_cycles"].keys()


def update_drivecycle_image(drive_cycle_df, dc_name):
    image_path = os.path.join(GUI_STATIC_DIR, f'{dc_name}.png')
    if not os.path.exists(image_path):
        print('regen', image_path)
        drive_cycle_df.plot(x='start_time', y='start_v')
        plt.margins(0)
        plt.savefig(image_path)


def change_drivecycle(drive_cycle_name):
    drive_cycle = model.data.data["drive_cycles"][drive_cycle_name]
    dc_df = drive_cycle.to_df()
    update_drivecycle_image(dc_df, drive_cycle_name)
