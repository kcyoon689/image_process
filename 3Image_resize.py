from PIL import Image
import os.path


category_names_list = ['ashcan', 'beer_bottle', 'beer_can', 'bicycle', 'bowl', 
        'camera', 'car', 'chair', 'clock', 'football_helmet', 
        'guitar', 'lamp', 'laptop', 'microwave', 'piano', 
        'pistol', 'pool_table', 'skateboard', 'sofa', 'vase']

currentDirPath = os.getcwd()
target = currentDirPath + "/1foreground_cropped"

for dir in category_names_list:
    targerdir = target + "/" + dir #해당 폴더 설정 
    files = os.listdir(targerdir)

    format = [".jpg",".png",".jpeg","bmp",".JPG",".PNG","JPEG","BMP"] #지원하는 파일 형태의 확장자들
    for (path,dirs,files) in os.walk(targerdir):
        for file in files:
            if file.endswith(tuple(format)):
                image = Image.open(path+"/"+file)
                print(image.filename)
                print(image.size)
                
                #  image=image.resize((int(image.size[0]*0.35), int(image.size[1]*0.375)))
                image=image.resize((640, 480))
                image.save(path+"/"+file)
                print(image.size)
                
            else:
                print(path)
                print("InValid",file)