"""Functions to create a new set of *C* vectors directed outwards from a cloud of *A* and *B* points and visualize the result."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% ../nbs/00_core.ipynb 4
from __future__ import annotations

import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull

# %% auto 0
__all__ = ['load_input_data', 'get_centroid', 'get_labeled_points', 'calculate_C_point', 'plot_convex_hull', 'plot_points',
           'plot_vectors', 'plot_ABC', 'calculate_C_points']

# %% ../nbs/00_core.ipynb 6
def load_input_data(
        path: str,      # path to data file
    ) -> pd.DataFrame:  
    "Load data from a txt file with headers [label, x, y, z] and values separated by spaces."
    
    df = pd.read_csv(path, delimiter=" ", names=["label", "x", "y", "z"])
    return df

# %% ../nbs/00_core.ipynb 14
def get_centroid(
        points: np.array, # xyz-coords of points
    ) -> np.array:        
    "Calculate centroid of point cloud."

    nps = points.shape[0]
    centroid = np.array([points[:,i].mean() for i in range(points.shape[1])])
    return centroid

# %% ../nbs/00_core.ipynb 18
def get_labeled_points(
        input_data: pd.DataFrame,  # points labels and xyz-coords
        label: str                 # label of subset of points
    ) -> np.array:              
    "Select subset of points by label."
    
    subset = input_data[input_data["label"]==label]
    return subset[["x", "y", "z"]].values

# %% ../nbs/00_core.ipynb 23
def calculate_C_point(
        B_point: np.array,     # B point
        centroid: np.array,    # centroid of point cloud
        distance: float=1.0    # prescribed distance D of the B->C vector
    ) -> np.array:
    "Given a point B, calculate a vector C originating from B and directed outwards from the point cloud, along the direction `centroid`-->`B_point`." 
    
    outwards_direction = (B_point - centroid) / np.linalg.norm(B_point - centroid)
    C_point = B_point + outwards_direction * distance
    return C_point

# %% ../nbs/00_core.ipynb 29
def plot_convex_hull(
        ax: Axes3D,
        points: np.array,       # xyz-coords of points
    ) -> Axes3D:
    "3D plot of convex hull."
    
    convex_hull = ConvexHull(points)
    for s in convex_hull.simplices:
        s = np.append(s, s[0])
        ax.plot(points[s, 0], points[s, 1], points[s, 2], "-", color="gray")
    return ax

# %% ../nbs/00_core.ipynb 31
def plot_points(
        ax: Axes3D,
        input_data: pd.DataFrame,     # labels and xyz-coords of points
    ) -> Axes3D:
    "3D plot of original points."
    
    for k in input_data["label"].unique():
        kps = get_labeled_points(input_data, k)
        ax.scatter(kps[:, 0], kps[:, 1], kps[:, 2], color=np.random.rand(3,), label=k)
    return ax

# %% ../nbs/00_core.ipynb 32
def plot_vectors(
        ax, 
        vectors: np.array,    # vector to plot
        origins: np.array,    # origin of vector
        length: float=0.3,    # vector length
    ):
    "Plot vectors as arrows."
    
    for origin, vector in zip(origins, vectors):
        x, y, z = origin
        dx, dy, dz = vector * length
        ax.quiver(x, y, z, dx, dy, dz, arrow_length_ratio=0.5)

    return ax

# %% ../nbs/00_core.ipynb 33
def plot_ABC(
        input_data: pd.DataFrame,     # labels and xyz-coords of points 
        C_points: np.array,           # calculated C points
        centroid: np.array            # centroid of point cloud    
    ) -> plt.figure:
    "Plot point cloud including its convex hull and the C vectors as arrows."
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    plot_points(ax, input_data)
    ax.scatter(centroid[0], centroid[1], centroid[2], marker="x", color="k", label="centroid")
    
    B_points = get_labeled_points(input_data, "B")
    plot_vectors(ax, C_points, B_points)
    plot_convex_hull(ax, input_data[["x", "y", "z"]].values)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.legend()
    
    return fig

# %% ../nbs/00_core.ipynb 36
def calculate_C_points(
        input_file: str,            # input file path with point A and B data
        output_file: str,           # output file path for the generated C points
        output_plot_file: str=None, # output file path for the plot of point cloud and C vectors
        distance: float=1.0,        # prescribed distance D of the B->C vectors
    ):
    "Calculate C points and export them to a file (together with the result plot, optionally)."

    print(f"Loading input data from '{input_file}'...")
    input_data = load_input_data(input_file)

    print("Calculate points...")
    centroid = get_centroid(input_data[["x", "y", "z"]].values)
    B_points = get_labeled_points(input_data, "B")
    C_points = np.apply_along_axis(lambda b_point: calculate_C_point(b_point, centroid, distance), 1, B_points)

    print(f"Saving result data to '{output_file}'...")
    np.savetxt(output_file, C_points)

    if output_plot_file:
        print(f"Exporting plots to '{output_plot_file}'...")
        fig = plot_ABC(input_data, C_points, centroid)
        fig.savefig(output_plot_file)

    print("Done.")