"""Form class declaration."""
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

from model import api

class SetupSubForm(FlaskForm):

    manufacturer = SelectField(
        "Manufacturer",
        choices=api.get_manufacturer_list(),
        id="manufacturer",
    )

    model = SelectField("Model", id="model")
    drivecycle = SelectField(
        "Drive Cycle",
        choices=api.get_drivecycle_list(),
        id="drivecycle",
    )


class PhysicalSubForm(FlaskForm):
    mass = FloatField("Vehicle Mass", id="mass")
    coeff_drag = FloatField("Drag Coefficient", id="coeff_drag")
    cross_section = FloatField("Cross Section", id="cross_section")
    coeff_rr = FloatField("Rolling Resistance Coefficient", id="coeff_rr")

class DrivetrainSubForm(FlaskForm):
    fuel = FloatField("Fuel Type", id="fuel")

class ResultSubForm(FlaskForm):
    submit_ab = SubmitField("Export as an A/B comparison")
    submit_sens = SubmitField("Export Sensitivity Analysis")
