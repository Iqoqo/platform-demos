# compare_mlmethods.py usage


## Running the demo using iqoqomp
The script already has the iqoqomp imported and configured.
In order to run the script, you need to have the [iqoqomp](https://github.com/Iqoqo/iqoqomp) configured and then just open a command line and run the script as any python script.

## The analysis
The analysis is comparing 6 ML methods (using the sklearn package).
The models that compared are:
modelnames = ["LogReg", "SVM", "DecTree", "KNN", "LinDisc", "GaussianNB"]
You can see the original script in the following articale:
https://pythondata.com/

In order to compare the local run, in the code you'll have to just comment out the following line:
from iqoqomp import Pool
and comment in the following line:
from multiprocessing import Pool

You also have the possibility to run it in linear mode, for that you just need to comment in the linear() function.

## The Data

To have a more significant comparing the data was replaced with the following data: https://archive.ics.uci.edu/ml/datasets/Wilt
The demo data is stored in the following location:
1. For a data file of 10000 lines: https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_10000.csv
2. For a data file of 50000 lines: https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_50000.csv
3. For a data file of 7 million lines (5GB file): https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train.csv

statistic for 6 tasks:
#lines	local mp(sec)	iqoqmp(sec)
10000	   30	          30
30000	   260	          180
50000	   960	          840

