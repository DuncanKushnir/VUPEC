"""
Organizes and calculates the conversion of various energy types between different
locations in the drive train
"""


def source_energy(global_params, vehicle, model_df):
    """
    Determines where the energy to drive the wheel will come from
    """
    wheel_energy_required_mask = model_df["energy_wheel"] > 0
    energy_wheel = model_df.loc[wheel_energy_required_mask, "energy_wheel"]

    if not vehicle.battery:
        pass

    return model_df


def sink_energy(global_params, vehicle, model_df):
    """
    Determines how the excess wheel energy will be sunk
    """
    wheel_energy_required_mask = model_df["energy_wheel"] < 0
    energy_wheel = model_df.loc[wheel_energy_required_mask, "energy_wheel"]

    if not vehicle.battery:
        pass

    else:
        # In this case, we are dealing with a vehicle that can not regen brake
        pass

    # Now that we know the true demand on the brakes, we apply it.
    model_df["loss_friction_brake"] = energy_wheel * -1
    return model_df


def idle(global_params, vehicle, model_df):
    """
    Determines idling behaviour
    """
    wheel_energy_required_mask = model_df["energy_wheel"] == 0
    energy_wheel = model_df.loc[wheel_energy_required_mask, "energy_wheel"]
    if vehicle:
        pass

    return model_df


def from_wheels_to_driveshaft(global_params, vehicle, model_df):
    model_df["torque_driveshaft"] = (
        model_df["torque_wheel"]
        * vehicle.drivetrain.drive_n
        / vehicle.drivetrain.final_ratio
    )
    model_df["power_driveshaft"] = model_df["power_wheel"] / vehicle.drivetrain.eff_diff
    model_df["omega_driveshaft"] = model_df["omega_wheel"] / vehicle.drivetrain.eff_diff
    return model_df


def from_driveshaft_to_engine(global_params, vehicle, model_df):
    model_df["power_engine_driveshaft"] = model_df["power_driveshaft"] / 0.98
    model_df["energy_engine_driveshaft"] = (
        model_df["power_engine_driveshaft"] * model_df["duration"]
    )
    model_df["torque_engine_driveshaft"] = model_df["torque_driveshaft"] / 0.98
    return model_df


def allocate_demands(global_params, vehicle, model_df):
    """
    Determines the direction and magnitude of component energy flows
    """
    # First, we need to know if the engine is already loaded, e.g. driving the
    # alternator, running belt driven pumps, etc. This will be handled in the
    # pipeline with the accessory_demand function.

    model_df = source_energy(global_params, vehicle, model_df)
    model_df = sink_energy(global_params, vehicle, model_df)
    model_df = idle(global_params, vehicle, model_df)

    # The previous three functions operate on slices of model_df
    model_df = from_wheels_to_driveshaft(global_params, vehicle, model_df)
    model_df = from_driveshaft_to_engine(global_params, vehicle, model_df)
    model_df = allocate_torque(global_params, vehicle, model_df)

    # If not an electric, then accessory power comes from an alternator
    if not vehicle.battery:
        model_df["energy_engine_alternator"] = (
            model_df["electric_demand_accessory"] / vehicle.eff_alternator
        )

    model_df["energy_from_engine"] = (
        model_df[model_df["energy_engine_driveshaft"] > 0]["energy_engine_driveshaft"]
        + model_df["energy_engine_alternator"]
    )

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
