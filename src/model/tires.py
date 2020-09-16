import re
import math

import model.constants
import model.physics as physics

SIDEWALL_MASS = {"P": 123, "T": 123, "LT": 240}

TREAD_MASS = {"P": 123, "T": 123, "LT": 240}


def parse_tire_string(string="255/65 R16"):
    """
    :param string: a tire spec, e.g P255/65R16
    :return:
    """
    string = string.lower()
    result = {}
    try:
        measurement_spec = "us"
        drop_load_index = string.split("r")[0].strip()
        if drop_load_index.startswith("lt"):
            tire_spec = "lt"
        elif drop_load_index[0].isnumeric():
            measurement_spec = "eu"
            tire_spec = ""
        else:
            tire_spec = drop_load_index[0]
        size_spec = drop_load_index[len(tire_spec) :]

        diameter_str = string.split("r")[1].split()[0].strip()
        hub_diameter_m = float(diameter_str) * model.constants.METER_INCH

        width = float(size_spec.split("/")[0]) / 1000
        ratio = float(size_spec.split("/")[1]) / 100
        thickness = width * ratio
        diameter = hub_diameter_m + thickness * 2

        result = {
            "radius": diameter / 2,
            "diameter": diameter,
            "circumference": math.pi * diameter,
            "width": width,
            "spec": tire_spec,
            "ratio": ratio,
            "hub_diameter": hub_diameter_m,
            "sidewall": thickness,
            "name": string,
            "sidewall_area": math.pi
            * ((diameter / 2) ** 2 - (hub_diameter_m / 2) ** 2),
            "tread_area": width * math.pi * diameter,
            "measurement_spec": measurement_spec,
        }
        mass_tread = 19.8028 * result["tread_area"]
        mass_sidewall = 13.63 * result["sidewall_area"]
        result["est_mass"] = mass_tread + mass_sidewall
        result["moment"] = physics.rotational_moment(
            mass_sidewall, hub_diameter_m / 2 + result["sidewall"] / 2
        ) + physics.rotational_moment(mass_tread, diameter)
    except:
        raise
        raise ValueError(f"The tire string {string} could not be parsed")
    return result
