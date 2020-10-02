import json
from flask import current_app as app

from model import api


@app.route("/data/models_by_manufacturer/<manufacturer>")
def get_models(manufacturer):
    model_array = api.get_model_list(manufacturer)
    model_array = [{"id": f"{val}"} for val in model_array]
    return json.dumps(model_array)
