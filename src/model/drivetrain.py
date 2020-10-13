"""
Organizes and calculates the conversion of various energy types between different
locations in the drive train
"""
import math

from model.accessories import belt_connected_accessories


def source_energy(global_params, vehicle, model_df):
    """
    Determines where the energy to drive the wheel will come from
    """
    wheel_energy_required_mask = model_df["energy_wheel"] > 0
    model_df.loc[wheel_energy_required_mask, "energy_need_driveshaft"] = (
        model_df.loc[wheel_energy_required_mask, "energy_wheel"]
        / vehicle.drivetrain.eff_diff
    )

    model_df.loc[wheel_energy_required_mask, "energy_need_transmission"] = (
        model_df.loc[wheel_energy_required_mask, "energy_need_driveshaft"]
        / vehicle.drivetrain.eff_diff
    )

    if vehicle.battery.capacity and not vehicle.drivetrain.parallel:
        model_df.loc[
            wheel_energy_required_mask, "energy_need_electric_motor"
        ] = model_df.loc[wheel_energy_required_mask, "energy_need_transmission"]

        model_df["el_motor_instant_efficiency"] = 0.0
        model_df.loc[
            wheel_energy_required_mask, "el_motor_instant_efficiency"
        ] = vehicle.el_motor.obj.instant_efficiencies(
            model_df.loc[wheel_energy_required_mask, "torque_driveshaft"],
            model_df.loc[wheel_energy_required_mask, "omega_driveshaft_rpm"],
        )

        model_df.loc[wheel_energy_required_mask, "energy_need_battery"] = (
            model_df.loc[wheel_energy_required_mask, "energy_need_electric_motor"]
            / model_df.loc[wheel_energy_required_mask, "el_motor_instant_efficiency"]
        )

    else:
        model_df.loc[wheel_energy_required_mask, "energy_need_ff_motor"] = model_df.loc[
            wheel_energy_required_mask, "energy_need_transmission"
        ]

    return model_df


def sink_energy(global_params, vehicle, model_df):
    """
    Determines how the excess wheel energy will be sunk
    """
    wheel_energy_to_sink_mask = model_df["energy_wheel"] < 0
    model_df["energy_to_sink"] = 0.0
    model_df.loc[wheel_energy_to_sink_mask, "energy_to_sink"] = model_df.loc[
        wheel_energy_to_sink_mask, "energy_wheel"
    ]

    if not vehicle.battery:
        # First, energy needs of engine and accessories
        model_df["loss_friction_brake"] = (
            model_df["energy_to_sink"] + model_df["loss_friction_differential"]
        )

    else:
        # In this case, we are dealing with a vehicle that can regen brake
        model_df.loc[wheel_energy_to_sink_mask, "potential_regen_torque"] = (
            model_df.loc[wheel_energy_to_sink_mask, "torque_per_drive_wheel"]
            * vehicle.drivetrain.drive_n
            / vehicle.drivetrain.final_ratio
            * -1
            * vehicle.drivetrain.eff_diff
        )

        model_df["actual_regen_torque"] = model_df["potential_regen_torque"].apply(
            lambda row: max(min(row - 15, 100.0), 0.0)
        )

        model_df["energy_brake_to_engine"] = (
            model_df["actual_regen_torque"] * model_df["omega_driveshaft"]
        )

        model_df["energy_brake_to_battery"] = model_df["energy_brake_to_engine"] * 0.85

        model_df["loss_friction_brake"] = (
            model_df["energy_brake_to_battery"] + model_df["energy_to_sink"]
        )

        # Now that we know the true demand on the brakes, we apply it.
    return model_df


def idle(global_params, vehicle, model_df):
    """
    Determines idling behaviour
    """
    idle_mask = model_df["energy_wheel"] == 0
    model_df["energy_engine_idle"] = 0

    if not vehicle.battery:
        model_df.loc[idle_mask, "energy_engine_idle"] = 1000
        model_df.loc[idle_mask, "motor_rpm"] = 800

    model_df.fillna(0.0)
    return model_df


