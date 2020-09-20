"""
Organizes and calculates the conversion of various energy types between different
locations in the drive train
"""

def from_wheels_to_driveshaft(global_params, vehicle, model_df):
    model_df["torque_driveshaft"] = (
        model_df["torque_wheel"] / vehicle.drivetrain.final_ratio
    )
    model_df["power_driveshaft"] = (
        model_df["power_wheel"] / vehicle.drivetrain.eff_diff
    )
    model_df["omega_driveshaft"] = model_df["omega_wheel"] / vehicle.drivetrain.eff_diff
    return model_df

def allocate_demands(global_params, vehicle, model_df):

    model_df = from_wheels_to_driveshaft(global_params, vehicle, model_df)
    model_df = allocate_torque(global_params, vehicle, model_df)

    # If not an electric, then accessory power comes from an alternator
    if not vehicle.battery:
        model_df['energy_engine_alternator'] = model_df['electric_demand_accessory'] \
                                               / vehicle.eff_alternator


    return model_df


def allocate_torque(global_params, vehicle, model_df):
    torque_d = model_df["torque_driveshaft"]
    model_df["torque_brake"] = 0
    model_df["power_brake"] = 0
    if vehicle.has_regen:
        print("regen!")
    else:
        model_df["loss_friction_brake"] = model_df[model_df["energy_wheel"] < 0][
            "energy_wheel"
        ]

    return model_df
