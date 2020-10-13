MOCK_DRIVETRAIN = {
    "final_ratio": 4.71,
    "drive_n": 2,
    "eff_diff": 0.98,
    "parallel": False,
}

MOCK_TIRES = {"size": "P255/65R16"}

MOCK_ACCESSORIES = {"base": 100}

MOCK_BATTERY = {}


def mock_data(manufacturer, model):
    if manufacturer == "generic":
        if model == "generic":
            result = {
                "data": {
                    "physical": {
                        "mass": 1644,
                        "coeff_drag": 0.3,
                        "cross_section": 2.4,
                        "coeff_rr": 0.100,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": MOCK_BATTERY,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

        elif model == "generic_suv":
            result = {
                "data": {
                    "physical": {
                        "mass": 2200,
                        "coeff_drag": 0.34,
                        "cross_section": 3.1,
                        "coeff_rr": 0.100,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": MOCK_BATTERY,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

    elif manufacturer == "volvo":
        if model == "s60":
            result = {
                "data": {
                    "physical": {
                        "mass": 1600,
                        "coeff_drag": 0.27,
                        "cross_section": 2.22,
                        "coeff_rr": 0.090,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": MOCK_BATTERY,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

        elif model == "s60_twen":
            result = {
                "data": {
                    "physical": {
                        "mass": 1950,
                        "coeff_drag": 0.27,
                        "cross_section": 2.22,
                        "coeff_rr": 0.090,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": {"capacity": 11.6},
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

        elif model == "s90":
            result = {
                "data": {
                    "physical": {
                        "mass": 1700,
                        "coeff_drag": 0.26,
                        "cross_section": 2.29,
                        "coeff_rr": 0.090,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": MOCK_BATTERY,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

        elif model == "s90_twen":
            result = {
                "data": {
                    "physical": {
                        "mass": 2000,
                        "coeff_drag": 0.26,
                        "cross_section": 2.29,
                        "coeff_rr": 0.090,
                    },
                    "accessory": MOCK_ACCESSORIES,
                    "battery": {"capacity": 11.6},
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                }
            }

    return result
