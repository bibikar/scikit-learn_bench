# Copyright (C) 2017-2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

import argparse
from bench import parse_args, time_mean_min, print_header, print_row, size_str
import numpy as np
from sklearn.cluster import DBSCAN

parser = argparse.ArgumentParser(description='scikit-learn DBSCAN benchmark')
parser.add_argument('-x', '--filex', '--fileX', '--input', required=True,
                    type=str, help='Points to cluster')
parser.add_argument('-e', '--eps', '--epsilon', type=float, default=0.5,
                    help='Radius of neighborhood of a point')
parser.add_argument('-m', '--data-multiplier', default=100,
                    type=int, help='Data multiplier')
parser.add_argument('-M', '--min-samples', default=5, type=int,
                    help='The minimum number of samples required in a '
                    'neighborhood to consider a point a core point')
params = parse_args(parser, loop_types=('fit', 'predict'), n_jobs_supported=True)

# Load generated data
X = np.load(params.filex)
X_mult = np.vstack((X,) * params.data_multiplier)

# Create our clustering object
dbscan = DBSCAN(eps=params.eps, n_jobs=params.n_jobs,
                min_samples=params.min_samples, metric='euclidean',
                algorithm='auto')

# N.B. algorithm='auto' will select DAAL's brute force method when running
# daal4py-patched scikit-learn.

columns = ('batch', 'arch', 'prefix', 'function', 'threads', 'dtype', 'size',
           'n_clusters', 'time')
params.size = size_str(X.shape)
params.dtype = X.dtype
print_header(columns, params)

# Time fit
fit_time, _ = time_mean_min(dbscan.fit, X,
                            outer_loops=params.fit_outer_loops,
                            inner_loops=params.fit_inner_loops,
                            goal_outer_loops=params.fit_goal,
                            time_limit=params.fit_time_limit,
                            verbose=params.verbose)
params.n_clusters = len(dbscan.core_sample_indices_)
print_row(columns, params, function='DBSCAN.fit', time=fit_time)

# Time predict
predict_time, _ = time_mean_min(dbscan.fit_predict, X,
                                outer_loops=params.predict_outer_loops,
                                inner_loops=params.predict_inner_loops,
                                goal_outer_loops=params.predict_goal,
                                time_limit=params.predict_time_limit,
                                verbose=params.verbose)
print_row(columns, params, function='DBSCAN.fit_predict', time=predict_time)