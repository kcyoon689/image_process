import json
import os
import sys
from pathlib import Path
import shutil

from shapely.geometry import Polygon, MultiPolygon  # (pip install Shapely)
from skimage import measure                        # (pip install scikit-image)
import numpy as np                                 # (pip install numpy)
from PIL import Image  # (pip install Pillow)
from tqdm import tqdm # (pip install tqdm)

def create_sub_masks(mask_image):
    width, height = mask_image.size

    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the values of the pixel
            pixel = mask_image.getpixel((x, y))

            # If the pixel is not black...
            if pixel != (255): # background : ignore_label
            # if pixel != (0): # background : ignore_label
                # Check to see if we've created a sub-mask...
                pixel_str = str(pixel)
                sub_mask = sub_masks.get(pixel_str)
                if sub_mask is None:
                   # Create a sub-mask (one bit per pixel) and add to the dictionary
                    # Note: we add 1 pixel of padding in each direction
                    # because the contours module doesn't handle cases
                    # where pixels bleed to the edge of the image
                    sub_masks[pixel_str] = Image.new('1', (width+2, height+2))

                # Set the pixel value to 1 (default is 0), accounting for padding
                sub_masks[pixel_str].putpixel((x+1, y+1), 1)

    return sub_masks


def create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    np_sub_mask = np.array(sub_mask)
    contours = measure.find_contours(np_sub_mask, 0.5, positive_orientation='low')
    contours = contours[0:1] # first element only

    segmentations = []
    polygons = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)
        polygons.append(poly)
        segmentation = np.array(poly.exterior.coords).ravel().tolist()
        segmentations.append(segmentation) # TODO:

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    x, y, max_x, max_y = multi_poly.bounds # TODO:
    width = max_x - x
    height = max_y - y
    bbox = (x, y, width, height)
    area = multi_poly.area # TODO:

    annotation_dict = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation_dict


