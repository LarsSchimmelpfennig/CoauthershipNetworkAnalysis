import os, csv
import pandas as pd
import numpy as np
from fastdtw import fastdtw

def normalized(array):
  "Takes an array and returns a normalized array with values from 0-1." 
	normalized_array = []
	for x in array:
		normalized_array.append((x-min(array))/(max(array)-min(array)))
	return normalized_array

def convert_numpy_format(array):
  """Takes an array and updates each value to contain a corresponding index. 
  Required with fastdtw() when dist=eulcidean"""
	updated = []
	for idx, val in enumerate(array):
		updated.append([idx, val])
	return updated

def calculate_dtw(curve1, curve2):
    "Takes two arrays and returns the fastdtw() distance between them."
    distance, _ = fastdtw(curve1, curve2, dist=euclidean)
    return distance

def permutation_test(curve1, curve2, n_permutations=10000):
    '''
    Returns significance value for the distance between two curves using a permutation test.

            Parameters:
                    curve1 (array): array of values
                    curve2 (array): array of values
                    n_permutations (int): number of iterations

            Returns:
                    p_value (float): significance value for observed distance between curves
    '''
    observed_distance = calculate_dtw(curve1, curve2)
    combined_curve = np.concatenate([curve1, curve2])
    permuted_distances = []
    for _ in range(n_permutations):
        np.random.shuffle(combined_curve)
        permuted_curve1 = combined_curve[:len(curve1)]
        permuted_curve2 = combined_curve[len(curve1):]
        permuted_distance = calculate_dtw(permuted_curve1, permuted_curve2)
        permuted_distances.append(permuted_distance)

    p_value = np.sum(np.array(permuted_distances) <= observed_distance) / n_permutations
    return p_value
