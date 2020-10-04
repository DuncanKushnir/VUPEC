from flask import redirect
from flask import url_for
from flask import render_template
from flask import current_app as app

from gui.forms import SetupForm, ResultForm, PhysicalForm, DrivetrainForm
from gui.data_routes import *

from model import api


@app.route("/", methods=(["GET", "POST"]))
def vehicle():
    setup_form = SetupForm()
    result_form = ResultForm()
    physical_form = PhysicalForm()
    drivetrain_form = DrivetrainForm()
    print(setup_form.manufacturer.data, setup_form.is_submitted())
    if setup_form.is_submitted():
        selected_manufacturer = setup_form.manufacturer.data
    else:
        selected_manufacturer = "generic"

    setup_form.model.choices = api.get_model_list(selected_manufacturer)

    return render_template(
        "forms.jinja2",
        setup_form=setup_form,
        result_form=result_form,
        physical_form=physical_form,
        drivetrain_form=drivetrain_form,
        template="setup_form-template",
    )


@app.route("/success", methods=(["GET", "POST"]))
def success():
    return render_template("success.jinja2", template="success-template")


@app.route("/export")
def export():
    pass

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
