import os
import pickle
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from sklearn.metrics import classification_report
from pyimagesearch import config
from keras.layers.core import Dense
from keras.optimizers import SGD
from keras.utils import to_categorical
import math
import tensorflow as tf
# Suppress tensoflow version warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def run_prediction(is_test = False):
	tf.logging.set_verbosity(tf.logging.ERROR)
	print("[INFO] Running prediction...")
	def csv_feature_generator(inputPath, batchSize, numClasses, mode="train"):
		# open the input file for reading
		f = open(inputPath, "r")

		# loop indefinitely
		while True:
			# initialize our batch of data and labels
			featuresArray = []
			labels = []

			# keep looping to batch size
			while len(featuresArray) < batchSize:
				# attempt to read the next row of the CSV file
				row = f.readline()
				# empty row means end of file
				if row == "":
					# reset file pointer to the beginning of the file
					# and re-read the row
					f.seek(0)
					row = f.readline()

					# if we are evaluating we should now break from our
					# loop to ensure we don't continue to fill up the
					# batch from samples at the beginning of the file
					if mode == "eval":
						break

				# extract the class label and features from the row
				row = row.strip().split(",")
				label = row[1]
				label = to_categorical(label, num_classes=numClasses)
				features = np.array(row[2:], dtype="float")

				# update the featuresArray and label lists
				featuresArray.append(features)
				labels.append(label)

			# return batch
			yield (np.array(featuresArray), np.array(labels))


	testPath = os.path.sep.join([config.BASE_CSV_PATH,
		"{}.csv".format(config.TEST)])

	testLabels = [int(row.split(",")[1]) for row in open(testPath)]
	testNames = [row.split(",")[0] for row in open(testPath)]
	totalTest = len(testLabels)

	# load the label encoder
	le = pickle.loads(open(config.LE_PATH, "rb").read())

	testGen = csv_feature_generator(testPath, config.BATCH_SIZE,
		len(config.CLASSES), mode="eval")

	model = load_model('food_model.h5')
	# Make predictions on the testing images:
	# - Finding the index of the label with the corresponding largest predicted probability
	# - Then show a detailed classification report
	print("[INFO] Processing images input...")
	predIdxs = model.predict_generator(testGen,
		steps=math.ceil(totalTest/config.BATCH_SIZE))
	print("[INFO] Total inspected images: " + str(totalTest))
	predIdxs = np.argmax(predIdxs, axis=1)
	print(classification_report(testLabels, predIdxs,
		target_names=le.classes_))

	test_labels_names = le.inverse_transform(testLabels)
	for label, path in zip (test_labels_names, testNames):
		print ("{} classified as {}".format(path, label))

if __name__ == '__main__' :
	run_prediction()