if __name__ == "__main__":
    rootDirPath = Path('/home/crvl-yoon/detectoRS/output/').absolute()
    trainDirPath = os.path.join(rootDirPath, 'train')
    valDirPath = os.path.join(rootDirPath, 'val')
    testDirPath = os.path.join(rootDirPath, 'test')
    annotDirPath = os.path.join(rootDirPath, 'annotations')

    dataDirPathList = [trainDirPath, valDirPath, testDirPath]
    for dataDirPath in dataDirPathList:
        imageDirPath = os.path.join(dataDirPath, 'images')
        imageNameList = os.listdir(imageDirPath)
        imagePathList = [os.path.join(imageDirPath, imageName) for imageName in imageNameList]
        imagePathList.sort()

        maskDirPath = os.path.join(dataDirPath, 'masks')
        maskNameList = os.listdir(maskDirPath)
        maskPathList = [os.path.join(maskDirPath, maskName) for maskName in maskNameList]
        maskPathList.sort()

        # print(len(imageNameList))
        # print(len(maskNameList))
        # print(imageDirPath)
        # print(maskDirPath)
        # print(imagePathList[100:105])
        # print(maskPathList[100:105])
        # sys.exit() # stop!

        # imagePathList = [imagePathList[0], imagePathList[1]]
        # maskImageList = [Image.open(maskPathList[0]), Image.open(maskPathList[1])]
        # maskImageList = [Image.open(maskPath) for maskPath in maskPathList]

        # Define which colors match which categories in the images
        category_names_list = ['ashcan', 'beer_bottle', 'beer_can', 'bowl', 'camera', 'chair', 'clock', 'coke', 'faucet', 
        'football_helmet', 'guitar', 'jug', 'lamp', 'piano', 'pistol', 'pool_table', 'sofa']
        category_ids = {
        #   '(255, 255, 255)': category_names_list.index('table')+1,
        #   '(0, 255, 255)': category_names_list.index('chair')+1,
        #   '(255, 0, 255)': category_names_list.index('drawer')+1,
        # '0': category_names_list.index('table'), # 0
        # '1': category_names_list.index('chair'), # 1
        # '2': category_names_list.index('drawer'), # 2
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        '11': 11,
        '12': 12,
        '13': 13,
        '14': 14,
        '15': 15,
        '16': 16,
        '255': 255,
        }

        # Create the json_dict
        json_dict = {}

        # Create the info dict
        info_dict = {}
        info_dict['description'] = "kcyoon 2022 ShapeNet Dataset (" + os.path.split(dataDirPath)[-1] + ")"
        info_dict['url'] = ""
        info_dict['version'] = "1.0"
        info_dict['year'] = 2022
        info_dict['contributor'] = "chaeyoon kim"
        info_dict['date_created'] = "2022/01/15"
        json_dict['info'] = info_dict

        # Create the licenses_list
        licenses_list = []
        licenses_dict = {}
        licenses_dict['url'] = ""
        licenses_dict['id'] = 1
        licenses_dict['name'] = ""
        licenses_list = [licenses_dict]
        json_dict['licenses'] = licenses_list

        # Create the images_list
        images_list = []
        image_id = 1
        pbar = tqdm(imagePathList)
        for imagePath in pbar:
            pbar.set_description("images [" + os.path.split(imagePath)[-1] + "]")
            image_dict = {}
            image_dict['id'] = image_id
            image_dict['license'] = 1
            image_dict['coco_url'] = ""
            image_dict['flickr_url'] = ""
            image_dict['height'] = 480
            image_dict['width'] = 640
            image_dict['file_name'] = os.path.split(imagePath)[-1]
            image_dict['date_captured'] = "2022/01/15"
            images_list.append(image_dict)
            image_id += 1
        json_dict['images'] = images_list

        # Create the annotation_list
        annotation_list = []
        image_id = 1
        annotation_id = 1
        pbar = tqdm(maskPathList)
        # for mask_image in tqdm(maskImageList):
        for maskPath in pbar:
            mask_image = Image.open(maskPath)
            pbar.set_description("annotations [" + os.path.split(maskPath)[-1] + "]")
            sub_masks = create_sub_masks(mask_image)
            for color, sub_mask in sub_masks.items():
                category_id = category_ids[color]
                annotation_dict = create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd = 0)
                annotation_list.append(annotation_dict)
                annotation_id += 1 # it is okay when one foreground per one image
            image_id += 1
        json_dict['annotations'] = annotation_list

        # Create the categories_list
        categories_list = []
        for category_names in category_names_list:
            categories_dict = {}
            categories_dict['supercategory'] = ""
            categories_dict['id'] = category_names_list.index(category_names)
            categories_dict['name'] = category_names
            categories_list.append(categories_dict)

        json_dict['categories'] = categories_list

        with open(os.path.join(annotDirPath, os.path.split(dataDirPath)[-1]) + ".json", "w") as json_file:
            json_file.write(json.dumps(json_dict, indent = 4))

    # Copy the images to the annotations directory
    dataDirPathList = [trainDirPath, valDirPath, testDirPath]
    outputDirNameList = ['train2022', 'val2022', 'test2022']

    for dataDirPath, outputDirName in zip(dataDirPathList, outputDirNameList):
        imageDirPath = os.path.join(dataDirPath, 'images')
        cocoImageDirPath = os.path.join(rootDirPath, outputDirName)
        for imageName in os.listdir(imageDirPath):
            imagePath = os.path.join(imageDirPath, imageName)
            shutil.copy(imagePath, cocoImageDirPath)

    # Copy the masks to the annotations directory
    stuffDirPath = os.path.join(rootDirPath, 'stuffthingmaps')
    
    for dataDirPath, outputDirName in zip(dataDirPathList, outputDirNameList):
        maskDirPath = os.path.join(dataDirPath, 'masks')
        cocoMaskDirPath = os.path.join(stuffDirPath, outputDirName)
        for maskName in os.listdir(maskDirPath):
            maskPath = os.path.join(maskDirPath, maskName)
            shutil.copy(maskPath, cocoMaskDirPath)
