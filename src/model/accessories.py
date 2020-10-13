"""
Calculates power for accessory loads
"""
import model.physics as physics


def belt_connected_accessories(global_params, vehicle, model_df):
    """
    Add the accessory demands for belt connected accessories

    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param model_df: the model dataframe
    """
    if vehicle.battery and not vehicle.drivetrain.parallel:
        # Then, electrically driven pumps, etc.
        model_df["physical_demand_accessory"] = 0.0

    else:
        model_df["physical_demand_accessory"] = model_df['motor_rpm'] / 3

    return model_df


def electric_connected_accessories(global_params, vehicle, model_df):
    """
    Add the accessory demands for electrically driven accessories

    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param model_df: the model dataframe
    """
    static_accessories = vehicle.accessory.base * model_df["duration"]
    model_df["electric_demand_accessory"] = static_accessories

    # If not an electric, then accessory power comes from an alternator
    if not vehicle.battery:
        model_df["energy_engine_alternator"] = (
            model_df["electric_demand_accessory"] / 0.78
        )
        model_df["remaining_el_need_accessory"] = 0.0
    else:
        model_df["energy_engine_alternator"] = 0.0
        model_df["remaining_el_need_accessory"] = model_df["electric_demand_accessory"]

    return model_df


def add_accessory_demands(global_params, vehicle, model_df):
    """
    Add the accessory demands to the datafame inline

    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param drive_cycle: a drive_cyles.DriveCycle object
    :param model_df: the dataframe with summary model information
    :return: the input model_df, modified in place
    """
    model_df = electric_connected_accessories(global_params, vehicle, model_df)
    # This is calculated_later
    #model_df = belt_connected_accessories(global_params, vehicle, model_df)

    return model_df
