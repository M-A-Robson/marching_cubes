from typing import List, Optional, Tuple
import numpy as np
from utils import *


def get_offset(v1:float,v2:float, surface:float = 0.0) -> float:
    ''' finds the approximate point of intersection of the surface
        between two points with the values v1 and v2 '''
    delta = v2 - v1
    if delta == 0:
        return surface
    else:
        return (surface - v1) / delta


def march(x:float, y:float, z:float, cube:List[float], vertices:Optional[List] = None, triangles:Optional[List] = None):
    ''' Performs the Marching Cubes algorithm on a single cube '''
    edge_vertex = np.zeros((12,3))

    #Find which vertices are inside of the surface and which are outside, represented as integer
    flagIndex = np.sum(2**np.argwhere(np.asarray(cube)<=0))

    #Find which edges are intersected by the surface
    edgeFlags = CUBE_EDGE_FLAGS[flagIndex]

    #If the cube is entirely inside or outside of the surface, then there will be no intersections
    if (edgeFlags == 0): return vertices, triangles

    #Find the point of intersection of the surface with each edge
    for i in range(12):
        #if there is an intersection on this edge
        data = bin(edgeFlags)[:2] # turn edgeFlags int into binary string e.g. 255 --> '11111111'
        val = '0'*(12-len(data))+data # force minimum 12 digit data by adding leading zeros otherwise will get out of range error in next line
        if val[::-1][i] != 0: # TODO not sure on bit ordering here [::-1] reverses data so '0001' becomes '1000'
        #if val[i] != 0:
            offset = get_offset(cube[EDGE_CONNECTION[i][0]], cube[EDGE_CONNECTION[i][1]])
            # original code seperated x,y,z
            # edge_vertex[i][0] = x + (VERTEX_OFFSET[EDGE_CONNECTION[i][0]][0] + offset * EDGE_DIRECTION[i][0])
            # edge_vertex[i][1] = y + (VERTEX_OFFSET[EDGE_CONNECTION[i][0]][1] + offset * EDGE_DIRECTION[i][1])
            # edge_vertex[i][2] = z + (VERTEX_OFFSET[EDGE_CONNECTION[i][0]][2] + offset * EDGE_DIRECTION[i][2])
            # numpy to vectorise
            edge_vertex[i] = np.asarray([x,y,z]) + np.asarray(VERTEX_OFFSET[EDGE_CONNECTION[i][0]]) + offset*np.asarray(EDGE_DIRECTION[i])
    
    #Save the triangles that were found. There can be up to five per cube
    for i in range(5):
        if (TRIANGLE_CONNECTION_TABLE[flagIndex][3 * i] < 0): 
            return vertices, triangles
        idx = len(vertices)
        for j in range(3):
            vert = TRIANGLE_CONNECTION_TABLE[flagIndex][3 * i + j]
            triangles.append(idx + WINDING_ORDER[j])
            vertices.append(edge_vertex[vert])
    
    return vertices, triangles

def marching_cubes(voxels:np.ndarray) -> Tuple[np.ndarray,np.ndarray]:
    """performs marching cubes surface generation on a distance function

    Args:
        voxels (np.ndarray): shape(nx,ny,nz) voxel array
        where >= 0 is inside surface and < 0 outside surface

    Returns:
        Tuple[np.ndarray,np.ndarray]: vertices (n,3) and triangle (m,3) lists
    """
    verts = []
    triangles = []
    w,h,d = voxels.shape
    for x in range(w-1):
        for y in range(h-1):
            for z in range(d-1):
                cube = [1.0]*8
                for i in range(8):
                    ix = x + VERTEX_OFFSET[i][0]
                    iy = y + VERTEX_OFFSET[i][1]
                    iz = z + VERTEX_OFFSET[i][2]
                    cube[i] = voxels[ix, iy, iz]
                march(x, y, z, cube, verts, triangles)
    
    return np.asarray(verts), np.asarray([triangles]).reshape((-1,3))
