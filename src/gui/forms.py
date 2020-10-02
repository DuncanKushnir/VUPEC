"""Form class declaration."""
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

from model import api


class SetupForm(FlaskForm):
    """Sign up for a user account."""

    manufacturer = SelectField(
        "Manufacturer",
        [DataRequired()],
        choices=api.get_manufacturer_list(),
        id="manufacturer",
    )

    model = SelectField("Model", id="model")
    drivecycle = SelectField(
        "Drive Cycle",
        [DataRequired()],
        choices=api.get_drivecycle_list(),
        id="drivecycle",
    )

    submit = SubmitField("Output")


class PhysicalForm(FlaskForm):
    mass = FloatField("Vehicle Mass", [DataRequired()], id="mass")
    coeff_drag = FloatField("Drag Coefficient", [DataRequired()], id="coeff_drag")
    cross_section = FloatField("Cross Section", [DataRequired()], id="cross_section")

class DrivetrainForm(FlaskForm):
    fuel = FloatField("Fuel Type", [DataRequired()], id="fuel")

class ResultForm(FlaskForm):
    submit_ab = SubmitField("Export as an A/B comparison")
    submit_sens = SubmitField("Export Sensitivity Analysis")
