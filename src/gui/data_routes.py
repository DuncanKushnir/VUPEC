import json
from flask import current_app as app
from flask import url_for

from model import api


@app.route("/data/models_by_manufacturer/<manufacturer>")
def get_models(manufacturer):
    model_array = api.get_model_list(manufacturer)
    model_array = [{"id": f"{val}"} for val in model_array]
    return json.dumps(model_array)


@app.route("/data/vehicle_state")
def get_vehicle_state():
    pass

@app.route("/data/getbase/<manufacturer>/<model>/<drivecycle>")
def set_base_model(manufacturer, model, drivecycle):
    if model == 'generic' and manufacturer!= 'generic':
        model = api.get_model_list(manufacturer)[0]

    print('setbasemodel', manufacturer, model, drivecycle)
    default_params = api.setup_model(manufacturer, model, drivecycle)
    base_params = {'data': {key+'_base' : val for key, val in default_params[
        'data'].items()}}
    base_params['orig'] = default_params['data']

    return json.dumps(base_params)

@app.route("/data/dc/<drive_cycle>")
def update_drive_cycle(drive_cycle):
    api.change_drivecycle(drive_cycle)
    src = url_for("static", filename=f"{drive_cycle}.png")
    return json.dumps({"src": src})
