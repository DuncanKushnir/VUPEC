import model.data


def get_manufacturer_list():
    return ["generic", "volvo"]


def get_model_list(manufacturer):
    if manufacturer == "generic":
        return ["generic", "generic_suv"]
    return ["c70", "c80", "v70", "v60"]


def get_drivecycle_list():
    return model.data.data["drive_cycles"].keys()
