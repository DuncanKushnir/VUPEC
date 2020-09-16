"""
Organizes and calculates the conversion of various energy types between different
locations in the drive train
"""


def allocate_demands(global_params, vehicle, model_df):

    model_df["torque_driveshaft"] = (
        model_df["torque_at_wheel"] / vehicle.drivetrain.final_ratio
    )
    model_df["power_driveshaft"] = (
        model_df["power_at_wheel"] / vehicle.drivetrain.eff_diff
    )
    model_df["omega_driveshaft"] = model_df["omega_wheel"] / vehicle.drivetrain.eff_diff

    model_df = allocate_torque(global_params, vehicle, model_df)

    return model_df


def allocate_torque(global_params, vehicle, model_df):
    torque_d = model_df["torque_driveshaft"]
    model_df["torque_brake"] = 0
    model_df["power_brake"] = 0
    if vehicle.has_regen:
        print("regin!")
    else:
        model_df["energy_at_brake"] = model_df[model_df["energy_at_wheel"] < 0][
            "energy_at_wheel"
        ]

    return model_df
