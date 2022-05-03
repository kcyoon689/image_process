# This program is for auto labeling training data of yolo v5

import os
import sys
import signal
import cv2
from tqdm import tqdm


def signal_handler(signal, frame):
    print('pressed ctrl + c!!!')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


class AutoGenerate_bg:
    def __init__(self):
        print("AutoLabeler init!")
        self.currentDirPath = os.getcwd()  # /home/kcy/Auto_labeling_for_YOLOv5
        self.rawDataDirPath = self.currentDirPath + "/4images"
        self.rawDataFilePath_list = os.listdir(self.rawDataDirPath)
        self.rawDataFileFullPath_list = [
            self.rawDataDirPath + '/' + file_name for file_name in self.rawDataFilePath_list]

        self.bgDataDirPath = self.currentDirPath + "/2background_cropped"
        self.bgDataFilePath_list = os.listdir(self.bgDataDirPath)
        self.bgDataFileFullPath_list = [
            self.bgDataDirPath + '/' + file_name for file_name in self.bgDataFilePath_list]

        self.imagesDirPath = self.currentDirPath + "/4images_bg"

    def showImage(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)

    def mergeBG(self, img, bg, criteria):
        # convert raw rgb img to gray img
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgHeight_px, imgWidth_px = grayImg.shape

        # get background Image and check it is possible to use for merging raw image and bg iamge
        bgHeight_px, bgWidth_px, channel = bg.shape
        if (bgHeight_px < imgHeight_px) or (bgWidth_px < imgWidth_px):
            print("background image is too small!!")
            print(grayImg.shape)
            print(bg.shape)
            sys.exit(0)
        # trim bg image as same size of raw image
        bgTrimmed = bg[0:imgHeight_px, 0:imgWidth_px]

        # get background mask (bg: 255, object: 0)
        ret, bgMask = cv2.threshold(grayImg, criteria, 255, cv2.THRESH_BINARY)
        # convert the scale of bgMask gray to rgb
        bgMask_color = cv2.cvtColor(bgMask, cv2.COLOR_GRAY2RGB)
        # Get masked background
        bgMasked = cv2.bitwise_and(bgTrimmed, bgMask_color)

        # get inverted background mask (bg: 0, object: 255)
        bgMaskInv = cv2.bitwise_not(bgMask)
        # convert the scale of bgMaskInv gray to rgb
        bgMaskInv_color = cv2.cvtColor(bgMaskInv, cv2.COLOR_GRAY2RGB)
        # Get masked object
        imgMasked = cv2.bitwise_and(img, bgMaskInv_color)

        # Merge masked background and object images
        bgImg = cv2.add(bgMasked, imgMasked)
        return bgImg

    def saveImage(self, img, imgCount):
        imageFileFullPath = self.imagesDirPath + \
            "/" + self.rawDataFilePath_list[imgCount]
        imageFileFullPath = self.imagesDirPath + \
            "/" + self.rawDataFilePath_list[imgCount].replace('png', 'jpg')
        os.makedirs(self.imagesDirPath, exist_ok=True)
        cv2.imwrite(imageFileFullPath, img)

    def run(self):
        for idx, rawDataPath in enumerate(tqdm(self.rawDataFileFullPath_list)):
            # print("load images")
            img_color = cv2.imread(rawDataPath, cv2.IMREAD_COLOR)
            # print("load bgImage")
            bg_color = cv2.imread(self.bgDataFileFullPath_list[idx], cv2.IMREAD_COLOR)
            # print("merge raw image and bg image")
            bgImg_color = self.mergeBG(img_color, bg_color, 254)
            # print("save images")
            self.saveImage(bgImg_color, idx)
            # print("{} data done!\n".format(idx))


if __name__ == "__main__":
    AutoGenerater = AutoGenerate_bg()
    AutoGenerater.run()
