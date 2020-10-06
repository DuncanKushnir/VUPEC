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

    return model_df


def electric_connected_accessories(global_params, vehicle, model_df):
    """
    Add the accessory demands for electrically driven accessories

    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param model_df: the model dataframe
    """
    static_accessories = vehicle.accessory_base * model_df["duration"]

    model_df["electric_demand_accessory"] = static_accessories

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
    model_df = belt_connected_accessories(global_params, vehicle, model_df)

    return model_df
