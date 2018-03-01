"""This script computes and saves as csv the bottleneck distances 
between every pair of persistance diagrams.
"""
import pandas as pd
import numpy as np
import argparse
import gudhi
import sys
import os

sys.path.append("/Users/sidou/Desktop/gmda/gudhi/build/cython/")

def save_pairwise_btnck_dist(dgms, save_path, dimension):
    """Computes the bottleneck distances between each pair of diagrams.
    
    Parameters
    ----------
    dgms : array
        Persistence diagrams.
    save_path : string
        Path of the directory where to save the .csv file containing pairwise 
        bottleneck distances.
    dimension : int
        Dimension of the persistence diagrams to consider.

    """
    # Number of observations
    nb_individuals = dgms.shape[0]

    # Initialisation of the matrix to save
    pairwise_btnck_dist = np.zeros((nb_individuals, nb_individuals))

    # Compute pairwise bottleneck distances between i and j
    for i in range(nb_individuals):
        diag_i = dgms[i]
        for j in range(i+1, nb_individuals):
            diag_j = dgms[j]
            bottleneck_dist = gudhi.bottleneck_distance(diag_i, diag_j)
            pairwise_btnck_dist[i][j] = bottleneck_dist
            pairwise_btnck_dist[j][i] = bottleneck_dist
    
    # Save as .csv under the name save
    name_file = os.path.join(save_path, "pairwise_btnck_dist_dim{}.csv"\
                             .format(dimension))
    pd.DataFrame(pairwise_btnck_dist).to_csv(name_file)
    print("Successfully saved in {}!".format(name_file))

if __name__ == '__main__':

	# Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--dgms', help="path containing the directory of the file \
                        with the persistence diagrams", required=True)
    parser.add_argument('--dim', help="dimension of the persistence diagrams", 
                        required=True, type=int, choices=[0, 1])
    parser.add_argument('--save', help="path containing the directory where to \
                        save a csv file", required=True)

    args = parser.parse_args()

    # Path of the .npy file of the persistence diagrams
    dgms_path = os.path.join(args.dgms, "persistence_diagrams_{}dim.npy"\
                             .format(dimension))

    # Load persistence diagrams
    dgms = np.load(dgms_path)

    # Save the file
    save_pairwise_btnck_dist(dgms, args.save, args.dim)
	