def apply_motor_efficiencies(global_parameters, vehicle, model_df):
    model_df["input_thermal"] = model_df["energy_from_engine"] / 0.25
    model_df["input_petrol"] = model_df["input_thermal"] / 42000000
    return model_df
