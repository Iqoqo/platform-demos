# -*- coding: utf-8 -*-
import time
from random import randint
from yaspin import yaspin
from pyimagesearch import config
from imutils import paths
import shutil
import os


# This essencially copies the files (same structure) 
# from 'Food-5K' to 'dataset'
def build_dataset(limit_count = 0):
	# loop over the data directories
	for split in (config.TRAIN, config.TEST, config.VAL):

		with yaspin(text="Processing directory '{}'...".format(split), color="yellow") as spinner:
		# grab all image paths in the current split
			p = os.path.sep.join([config.ORIG_INPUT_DATASET, split])
			imagePaths = list(paths.list_images(p))

			# loop over the image paths
			for im_idx, imagePath in enumerate(imagePaths):
				# extract class label from the filename
				filename = imagePath.split(os.path.sep)[-1]
				primaryClass = int(filename.split("_")[0])
				if primaryClass > 0:
					primaryClass = 1
				food_or_not_dir = config.CLASSES[primaryClass]

				# construct the path to the output directory
				dirPath = os.path.sep.join([config.BASE_PATH, split, food_or_not_dir])

				if not os.path.exists(dirPath):
					os.makedirs(dirPath)

				# construct the path to the output image file and copy it
				p = os.path.sep.join([dirPath, filename])
				shutil.copy2(imagePath, p)
				# print("copying from "+imagePath+" to "+ p)
				if limit_count and im_idx > limit_count:
					break
		spinner.ok("✅ ")

if __name__ == '__main__':
	build_dataset()

