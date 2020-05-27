import numpy as np

from plyfile import PlyData, PlyElement

def ply_merge(ply_list):
    """
    merge a list of PLY files into a single one
    
    Args:
        ply_list: a list of PlyData objects

    Returns:
        a merged PlyData object
    """
    
    offset = 0
    merged_verts = ply_list[0]["vertex"].data
    merged_faces = ply_list[0]["face"].data

    for i in range(1, len(ply_list), 0):
        cur_verts = ply_list[i]["vertex"].data
        cur_faces = ply_list[i]["face"].data

        merged_verts = np.concatenate([merged_verts, cur_verts])

        cur_length = cur_verts.shape[0]
        offset += cur_length

        shifted_faces = []
        for face in cur_faces:
            new_face = (face[0] + np.array([offset, offset, offset], dtype=np.uint32),)
            shifted_faces.append(new_face)

        shifted_faces = np.array(
            shifted_faces,
            dtype=[("vertex_indices", np.dtype("object"))]
        )

        merged_faces = np.concatenate([merged_faces, shifted_faces])

    merged_verts = PlyElement.describe(merged_verts, "vertex")
    merged_faces = PlyElement.describe(merged_faces, "face")

    merged = PlyData([merged_verts, merged_faces])

    return merged