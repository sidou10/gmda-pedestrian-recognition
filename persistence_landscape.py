#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script computes the persistence landscapes.
"""
import numpy as np
import argparse
import os

def Lambda(t, b, d):
    """Triangle induced by the point p (b, d) in the new system
    of coordinates ((d+b)/2, (d-b)/2).
    
    Parameters
    ----------
    t : float
        Point to evaluate the Lambda function on.
    b : float
        x coordinate of the point in the original persistence diagram.
    d : float
        y coordinate of the point in the original persistence diagram.
    
    Returns
    -------
    float
        Value of the Lambda function (t).
    """
    b_new = (b+d)/2
    if b <= t <= b_new:
        return t-b
    elif b_new < t <= d:
        return d-t
    else:
        return 0

# Vectorized function to be able to apply it on a whole array
Lambda = np.vectorize(Lambda, otypes=[float])

def persistence_landscape(dgm, xmin, xmax, n_nodes, n_ld, plot_first=False):
    """Compute the persistence landscape on a given persistence diagram.
    
    Parameters
    ----------
    dgm : array, shape = [n_points, 2]
        Peristence diagram (e.g. 0 or 1 dimensional).
    xmin : float
        Left endpoint of the interval.
    xmax : float
        Right endpoint of the interval.
    n_nodes : int
        Number of nodes of a regular grid on the interval [xmin, xmax].
    n_ld : int
        Number of landscapes.
    plot_first : bool, optional
        If True, plot the first persistence landscape.
    
    Returns
    -------
    TYPE
        Description
    """
    # Number of points in the persistence diagram
    n_points = len(dgm)

    # Discretization for computing the persistence landscapes
    t = np.linspace(xmin, xmax, n_nodes)

    landscapes_by_point = np.zeros((n_points, n_nodes))

    for i in range(n_points):
        # Coordinates in the persistence diagram
        point = dgm[i]
        b = point[0]
        d = point[1]
        landscapes_by_point[i, :] = Lambda(t, b, d)
    
    # Sort the point in descending order
    landscapes = np.sort(landscapes_by_point, axis=0)[::-1]
    
    if plot_first:
        plt.scatter(t, landscapes[0,:])

    # Keep only the first n_ld landscapes
    landscapes = landscapes[:n_ld, :]

    return landscapes

def compute_landscape_features(dgms_path, xmin=0, xmax=0.4, n_nodes=200, n_ld=5):
    """Compute the landscape features from the pre-computed persistence diagrams.
    
    Parameters
    ----------
    dgms_path : str
        Path of the .npy file of the persistence diagrams.
    xmin : float
        Left endpoint of the interval.
    xmax : float
        Right endpoint of the interval.
    n_nodes : int
        Number of nodes of a regular grid on the interval [xmin, xmax].
    n_ld : int
        Number of landscapes.
    
    Returns
    -------
    array, shape = [n_observations, n_nodes]
        Persistence landscape observation matrix;
    """
    features = []

    dgms = np.load(dgms_path)

    for dgm in dgms:
        landscapes = persistence_landscape(dgm, xmin, xmax, n_nodes, n_ld).flatten()
        features.append(landscapes)

    return np.array(features)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dgms", help="path containing the directory of the file \
    	                with the persistence diagrams", required=True)
    parser.add_argument("--dim", help="dimension of the persistence diagrams", 
    	                type=int, choices=[0, 1])
    parser.add_argument("--save", help="path of the directory where to save the \
    	                persistence landscape observation matrix as a numpy array")
    parser.add_argument("--xmin", help="left endpoint of the interval", 
    	                type=float, default=0)
    parser.add_argument("--xmax", help="right endpoint of the interval", 
    	                type=float, default=0.4)
    parser.add_argument("--n-nodes", help="number of nodes of a regular grid on \
                        the interval [xmin, xmax]", type=int, default=200)
    parser.add_argument("--n-ld", help="number of landscapes", type=int, 
    	                default=5)

    args = parser.parse_args()
    dimension = args.dim
    dgms_path = os.path.join(args.dgms, "persistence_diagrams_{}dim.npy"\
                             .format(dimension))

    landscapes_features = compute_landscape_features(dgms_path, xmin=args.xmin, 
    	                                             xmax=args.xmax, 
    	                                             n_nodes=args.n_nodes, 
    	                                             n_ld=args.n_ld)

    np.save(os.path.join(args.save, "persistence_landscapes_{}dim.npy"\
                         .format(dimension)), landscapes_features)


