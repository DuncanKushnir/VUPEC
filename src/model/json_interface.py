"""
This file handles incoming json requests, parsing them and calling the model
where appropriate

Currently not included until interface stabilizes from this de-integration process
"""
from functools import wraps
from datetime import datetime
import time


def log_exec_time(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = datetime.utcnow()
        result = f(*args, **kwargs)
        end = datetime.utcnow()
        print("Elapsed time|{}|{}".format(f.__name__, end - start))
        return result

    return wrapper


@log_exec_time
def function():
    time.sleep(4)
    return "hoo"


function()
