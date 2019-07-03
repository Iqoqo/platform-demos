# Pre process
from sklearn.preprocessing import LabelEncoder
from keras.applications import ResNet50
from keras.applications import imagenet_utils
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from pyimagesearch import config
from imutils import paths
import numpy as np
import pickle
import random
import os
import sys

ALL_SPLITS = (config.TRAIN, config.TEST, config.VAL)

def extract_features(limit_n_batch=0, splits=ALL_SPLITS):
	os.makedirs(config.BASE_CSV_PATH, exist_ok=True)	
	clear_old_res()		
	print("[INFO] loading network...")
	
	# load the ResNet50 network and initialize the label encoder
	model = ResNet50(weights="imagenet", include_top=False)
	le = None

	# loop over the data splits
	for split in splits:
		# grab all image paths in the current split
		print("[INFO] processing '{} split'...".format(split))
		p = os.path.sep.join([config.BASE_PATH, split])
		imagePaths = list(paths.list_images(p))

		# randomly shuffle the image paths and then extract the class
		# labels from the file paths
		random.shuffle(imagePaths)
		labels = [p.split(os.path.sep)[-2] for p in imagePaths]

		# if the label encoder is None, create it
		if le is None:
			le = LabelEncoder()
			le.fit(labels)

		# open the output CSV file for writing
		csvPath = os.path.sep.join([config.BASE_CSV_PATH,
			"{}.csv".format(split)])
		csv = open(csvPath, "w")

		# loop over the images in batches
		for (b, i) in enumerate(range(0, len(imagePaths), config.BATCH_SIZE)):
			# extract the batch of images and labels, then initialize the
			# list of actual images that will be passed through the network
			# for feature extraction
			print("[INFO] processing batch {}/{}".format(b + 1,
				int(np.ceil(len(imagePaths) / float(config.BATCH_SIZE)))))
			batchPaths = imagePaths[i:i + config.BATCH_SIZE]
			batchLabels = le.transform(labels[i:i + config.BATCH_SIZE])
			batchImages = []

			# loop over the images and labels in the current batch
			for imagePath in batchPaths:
				# load the input image using the Keras helper utility
				# while ensuring the image is resized to 224x224 pixels
				image = load_img(imagePath, target_size=(224, 224))
				image = img_to_array(image)

				# preprocess the image by (1) expanding the dimensions and
				# (2) subtracting the mean RGB pixel intensity from the
				# ImageNet dataset
				image = np.expand_dims(image, axis=0)
				image = imagenet_utils.preprocess_input(image)

				# add the image to the batch
				batchImages.append(image)

			# pass the images through the network and use the outputs as
			# our actual features, then reshape the features into a
			# flattened volume
			batchImages = np.vstack(batchImages)
			features = model.predict(batchImages, batch_size=config.BATCH_SIZE)
			features = features.reshape((features.shape[0], 7 * 7 * 2048))

			# loop over the class labels and extracted features
			for (name, label, vec) in zip(batchPaths, batchLabels, features):
				# construct a row that exists of the class label and
				# extracted features
				vec = ",".join([str(v) for v in vec])
				csv.write("{},{},{}\n".format(name, label, vec))
			if limit_n_batch and b+1 >= limit_n_batch: #b is zero based
				print("hit limit. breaking")
				break
		# close the CSV file
		csv.close()

	# serialize the label encoder to disk
	f = open(config.LE_PATH, "wb")
	f.write(pickle.dumps(le))
	f.close()

out_files = ['{}.csv'.format(split) for split in (config.TRAIN, config.TEST, config.VAL)] + ['le.cpickle']
outdir = config.BASE_CSV_PATH

def clear_old_res():
	for f in out_files:
		f_path = '{}/{}'.format(outdir,f)
		if os.path.isfile(f_path):
			print("Clearing old data {}".format(f_path))
			os.remove(f_path)

def test():
	clear_old_res()
	for f in out_files:
		assert not os.path.isfile('{}/{}'.format(outdir,f)), 'file {} exists after clear'.format(f)
	
	extract_features(1)
	
	assert os.path.isdir(outdir), 'outdir does not exist'
	for f in out_files:
		f_path = '{}/{}'.format(outdir,f)
		assert os.path.isfile(f_path), 'file {} missing'.format(f)
		if 'csv' in f_path:
			with open(f_path) as _op:
				_line = _op.readline()
				assert len(_line.split(',')) > 3, _line

def main():
	try: 
		if len(sys.argv) == 1:
			#no splits 
			splits = ALL_SPLITS
		else:
			splits = set(argv[1:])
			for split in splits:  
				assert split in ALL_SPLITS, '{} not a valid split'.format(split)

	except:
		print('invalid args {}'.format(sys.argv))
		print('valid splits {}'.format(ALL_SPLITS))
		exit(1)
	extract_features(splits=splits)

if __name__ == '__main__':
	main()

