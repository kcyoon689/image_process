import os
import sys
import signal
import cv2
import random
from tqdm import tqdm

def signal_handler(signal, frame):
    print('pressed ctrl + c!!!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class CropForeground:
  def __init__(self):
    print("crop_foreground init!")
    self.currentDirPath = os.getcwd()
    self.foregroundDirPath = self.currentDirPath + "/1foreground"
    self.foregroundCroppedDirPath = self.currentDirPath + "/1foreground_cropped"
    self.foregroundClass_list = os.listdir(self.foregroundDirPath)
    self.foregroundFilePath_list = [None] * len(self.foregroundClass_list)
    self.rawDataFileFullPath_list = []
    for idx in range(len(self.foregroundClass_list)):
      self.foregroundFilePath_list[idx] = os.listdir(self.foregroundDirPath + "/" + self.foregroundClass_list[idx])
      self.rawDataFileFullPath_list += [
          self.foregroundDirPath + '/' + self.foregroundClass_list[idx] + '/' + file_name for file_name in self.foregroundFilePath_list[idx]]

  def run(self):
    print("run")
    for fileFullPath in tqdm(self.rawDataFileFullPath_list):
      img = cv2.imread(fileFullPath)
      height, width, channels = img.shape

      # Check if the image is valid
      assert height == 1920, "height is not 1920. [" + fileFullPath + "]"
      assert width == 2880, "width is not 2880. [" + fileFullPath + "]"
      assert channels == 3, "channels is not 3. [" + fileFullPath + "]"

      y = random.randrange(0,int(height/3))
      x = random.randrange(0,int(width/3))

      cropped_img = img[y: y + int(height*2/3), x: x + int(width*2/3)]
      height_cropped, width_cropped, channels_cropped = cropped_img.shape

      # Check if the cropped image is valid
      assert height_cropped == 1280, "height 웨디is not 1280"
      assert width_cropped == 1920, "width is not 1920"
      assert channels_cropped == 3, "channels is not 3"

      croppedFullPath = fileFullPath.replace("1foreground", "1foreground_cropped")
      head, tail = os.path.split(croppedFullPath)
      os.makedirs(head, exist_ok=True)
      cv2.imwrite(croppedFullPath, cropped_img)
    print("done!")

if __name__ == "__main__":
    cropForeground = CropForeground()
    cropForeground.run()
