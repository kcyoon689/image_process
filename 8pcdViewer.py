import sys
import open3d as o3d

if __name__ == "__main__":
  if len(sys.argv) == 2:
    pc_file = sys.argv[1]
    pcd = o3d.io.read_point_cloud(pc_file)
    o3d.visualization.draw_geometries([pcd])
  else:
    print("usage: python3 8pcdViewer.py <point_cloud_file>")
