"""
Utilities for outputting data
"""

from util.locations import *


def output_model_run(global_parameters, model_df, drive_cycle):
    output_stem = global_parameters["run_datetime"] + "_"
    output_data = os.path.join(OUTPUT_DIR, output_stem + "data.csv")
    output_log = os.path.join(OUTPUT_DIR, output_stem + "log.txt")
    output_cfg = os.path.join(OUTPUT_DIR, output_stem + "setup.cfg")
    model_df.to_csv(output_data, index=False)