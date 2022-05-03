import os
import sys
import signal
import cv2
import random
from tqdm import trange

def signal_handler(signal, frame):
    print('pressed ctrl + c!!!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class CropBackground:
  def __init__(self):
    print("crop_background init!")
    self.currentDirPath = os.getcwd()
    self.backgroundDirPath = self.currentDirPath + "/2background"
    self.backgroundCroppedDirPath = self.currentDirPath + "/2background_cropped"
    self.backgroundFilePath_list = os.listdir(self.backgroundDirPath)
    self.rawDataFileFullPath_list = [
        self.backgroundDirPath + '/' + file_name for file_name in self.backgroundFilePath_list]

  def run(self):
    print("run")
    for i in trange(4178): # 4178
      fileFullPath = random.choice(self.rawDataFileFullPath_list)
      img = cv2.imread(fileFullPath)
      height, width, channels = img.shape

      if width > 1920*3 and height > 1280*3:
        img = cv2.resize(img, (int(width*2/3), int(height*2/3)))
        height, width, channels = img.shape

      # Check if the image is valid
      assert height >= 1280, "height is less than 1280. [" + fileFullPath + "]"
      assert width >= 1920, "width is less than 1920. [" + fileFullPath + "]"
      assert channels == 3, "channels is not 3. [" + fileFullPath + "]"

      y = random.randrange(0, int(height - 1280))
      x = random.randrange(0, int(width - 1920))

      cropped_img = img[y: y + 1280, x: x + 1920]
      height_cropped, width_cropped, channels_cropped = cropped_img.shape

      # Check if the cropped image is valid
      assert height_cropped == 1280, "height is not 1280"
      assert width_cropped == 1920, "width is not 1920"
      assert channels_cropped == 3, "channels is not 3"

      os.makedirs(self.backgroundCroppedDirPath, exist_ok=True)
      cv2.imwrite(self.backgroundCroppedDirPath + "/bg_cropped_" + str(i).zfill(4) + ".png", cropped_img)
    print("done!")

if __name__ == "__main__":
    cropBackground = CropBackground()
    cropBackground.run()
