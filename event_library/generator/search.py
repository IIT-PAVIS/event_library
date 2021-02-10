from typing import Any, Callable, Iterable

import numpy as np
from hyperopt import fmin, hp, space_eval, tpe
from tqdm import tqdm

from .simulator import SimulatorWrapper

__all__ = ['find_best_events_parameters']


def objective_variance(args):
    sim = SimulatorWrapper(**args)

    representation_gen = args['representation_gen']
    avg_variance = 0.0

    for input_dir in args['input_dirs']:
        sim.set_input_dir(input_dir)
        for events_batch in sim:
            for frame in representation_gen(events_batch):
                avg_variance += frame.var()

    return -avg_variance


def find_best_events_parameters(input_dirs: str, representation_gen):
    # TODO use hyperopt to find parameters that maximize avg variance

    space = {
        'input_dirs': input_dirs,
        'representation_gen': representation_gen,
        'Cp': hp.normal('Cp', 1, 1),
        'Cn': hp.normal('Cn', 1, 1),
        'refractory_period': hp.loguniform('ref', 1e-7, 1),
        'log_eps': hp.loguniform('log_eps', 1e-7, 1),
        'use_log': hp.choice('use_log', [True, False]),
    }
    best = fmin(objective_variance, space, algo=tpe.suggest, max_evals=50)
    return best
