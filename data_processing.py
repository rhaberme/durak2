import pandas as pd
import numpy as np
from datetime import datetime


def unixtime_to_dt64(ut):
    if type(ut) == pd.Timestamp:
        return ut.to_numpy()
    else:
        ut = int(ut)
        dt = datetime.utcfromtimestamp(ut)
        return np.datetime64(dt)
