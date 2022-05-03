import os
from pathlib import Path
# pip install split-folders
import splitfolders

print("Start datasetSplit")
# category_names_list = ['beer_bottle', 'beer_can', 'bowl', 'camera', 'chair', 'clock', 'club_chair', 'faucet', 'football_helmet', 'guitar', 'jug', 'lamp', 'piano', 'pistol', 'sofa', 'vase']
# category_names_list = ['piano', 'pistol', 'sofa', 'vase']
inputPath = Path('5input').absolute()
outputPath = Path('5output').absolute()
os.makedirs(outputPath, exist_ok=True)
splitfolders.ratio(inputPath, outputPath, seed=689, ratio=(.7, .2, .1))
