from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
from keras.utils import to_categorical
from sklearn.metrics import classification_report
from pyimagesearch import config
import numpy as np
import pickle
import os


def build_model(is_test = False):

	def csv_feature_generator(inputPath, bs, numClasses, mode="train"):
		# Open input file for reading
		f = open(inputPath, "r")

		# Loop indefinitely
		while True:
			# Initialize our batch of data and labels
			data = []
			labels = []

			# Keep looping until we reach our batch size
			while len(data) < bs:
				# Attempt to read the next row of the CSV file
				row = f.readline()

				# Check to see if the row is empty 
				# (indicating we have reached the end of the file)
				if row == "":
					# reset the file pointer to the beginning of the file
					f.seek(0)
					row = f.readline()

					# if we are evaluating we should now break from our
					# loop to ensure we don't continue to fill up the
					# batch from samples at the beginning of the file
					if mode == "eval":
						break

				# extract the class label 	and features from the row
				row = row.strip().split(",")
				label = row[1]
				label = to_categorical(label, num_classes=numClasses)
				features = np.array(row[2:], dtype="float")

				# update the data and label lists
				data.append(features)
				labels.append(label)

			# yield the batch to the calling function
			yield (np.array(data), np.array(labels))

	# load the label encoder from disk
	le = pickle.loads(open(config.LE_PATH, "rb").read())

	# derive the paths to the training, validation, and testing CSV files
	trainPath = os.path.sep.join([config.BASE_CSV_PATH,
		"{}.csv".format(config.TRAIN)])
	valPath = os.path.sep.join([config.BASE_CSV_PATH,
		"{}.csv".format(config.VAL)])
	testPath = os.path.sep.join([config.BASE_CSV_PATH,
		"{}.csv".format(config.TEST)])

	# determine the total number of images in the training and validation
	# sets
	totalTrain = sum([1 for l in open(trainPath)])
	totalVal = sum([1 for l in open(valPath)])

	# extract the testing labels from the CSV file and then determine the
	# number of testing images
	testLabels = [int(row.split(",")[1]) for row in open(testPath)]
	testPaths = [row.split(",")[0] for row in open(testPath)]
	totalTest = len(testLabels)

	# construct the training, validation, and testing generators
	trainGen = csv_feature_generator(trainPath, config.BATCH_SIZE,
		len(config.CLASSES), mode="train")
	valGen = csv_feature_generator(valPath, config.BATCH_SIZE,
		len(config.CLASSES), mode="eval")
	testGen = csv_feature_generator(testPath, config.BATCH_SIZE,
		len(config.CLASSES), mode="eval")

	# Define simple neural network
	model = Sequential()
	model.add(Dense(256, input_shape=(7 * 7 * 2048,), activation="relu"))
	model.add(Dense(16, activation="relu"))
	model.add(Dense(len(config.CLASSES), activation="softmax"))

	# Compile the model
	opt = SGD(lr=1e-3, momentum=0.9, decay=1e-3 / 25)
	model.compile(loss="binary_crossentropy", 
				  optimizer=opt,
		       	  metrics=["accuracy"])

	# Train the network
	print("[INFO] training simple network...")
	# (in test, we just want to see that this code is runing ok.)
	if is_test:
		epochs = 1
		model_f_name = 'food_model.test.h5'
	else:
		epochs =  25 
		model_f_name = 'food_model.h5'
	H = model.fit_generator(
		trainGen,
		steps_per_epoch=totalTrain // config.BATCH_SIZE,
		validation_data=valGen,
		validation_steps=totalVal // config.BATCH_SIZE,
		epochs=epochs)
	
	model.save(model_f_name)
	print("[INFO] Done training model.")

def test():
	build_model(True)
	assert os.path.isfile('food_model.test.h5'), 'model file does not exist'


if __name__ == '__main__':
	build_model()