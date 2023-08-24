import os, csv
import pandas as pd
import numpy as np
from fastdtw import fastdtw
import scipy.stats as stats

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

def network_regression(field):
	"Computes regression analysis for multiple metrics for a given field"
	l_tuple_metrics = [('modularity', 'average cosine sim of neighbors'), ('modularity', 'cosine_sim_homophily'), 
			   ('average cosine sim of neighbors', 'cosine_sim_homophily')]
	df = pd.read_csv(f'{field}_CA_stats_over_time.csv')
	with open(f'CA_{field}_regression.csv','w') as temp_csv:
		writer=csv.writer(temp_csv, delimiter=',',lineterminator='\n')
		writer.writerow(['metric_tuple', 'slope', 'intercept', 'R_squared', 'pval'])
		for metric1, metric2 in l_tuple_metrics:
			x = np.array(df[metric1])
			y = np.array(df[metric2])

			slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
			r_squared = r_value ** 2
			writer.writerow([f"{metric1}, {metric2}", slope, intercept, r_squared, p_value])
