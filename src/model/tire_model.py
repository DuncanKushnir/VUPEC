from model.tires import parse_tire_string
import model.constants

import pandas as pd
import numpy as np

# From https://tiresize.com/tires/Kumho/Crugen-HP71-235-55R20.htm
# Spec, Mass
datapoints = [
    ("255/65R16", 31.8),
    ("255/65R16", 34.7),
    ("215/75R16", 29.3),
    ("215/75R16", 29.5),
    ("225/70R16", 32.34),
    ("225/70R16", 30),
    ("245/70R16", 33),
    ("275/60R18", 38),
    ("275/60R18", 41),
    ("275/60R18", 40),
    ("265/60R18", 39),
    ("265/60R18", 36),
    ("235/70R18", 33),
    ("235/55R20", 34),
    ("235/55R20", 32.8),
    ("255/65R19", 35),
    ("305/40R22", 44),
    ("305/40R22", 42),
    ("225/70R14", 22),
    ("225/70R14", 24),
    ("225/70R14", 33),
    ("245/65R17", 37.2),
    ("245/65R17", 31),
    ("225/75R17", 40),
    ("225/75R17", 41),
    ("225/75R17", 36),
    ("225/75R17", 40),
    ("265/60R17", 35.2),
    ("265/60R17", 35.1),
    ("265/60R17", 34.1),
    ("235/75R17", 33.9),
    ("235/75R17", 30),
    ("235/75R17", 33),
]

data = []
for d in datapoints:
    result = parse_tire_string(d[0])
    mass = d[1] / model.constants.KG_LB
    line = (result["sidewall_area"], result["tread_area"], mass)
    data.append(line)

A = pd.DataFrame(data, columns=["sidewall", "tread", "mass"])

X = A[["sidewall", "tread"]]
y = A["mass"]

import statsmodels.api as sm

model = sm.OLS(y, X).fit()
A["pred"] = model.predict(X)  # make the predictions by the model
print(A["pred"] / A["mass"])
print(model.summary())
