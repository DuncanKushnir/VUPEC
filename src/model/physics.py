"""
Physics calculations and formulae
"""
import math

from model.constants import *


def air_density(pressure, temperature):
    """
    Calculate the air density at a given pressure and temperature.
    :param pressure: the pressure in Pascals
    :param temperature: temperature in Kelvin
    :return: The density in kg/m3
    """
    return pressure / (AIR_STD_GAS_CONST * temperature)


def air_pressure_at_altitude(
    altitude, base_pressure=AIR_STD_PRES, base_temp=AIR_TEMP_ISA
):
    """
    Calculate the pressure at a given altitude
    :param altitude: altitude, in meters above sea level
    :param base_pressure: pressure at sea level (Pascals)
    :return: the pressure at altitude
    """
    temp_a = AIR_STD_LAPSE * altitude / base_temp
    return ((1 + temp_a) ** AIR_ALT_EXP) * base_pressure


def air_density_alt_temp(altitude=0, temperature=AIR_TEMP_ISA):
    """
    Calculates the air density at a given altitude and observed temperature
    :param altitude:
    :param temperature:
    :return:
    """
    press = air_pressure_at_altitude(altitude, base_temp=temperature)
    return air_density(press, temperature)


def aerodynamic_drag_instant(v, A, cd, rho=AIR_DENS_ISA):
    """
    F = 1/2 * ? * v? * A * cd
    :param v: the force due to drag
    :param A: the cross sectional area
    :param cd: the coefficient of drag
    :param rho: the density of the fluid the object is moving through (1.225kg/m3 air)
    :return: Force in Newtons
    """
    force = (v ** 2) * A * cd * rho / 2
    return force


def aerodynamic_drag_average(vv, A, cd, rho=AIR_DENS_ISA):
    """
    F = 1/2 * ? * vv * A * cd
    :param vv: the average square of the velocity in meters/second
    :param A: the cross sectional area in meters squared
    :param cd: the coefficient of drag
    :param rho: the density of the fluid the object is moving through (1.225kg/m3 air)
    :return: Force in Newtons
    """
    force = vv * A * cd * rho / 2
    return force


def rolling_resistance_simple(vehicle_mass, crr=0.01):
    """
    F=C_rr * N
    :param crr: the dimensionless rolling resistance coefficient or coefficient of
        rolling friction

        0.0025               		Special Michelin solar car/eco-marathon tires
        0.0045 to 0.0080     		Large truck (Semi) tires
        0.0055               		Typical BMX bicycle tires used for solar cars
        0.0062 to 0.0150     		Car tire measurements
        0.0100 to 0.0150     		Ordinary car tires on concrete
        0.3000	                    Ordinary car tires on sand
    :param vehicle_mass: the mass of the vehicle in kg.
    :return: Force in Newtons
    """
    force = crr * vehicle_mass * EARTH_G
    return force


def rotational_energy(tire_moment, tire_d, v):
    """
    Calculates the rotational energy stored in a tire
    :param tire_moment: The tire moment of inertia
    :param tire_d: The diameter of the tire
    :param v: The velocity of the vehicle (m/s)
    :return: The energy in Joules stored as rotational kinetic energy
    """
    omega = 2 * v / tire_d
    return (omega ** 2) * tire_moment / 2


def rotational_moment(mass, r):
    """
    Calculates the rotational moment of a point mass at diameter r
    :param mass: mass in kg
    :param r: radius in meters
    :return: the moment
    """
    return mass * (r ** 2)


def grav_energy(vehicle_mass, altitude):
    """
    The gravitational potential energy at a given altitude
    :param vehicle_mass: the mass of the vehicle in kg
    :param altitude: the altitude above sea level (or any reference) in m
    :return: the potential energy in Joules
    """
    return vehicle_mass * altitude * EARTH_G


def kinetic_energy(vehicle_mass, v):
    """
    Calculates the rotational energy stored in a tire
    :param vehicle_mass: The tire moment of inertia
    :param v: The velocity of the vehicle (m/s)
    :return: The energy in Joules stored as rotational kinetic energy
    """
    return vehicle_mass * (v ** 2) / 2


def kinetic_energies(vehicle, v):
    tire_moment = vehicle.tires.moment
    tire_moment *= 4.0
    tire_kinetic = rotational_energy(tire_moment, vehicle.tires.diameter, v)
    vehicle_kinetic = kinetic_energy(vehicle.mass, v)
    return tire_kinetic + vehicle_kinetic


def add_external_physics(global_params, vehicle, model_df):
    """
    Calculate the external physics of the drive cycle
    :param global_params: a dictionary of global parameters
    :param vehicle: a vehicle.Vehicle object
    :param drive_cycle: a drive_cyles.DriveCycle object
    :param model_df: the dataframe with summary model information
    :return: the input model_df, modified in place
    """
    mass = vehicle.mass
    model_df["vehicle_mass"] = mass
    model_df["air_density"] = air_density_alt_temp(model_df["avg_alt"])
    model_df["loss_rolling"] = (
        rolling_resistance_simple(model_df["vehicle_mass"]) * model_df["delta_d"]
    )

    model_df["loss_drag"] = (
        aerodynamic_drag_average(model_df["avg_vv"], 2.5, 0.30, model_df["air_density"])
        * model_df["delta_d"]
    )
    model_df["kinetic_start"] = kinetic_energies(vehicle, model_df["start_v"])
    model_df["kinetic_end"] = kinetic_energies(vehicle, model_df["end_v"])
    model_df["kinetic_delta"] = model_df["kinetic_end"] - model_df["kinetic_start"]
    model_df["grav_delta"] = grav_energy(mass, model_df["delta_alt"])
    model_df["energy_wheel"] = (
        model_df["kinetic_delta"]
        + model_df["loss_drag"]
        + model_df["loss_rolling"]
        + model_df["grav_delta"]
    )

    model_df["power_wheel"] = model_df["energy_wheel"] / model_df["duration"]
    model_df["force_wheel"] = model_df["power_wheel"] / model_df["delta_d"]
    model_df["omega_wheel"] = model_df["avg_v"] / vehicle.tires.radius
    model_df["torque_wheel"] = model_df["power_wheel"] / (model_df["omega_wheel"] * 4)

    return model_df
