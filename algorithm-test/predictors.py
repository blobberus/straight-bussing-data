"""Predictors under test. Each one: fit(train_sample) once per test day (only earlier days), then predict(test_sample)
-> predicted arrival epochs (np.ndarray, NaN = no prediction; the harness then falls back to Passio's time and counts
how often that happened)."""
import numpy as np


class Predictor:
    name = "base"

    def fit(self, train):
        return self

    def predict(self, test):
        raise NotImplementedError


class Passio(Predictor):
    """What riders see today: Passio's live prediction."""
    name = "passio"

    def predict(self, test):
        return test["passio_epoch"].to_numpy(float)


class Timetable(Predictor):
    """The printed timetable of the bus's trip (none on the Downtown Campus Connector's frequency trips)."""
    name = "timetable"

    def predict(self, test):
        return test["tt_epoch"].to_numpy(float)


class TimetableDelay(Predictor):
    """The timetable shifted by the bus's current delay at its last stop."""
    name = "timetable_delay"

    def predict(self, test):
        return test["ttd_epoch"].to_numpy(float)


REGISTRY = {p.name: p for p in (Passio, Timetable, TimetableDelay)}


def register(cls):
    REGISTRY[cls.name] = cls
    return cls
