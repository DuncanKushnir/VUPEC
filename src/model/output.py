"""
Utilities for outputting data
"""
import pandas as pd

from util.locations import *


def output_model_run(global_parameters, result_dfs):
    output_stem = global_parameters["run_datetime"] + "_"

    output_data_filename = os.path.join(OUTPUT_DIR, output_stem + "data.xlsx")
    output_log_filename = os.path.join(OUTPUT_DIR, output_stem + "log.txt")
    output_cfg_filename = os.path.join(OUTPUT_DIR, output_stem + "setup.cfg")

    writer = pd.ExcelWriter(output_data_filename, engine="xlsxwriter")
    for result in result_dfs:
        result.to_excel(writer, sheet_name=str(result._output_name))
    writer.close()
