"""Form class declaration."""
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired

from model import api


class SetupSubForm(FlaskForm):

    manufacturer = SelectField(
        "Manufacturer", choices=api.get_manufacturer_list(), id="manufacturer",
    )

    model = SelectField("Model", id="model")
    drivecycle = SelectField(
        "Drive Cycle",
        choices=api.get_drivecycle_list(),
        id="drivecycle",
        default="wltp-3b",
    )


class PhysicalSubForm(FlaskForm):
    mass = FloatField("Vehicle Mass", id="mass")
    coeff_drag = FloatField("Drag Coefficient", id="coeff_drag")
    cross_section = FloatField("Cross Section", id="cross_section")
    coeff_rr = FloatField("Rolling Res. Coefficient", id="coeff_rr")
    mass_base = None
    mass_unit = "kg"
    coeff_drag_base = None
    coeff_drag_unit = ""
    coeff_rr_base = None
    coeff_rr_unit = ""
    cross_section_base = None
    cross_section_unit = "m2"


class DrivetrainSubForm(FlaskForm):
    fuel = FloatField("Fuel Type", id="fuel")


class AccessorySubForm(FlaskForm):
    base = FloatField("Accessory Power", id="accessory_base")
    base_base = None
    base_unit = "W"


class BatterySubForm(FlaskForm):
    capacity = FloatField("Battery Capacity", id="batt_cap")
    capacity_base = None
    capacity_unit = "kWh"


class ResultSubForm(FlaskForm):
    submit_ab = SubmitField("Export as an A/B comparison")
    submit_sens = SubmitField("Export Sensitivity Analysis")
