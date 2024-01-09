from typing import TYPE_CHECKING

import numpy as np
import open3d as o3d


if TYPE_CHECKING:
    from numpy.typing import NDArray


def expand_samples(samples, perpendicular, z_shift):
    """expand sample line to a cuboid"""
    new_samples = []
    for sample in samples:
        new_samples.append(sample - perpendicular - z_shift)
        new_samples.append(sample - perpendicular + z_shift)
        new_samples.append(sample + perpendicular - z_shift)
        new_samples.append(sample + perpendicular + z_shift)
    return new_samples


def sampling_line(start: "NDArray", end: "NDArray", distance: float):
    """sampling point from a line"""
    diff = end - start
    norm = np.linalg.norm(diff)
    direction = diff / norm
    perpendicular = np.asarray([-direction[1], direction[0], direction[2]])
    p_shift = perpendicular * distance / 2
    z_shift = np.asarray([0.0, 0.0, distance / 2])
    if norm <= distance:
        return expand_samples([start, end], p_shift, z_shift)
    samples = [start]
    for i in range(1, int(norm / distance) + 1):
        samples.append(start + i * direction * distance)
    samples.append(end)
    samples = expand_samples(samples, p_shift, z_shift)
    return samples


def sampling_model(lines, distance: float):
    """sampling the lines in the whole model"""
    samples = []
    for start, end in lines:
        samples.extend(sampling_line(start, end, distance))
    return np.asarray(samples)


def surface_reconstruct(points, alpha: float):
    from open3d.geometry import TriangleMesh

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    # o3d.visualization.draw_geometries([pcd])
    mesh = TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
    return mesh


def model_transfer(lines, distance: float, alpha: float):
    """Transfer line model into surface model"""
    points = sampling_model(lines, distance)
    mesh = surface_reconstruct(points, alpha)
    return mesh.vertices, mesh.triangles
