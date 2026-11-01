"""Features for the learned models: only what is known at the query minute (no peeking at the real arrival).

Target: the residual = real arrival - Passio's predicted time (seconds; positive = the bus came LATER than Passio said).
A model predicts the residual and its prediction is Passio's time + that residual, so it corrects what riders see
instead of replacing it.
"""
import numpy as np
import pandas as pd

NUMERIC = ["lead_passio", "lead_tt", "lead_ttd", "tt_minus_passio", "passio_age_s", "stops_away", "dist_m", "delay_s",
           "standing_s", "speed_mps", "last_age_s", "next_trip", "crosses_terminal", "visit_rank", "stop_index",
           "hour_sin", "hour_cos", "weekend"]
CATEGORICAL = ["route_id", "stop_key", "bin"]


def frame(s):
    """Feature table for a sample (DataFrame from dataset.sample). NaN stays NaN (models handle it)."""
    f = pd.DataFrame(index=s.index)
    q = s["query_epoch"]
    f["lead_passio"] = s["passio_epoch"] - q
    f["lead_tt"] = s["tt_epoch"] - q
    f["lead_ttd"] = s["ttd_epoch"] - q
    f["tt_minus_passio"] = s["tt_epoch"] - s["passio_epoch"]
    for c in ["passio_age_s", "stops_away", "dist_m", "delay_s", "standing_s", "speed_mps", "last_age_s", "next_trip",
              "crosses_terminal", "visit_rank", "stop_index"]:
        f[c] = s[c].astype(float)
    h = s["hour"].astype(float)
    f["hour_sin"], f["hour_cos"] = np.sin(2 * np.pi * h / 24), np.cos(2 * np.pi * h / 24)
    f["weekend"] = (s["day_type"] == "weekend").astype(float)
    f["route_id"] = s["route_id"].astype(str)
    f["stop_key"] = s["route_id"].astype(str) + ":" + s["stop_id"].astype(str)
    f["bin"] = s["bin"].astype(str)
    return f


def target(s):
    """Residual (s): real arrival minus Passio's predicted time."""
    return (s["actual_epoch"] - s["passio_epoch"]).to_numpy(float)
