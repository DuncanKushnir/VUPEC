MOCK_DRIVETRAIN = {'final_ratio': 4.71,
                   'drive_n': 2,
                   'eff_diff': 0.98}

MOCK_TIRES = {'size': 'P255/65R16'}

def mock_data(manufacturer, model):
    if manufacturer == "generic":
        if model == "generic":
            result = {
                "data": {
                    "mass": 1644,
                    "coeff_drag": 0.3,
                    "cross_section": 2.4,
                    "coeff_rr": 0.100,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

        elif model == "generic_suv":
            result = {
                "data": {
                    "mass": 2200,
                    "coeff_drag": 0.34,
                    "cross_section": 3.1,
                    "coeff_rr": 0.100,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

    elif manufacturer == "volvo":
        if model == "s60":
            result = {
                "data": {
                    "mass": 1600,
                    "coeff_drag": 0.27,
                    "cross_section": 2.22,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

        elif model == "s60_twen":
            result = {
                "data": {
                    "mass": 1950,
                    "coeff_drag": 0.27,
                    "cross_section": 2.22,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": 11.6,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

        elif model == "s90":
            result = {
                "data": {
                    "mass": 1700,
                    "coeff_drag": 0.26,
                    "cross_section": 2.29,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": "None",
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

        elif model == "s90_twen":
            result = {
                "data": {
                    "mass": 2000,
                    "coeff_drag": 0.26,
                    "cross_section": 2.29,
                    "coeff_rr": 0.090,
                    "accessory_base": 100,
                    "batt_cap": 11.6,
                    "drivetrain": MOCK_DRIVETRAIN,
                    "tires": MOCK_TIRES,
                    "has_regen": False,
                }
            }

    return result


