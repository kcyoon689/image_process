import os
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np
import open3d as o3d
import time
from tqdm import tqdm

class point_cloud_generator():
    def __init__(self, rgb_file, depth_file, pc_file, focal_length, scaleMin, scaleMax):
        self.rgb_file = rgb_file
        self.depth_file = depth_file
        self.pc_file = pc_file
        self.focal_length = focal_length * 80 # 120
        self.scaleMin = scaleMin
        self.scaleMax = scaleMax
        self.rgb = Image.open(rgb_file)
        self.depth = Image.open(depth_file).convert('I')
        self.width = self.rgb.size[0]
        self.height = self.rgb.size[1]

    def calculate(self):
        t1 = time.time()
        depth = np.asarray(self.depth).T
        self.Z = self.scaleMin + depth / 255.0 * (self.scaleMax - self.scaleMin)
        X = np.zeros((self.width, self.height))
        Y = np.zeros((self.width, self.height))

        for i in range(self.width):
            X[i, :] = np.full(X.shape[1], i)
        self.X = ((X - self.width / 2) * self.Z) / self.focal_length
        for i in range(self.height):
            Y[:, i] = np.full(Y.shape[0], i)
        self.Y = ((Y - self.height / 2) * self.Z) / self.focal_length

        df = np.zeros((6, self.width*self.height))
        df[0] = self.X.T.reshape(-1)
        df[1] = -self.Y.T.reshape(-1)
        df[2] = -self.Z.T.reshape(-1)
        img = np.array(self.rgb)
        df[3] = img[:, :, 0:1].reshape(-1)
        df[4] = img[:, :, 1:2].reshape(-1)
        df[5] = img[:, :, 2:3].reshape(-1)
        self.df = df
        t2 = time.time()
        # print('calcualte 3d point cloud Done.', t2-t1, 's')

    def write_ply(self):
        t1 = time.time()
        def float_formatter(x): return "%.4f" % x
        points = []
        for i in self.df.T:
            points.append("{} {} {} {} {} {} 0\n".format
                          (float_formatter(i[0]), float_formatter(i[1]), float_formatter(i[2]),
                           int(i[3]), int(i[4]), int(i[5])))

        file = open(self.pc_file, "w")
        file.write('''ply
        format ascii 1.0
        element vertex %d
        property float x
        property float y
        property float z
        property uchar red
        property uchar green
        property uchar blue
        property uchar alpha
        end_header
        %s
        ''' % (len(points), "".join(points)))
        file.close()

        t2 = time.time()
        # print("Write into .ply file Done.", t2-t1, 's')

    def show_point_cloud(self):
        pcd = o3d.io.read_point_cloud(self.pc_file)
        o3d.visualization.draw_geometries([pcd])

className_list = os.listdir('11depth_image')

for className in className_list:
    print('depth image to point cloud: ', className)

    inputPath = Path('11depth_image/' + className).absolute()
    imagePath = os.path.join(inputPath, 'img')
    depthPath = os.path.join(inputPath, 'depth')

    outputPath = Path('12point_cloud/' + className).absolute()
    os.makedirs(outputPath, exist_ok=True)

    imageFile_list = os.listdir(imagePath)
    imageFile_list.sort()

    for imageFile in tqdm(imageFile_list):
        if imageFile.endswith('.png'):
            rgb_file = os.path.join(imagePath, imageFile)
            depth_file = os.path.join(depthPath, imageFile)
            pc_file = os.path.join(outputPath, imageFile.replace('.png', '.ply'))
            focal_length = float(imageFile.split('_')[1])
            scaleMin = float(imageFile.split('_')[2])
            scaleMax = float(imageFile.split('_')[3])
            generator = point_cloud_generator(rgb_file, depth_file, pc_file, focal_length, scaleMin, scaleMax)
            generator.calculate()
            generator.write_ply()
            # generator.show_point_cloud()
