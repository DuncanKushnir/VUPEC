from flask import redirect
from flask import url_for
from flask import render_template
from flask import current_app as app

from collections import defaultdict

from gui.forms import (
    SetupSubForm,
    ResultSubForm,
    PhysicalSubForm,
    DrivetrainSubForm,
    BatterySubForm,
    AccessorySubForm,
)
from gui.data_routes import *

from model import api


@app.route("/", methods=(["GET", "POST"]))
def vehicle():
    setup_form = SetupSubForm(data=api.get_basic_state())
    result_form = ResultSubForm()
    physical_form = PhysicalSubForm()
    # drivetrain_form = DrivetrainSubForm()
    accessory_form = AccessorySubForm()
    battery_form = BatterySubForm()
    print(setup_form.manufacturer.data, setup_form.is_submitted())
    if setup_form.is_submitted():
        selected_manufacturer = setup_form.manufacturer.data
    else:
        selected_manufacturer = "generic"

    setup_form.model.choices = api.get_model_list(selected_manufacturer)

    return render_template(
        "basic_view.jinja2",
        setup_form=setup_form,
        result_form=result_form,
        physical_form=physical_form,
        accessory_form=accessory_form,
        battery_form=battery_form,
    )


@app.route("/success", methods=(["GET", "POST"]))
def success():
    return render_template("success.jinja2", template="success-template")


@app.route("/submit", methods=(["GET", "POST"]))
def submit():
    submitted_params = {}
    filtered_params = defaultdict(dict)
    setup_form = SetupSubForm()
    result_form = ResultSubForm()
    physical_form = PhysicalSubForm()
    accessory_form = AccessorySubForm()
    battery_form = BatterySubForm()

    submitted_params["setup"] = setup_form.data
    submitted_params["physical"] = physical_form.data
    submitted_params["battery"] = battery_form.data
    submitted_params["accessory"] = accessory_form.data
    for k, v in submitted_params.items():
        for key, val in v.items():
            if val and key != "csrf_token":
                filtered_params[k][key] = val

    run_params = api.model_setup.basic_setup_from_web_api(filtered_params)
    results = api.run_model(*run_params, output_result=True)
    return {"submitted_params": submitted_params, "filtered_params": filtered_params}


@app.route("/updatescenario", methods=(["GET", "POST"]))
def update():
    submitted_params = {}
    filtered_params = defaultdict(dict)
    setup_form = SetupSubForm()
    result_form = ResultSubForm()
    physical_form = PhysicalSubForm()
    accessory_form = AccessorySubForm()
    battery_form = BatterySubForm()

    submitted_params["setup"] = setup_form.data
    submitted_params["physical"] = physical_form.data
    submitted_params["battery"] = battery_form.data
    submitted_params["accessory"] = accessory_form.data
    for k, v in submitted_params.items():
        for key, val in v.items():
            if val and key != "csrf_token":
                filtered_params[k][key] = val
    response = {}
    print("***", filtered_params)
    if filtered_params:
        response = api.setup_alternate_model(filtered_params)

    return json.dumps(response)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "public, max-age=0"
    return response
