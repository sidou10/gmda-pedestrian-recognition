#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script compute the persistence diagrams from the pedestrian points 
clouds.
"""
import numpy as np
import argparse
import ghudi
import os

def alpha_persistence_from_point_cloud(point_cloud, min_persistence=0):
    """Compute the persistence diagram of the alpha shape filtration built on
    top of a 3D point cloud.
    
    Parameters
    ----------
    point_cloud : array, shape = [n_points, 3]
        3D point cloud.
    min_persistence : int, optional
        Minimum persistence value to take into account.
    
    Returns
    -------
    list(tuple)
        Persistence diagrams as a list of points and the corresponding 
        dimension [(dim, (a, b))].
    """
    alpha_complex = gudhi.AlphaComplex(points=point_cloud)
    simplex_tree = alpha_complex.create_simplex_tree(max_alpha_square=60.0)
    diag = simplex_tree.persistence(homology_coeff_field=2, 
                                    min_persistence=min_persistence)
    return diag

def persistence_output_to_diag(persistence_output, dimension):
    return [[a,b] for (dim,(a,b)) in persistence_output if dim==dimension]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dim", help="dimension of the persistence diagrams", required=True)
    parser.add_argument("--raw-data", help="path containing the raw data", required=True)
    parser.add_argument("--save", help="path where to save the persistence diagrams as a numpy array")  
    args = parser.parse_args()

    path_data = args.raw_data
    path_to_save = args.save
    dimension = args.dim

    # Import data in the correct form
    with open(os.path.join(path_data, "data_acc_rot.dat"),"rb") as f:
        data = pickle.load(f, encoding="latin1")

    data_A = np.array(data[0])
    data_B = np.array(data[1])
    data_C = np.array(data[2])

    data_all = np.concatenate([data_A, data_B, data_C])
    
    # Compute the persistence diagrams
    nb_individuals = data_all.shape[0]

    diags = persistence_output_to_diag(alpha_persistance_from_point_cloud(
                                       data_all[0]), dimension=dimension)
    for i in range(1, nb_individuals):
        diag = persistence_output_to_diag(alpha_persistance_from_point_cloud(
                                          data_all[i]), dimension=dimension)
        diags = np.stack(diags, diag)

    # Save the persistence diagrams to .npy
    np.save(os.path.join(path_data, "persistence_diagrams_{}dim.npy".format(dimension)), diags)