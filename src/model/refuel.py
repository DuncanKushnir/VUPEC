def apply_motor_efficiencies(global_parameters, vehicle, model_df):
    model_df["input_thermal"] = model_df["energy_need_ff_motor"] / 0.25
    model_df["input_petrol"] = model_df["input_thermal"] / 42000000
    model_df["el_input_total"] = 0.0
    if vehicle.battery:
        el_input, thermal_loss = vehicle.battery_obj.recharge_given_c(0.1)
        model_df["el_input_total"] = el_input

    return model_df
