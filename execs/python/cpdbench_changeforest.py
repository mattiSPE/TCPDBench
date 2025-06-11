#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wrapper for ChangeForest in CPDBench-like structure.

Author: Mattis Pestinger
Date: 2025-06-06
"""

import argparse
import time
import numpy as np
import json
import pandas as pd

from changeforest import Control, changeforest

from cpdbench_utils import (
    load_dataset,
    make_param_dict,
    exit_with_error,
    exit_success,
    exit_with_timeout
)
from multiprocessing import Process, Manager

TIMEOUT = 60 * 30  # 30 minutes

def parse_args():
    parser = argparse.ArgumentParser(description="Wrapper for ChangeForest")
    parser.add_argument("-i", "--input", required=True, help="Path to input .json file")
    parser.add_argument("-o", "--output", help="Optional output path")
    parser.add_argument("--method", type=str, help="Search method in changeforest: knn, change_in_mean, random_forest", default="random_forest")
    parser.add_argument("--segmentation-type", type=str, help="Search strategy in changeforest: bs, wbs, sbs", default="bs")
    parser.add_argument("--n-estimators", type=int, help="Number of trees",default=100)
    parser.add_argument("--max-depth", help="Maximum tree depth", type=lambda x: int(x) if x != "None" else None, default=8)
    parser.add_argument("--feature_split", help="Feature selection per split (int or 'sqrt')", default="sqrt")
    parser.add_argument("--use-timeout", action="store_true")
    return parser.parse_args()

def wrapper(args, return_dict, **kwargs):
    detector = run_changeforest(*args, **kwargs)
    return_dict["detector"] = detector

def wrap_with_timeout(args, kwargs, limit):
    manager = Manager()
    return_dict = manager.dict()
    p = Process(target=wrapper, args=(args, return_dict), kwargs=kwargs)
    p.start()
    p.join(limit)
    if p.is_alive():
        p.terminate()
        return None, "timeout"
    return return_dict.get("detector", None), "success" if "detector" in return_dict else "fail"

def run_changeforest(mat: np.ndarray, params: dict):
    clf = changeforest(
        mat,
        params['method'],
        params['segmentation_type'],
        Control(
            random_forest_n_estimators=params['n_estimators'],
            random_forest_max_depth=params['max_depth'],
            random_forest_max_features=params['feature_split']
            )
    )
    detected = clf.split_points()
    return detected

def main():
    args = parse_args()
    data, mat = load_dataset(args.input)

    # Interpolieren von fehlenden Werten (NaNs), damit changeforest nicht crasht
    if np.isnan(mat).any():
        mat = pd.DataFrame(mat).interpolate(limit_direction="both").to_numpy()

    # Dynamische Featureanzahl basierend auf n_dim
    d = mat.shape[1]
    feature_split = int(np.sqrt(d)) if args.feature_split is None else args.feature_split

    defaults = {
        "feature_split": feature_split
    }

    parameters = make_param_dict(args, defaults)

    start_time = time.time()
    status = "fail"
    error = None

    #print("DEBUG(CONTROL):", vars(Control()))

    try:
        if args.use_timeout:
            detected, status = wrap_with_timeout((mat, parameters), {}, TIMEOUT)
        else:
            detected = run_changeforest(mat, parameters)
            status = "success"
    except Exception as err:
        error = repr(err)

    stop_time = time.time()
    runtime = stop_time - start_time

    if status == "timeout":
        exit_with_timeout(data, args, parameters, runtime, __file__)

    if error or status == "fail":
        exit_with_error(data, args, parameters, error, __file__)

    locations = [int(cp) for cp in detected]
    exit_success(data, args, parameters, locations, runtime, __file__)

if __name__ == "__main__":
    main()
