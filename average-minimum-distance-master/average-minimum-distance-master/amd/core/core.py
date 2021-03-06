# Contains core functions for AMD/PDD calculations.

from itertools import product, combinations
from collections import defaultdict
import numpy as np
from scipy.spatial import cKDTree

def _dist(p):
    return sum(x**2 for x in p)

def generate_integer_lattice(dims):
    """
    Generates batches of integer lattice points.
    
    Each yield gives all points (that have not already been yielded) 
    inside a sphere centered at the origin with radius d. d starts at 0 
    and increments by 1 on each loop. 
    
    Parameters
    ----------
    dims : int
        The dimension of Euclidean space the lattice is in.
        
    Yields
    -------
    ndarray 
        Yields arrays of integer points in dims dimensional Euclidean space.
    """
    
    ymax = defaultdict(int)
    d = 0
    
    while True:
        
        # get integer lattice points in +ve directions
        positive_int_lattice = []
        while True:
            batch = []
            for x in product(range(d+1), repeat=dims-1):
                pt = [*x, ymax[x]]
                if _dist(pt) <= d**2:
                    batch.append(pt)
                    ymax[x] += 1
            if not batch:
                break
            positive_int_lattice += batch
        positive_int_lattice.sort(key=_dist)

        # expand +ve integer lattice to full lattice with reflections
        int_lattice = []
        for p in positive_int_lattice:
            int_lattice.append(p)
            for n_reflections in range(1, dims+1):
                for indexes in combinations(range(dims), n_reflections):
                    if all((p[i] for i in indexes)):
                        p_ = list(p)
                        for i in indexes:
                            p_[i] *= -1
                        int_lattice.append(p_)
        
        yield np.array(int_lattice)
        d += 1

def generate_concentric_cloud(motif, cell):
    """
    Generates batches of points from a periodic set given by (motif, cell)
    which are roughly successively further away from the origin.
    
    Each yield gives all points (that have not already been yielded) which
    lie in a unit cell whose corner lattice point was generated by 
    _generate_integer_lattice(motif.shape[1]). 
    
    Parameters
    ----------
    motif : ndarray
        Cartesian representation of the motif, shape (no points, dims).
    cell : ndarray
        Cartesian representation of the unit cell, shape (dims, dims).
        
    Yields
    -------
    ndarray 
        Yields arrays of points from the periodic set.
    """
    
    lattice_generator = generate_integer_lattice(motif.shape[1])
    while True:
        lattice = next(lattice_generator) @ cell
        yield np.concatenate([motif + translation for translation in lattice])


def nearest_neighbours(motif, cell, k):
    """
    Given a periodic set represented by (motif, cell) and an integer k, find 
    the k nearest neighbours of the motif points in the periodic set.
    
    Note that cloud and inds are not used yet but may be in the future.
    
    Parameters
    ----------
    motif : ndarray
        Cartesian representation of the motif, shape (no points, dims).
    cell : ndarray
        Cartesian representation of the unit cell, shape (dims, dims).
    k : int
        Number of nearest neighbours to find for each motif point.
        
    Returns
    -------
    pdd : ndarray
        An array shape (motif.shape[0], k) of distances from each motif 
        point to its k nearest neighbours in order. Points do not count 
        as their own nearest neighbour. E.g. the distance to the n-th 
        nearest neighbour of the m-th motif point is pdd[m][n].
    cloud : ndarray 
        The collection of points in the periodic set that were generated
        during the nearest neighbour search.
    inds : ndarray
        An array shape (motif.shape[0], k) containing the indices of  
        nearest neighbours in cloud. E.g. the n-th nearest neighbour to 
        the m-th motif point is cloud[inds[m][n]].
    """
    
    cloud_generator = generate_concentric_cloud(motif, cell)
    
    n_points = 0
    cloud = []
    while n_points <= k:
        l = next(cloud_generator)
        n_points += l.shape[0]
        cloud.append(l)
    cloud.append(next(cloud_generator))
    cloud = np.concatenate(cloud)

    tree = cKDTree(cloud, compact_nodes=False, balanced_tree=False)
    pdd_, inds = tree.query(motif, k=k+1, workers=-1)
    pdd = np.zeros_like(pdd_)

    while not np.array_equal(pdd, pdd_):
        pdd = np.copy(pdd_)
        cloud = np.append(cloud, next(cloud_generator), axis=0)
        tree = cKDTree(cloud, compact_nodes=False, balanced_tree=False)
        pdd_, inds = tree.query(motif, k=k+1, workers=-1)

    return pdd_[:, 1:], cloud, inds[:, 1:]

if __name__ == '__main__':
    motif = np.array([[0,0,0],[0.1,0.1,0.1]])
    cell = np.identity(3)
    cloud, pdd, inds = nearest_neighbours(motif, cell, 10)
    print(pdd)