def account_startup_clutch(global_params, vehicle, model_df):
    model_df["clutch_slip"] = 1
    low_rpm_mask = model_df["motor_rpm"] < 200
    model_df.loc[low_rpm_mask, "clutch_slip"] = (
        model_df.loc[low_rpm_mask, "motor_rpm"] / 200
    )
    model_df.loc[low_rpm_mask, "motor_rpm"] = 200
    return model_df


def account_accel_ineff(global_params, vehicle, model_df):
    model_df["accel_eff"] = 1
    accel_mask = model_df["segment_type"] == "a"
    model_df.loc[accel_mask, "accel_eff"] = 1 / (
        model_df.loc[accel_mask, "acceleration"] / model_df.loc[accel_mask, "avg_v"] + 1
    )
    return model_df


def finish_ff_calculation(global_params, vehicle, model_df):

    model_df = belt_connected_accessories(global_params, vehicle, model_df)

    model_df["energy_from_ff_motor"] = (
        model_df["energy_need_ff_motor"]
        / (model_df["clutch_slip"] * model_df["accel_eff"])
        + model_df["energy_engine_idle"]
        + model_df["physical_demand_accessory"]
    )
    model_df["total_torque_motor"] = model_df["energy_from_ff_motor"] / (
        model_df["motor_rpm"] / 60 * 2 * math.pi
    )

    model_df["ff_motor_instant_efficiency"] = 0.0
    model_df["ff_motor_instant_efficiency"] = vehicle.ff_motor.obj.instant_efficiencies(
        model_df["total_torque_motor"], model_df["motor_rpm"]
    )

    model_df["thermal_input_ff_motor"] = (
        model_df["energy_from_ff_motor"] / model_df["ff_motor_instant_efficiency"]
    )
    model_df["loss_thermal_motor"] = (
        model_df["thermal_input_ff_motor"] - model_df["energy_from_ff_motor"]
    )

    return model_df


def add_constant_relations(global_params, vehicle, model_df):
    """
    Adds relationships that are always true
    """
    model_df["torque_per_drive_wheel"] = (
        model_df["torque_wheel_total"] / vehicle.drivetrain.drive_n
    )
    model_df["torque_driveshaft"] = (
        model_df["torque_wheel_total"] / vehicle.drivetrain.final_ratio
    )
    model_df["omega_driveshaft"] = (
        model_df["omega_wheel"] * vehicle.drivetrain.final_ratio
    )
    model_df["omega_driveshaft_rpm"] = model_df["omega_driveshaft"] * 60 / (2 * math.pi)
    model_df["loss_friction_differential"] = abs(model_df["energy_wheel"]) * (
        1 - vehicle.drivetrain.eff_diff
    )

    return model_df


def calculate_drivetrain_endpoints(global_params, vehicle, model_df):
    """
    Determines the direction and magnitude of component energy flows
    """
    # Because we operate on slices, we initialize columns
    model_df["energy_need_driveshaft"] = 0.0
    model_df["energy_need_transmission"] = 0.0
    model_df["energy_need_electric_motor"] = 0.0
    model_df["energy_need_ff_motor"] = 0.0
    model_df["energy_draw_battery"] = 0.0
    model_df["motor_rpm"] = model_df["omega_driveshaft_rpm"]

    # First, we need to know if the engine is already loaded, e.g. driving the
    # alternator, running belt driven pumps, etc. This will be handled in the
    # pipeline with the accessory_demand function.

    model_df = source_energy(global_params, vehicle, model_df)
    model_df = sink_energy(global_params, vehicle, model_df)
    model_df = idle(global_params, vehicle, model_df)

    model_df.fillna(0.0, inplace=True)

    model_df = account_startup_clutch(global_params, vehicle, model_df)
    model_df = account_accel_ineff(global_params, vehicle, model_df)
    model_df = finish_ff_calculation(global_params, vehicle, model_df)

    if vehicle.battery.capacity:
        model_df["energy_draw_inverter"] = (
            model_df["remaining_el_need_accessory"]
            + model_df["energy_need_battery"]
            + model_df["energy_brake_to_battery"] * -1
        )

    return model_df
