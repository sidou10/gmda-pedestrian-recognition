#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script compute the persistence diagrams from the pedestrian points 
clouds.
"""
import numpy as np
import argparse
import pickle
import gudhi
import sys
import os

sys.path.append("/Users/sidou/Desktop/gmda/gudhi/build/cython/")

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
    diag = simplex_tree.persistence(homology_coeff_field=2, min_persistence=min_persistence)
    return diag

def persistence_output_to_diag(persistence_output, dimension):
    """Change the ouput of the gudhi persistence function and keep only a 
    specific dimension (e.g. 0 or 1).
    
    Parameters
    ----------
    persistence_output : list(tuple)
    dimension : int
    
    Returns
    -------
    list(list)
    """
    return [[a,b] for (dim,(a,b)) in persistence_output if dim==dimension]

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dim", help="dimension of the persistence diagrams", 
                        type=int, required=True, choices=[0, 1])
    parser.add_argument("--raw-data", help="path containing the data file", 
                        required=True)
    parser.add_argument("--save", help="path of the directory where to save the \
                        persistence diagrams as a numpy array")  
    args = parser.parse_args()

    path_data = args.raw_data
    path_to_save = args.save
    dimension = args.dim

    # Import data in the correct form
    with open(path_data,"rb") as f:
        data = pickle.load(f, encoding="latin1")

    data_A = np.array(data[0])
    data_B = np.array(data[1])
    data_C = np.array(data[2])

    data_all = np.concatenate([data_A, data_B, data_C])
    
    # Compute the persistence diagrams
    nb_individuals = data_all.shape[0]

    diags = []

    for i in range(1, nb_individuals):
        diag = persistence_output_to_diag(alpha_persistence_from_point_cloud(
                                          data_all[i]), dimension=dimension)
        diags.append(diag)

    diags = np.array(diags)

    # Save the persistence diagrams to .npy
    np.save(os.path.join(path_to_save, "persistence_diagrams_{}dim.npy"\
                         .format(dimension)), diags)