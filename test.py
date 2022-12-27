from marching_cubes import marching_cubes
import open3d as o3d
import numpy as np
import time

def main():
    '''test with a small array and visualise using open3d'''
    
    a = np.zeros((9,9,9))
    a[3:6,3:6,1:7] = 1
    
    t0 = time.perf_counter()
    v,t = marching_cubes(a)
    print(f'{time.perf_counter()-t0} secs')  
    
    m = o3d.geometry.TriangleMesh()
    m.vertices = o3d.utility.Vector3dVector(v)
    m.triangles = o3d.utility.Vector3iVector(t)
    
    m.compute_vertex_normals()
    m.compute_triangle_normals()
    o3d.visualization.draw_geometries([m])
    

if __name__ =="__main__":
    main()