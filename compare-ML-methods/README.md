# Usage


## Running the demo using discomp
The script already has the discomp imported and configured the pool usage.

In order to run the script you should do the following:

1. Create a new folder and download there the script (recommended to start with the simple script, compare_mlmethods.py) and the requirements.txt from this repository.

Note that you should adjust in the script your discomp user and password.

2. In that folder Install and activate python virtual env (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. In that folder,  pip3 install -r requirements.txt

4. python3 compare_mlmethods.py

5. You can now login to your disco app and see that job with 6 tasks was created.

link to [discomp](https://github.com/Iqoqo/iqoqomp) documentation.

You should also have Dis.co CLI installed before running the script:

```
 curl https://s3.us-west-2.amazonaws.com/disco.cli/install.sh | sh
```

## The analysis
The analysis is comparing different Machine learning methods (using the sklearn package).

There are 2 scripts:

1. Comparing 6 methods:

   modelnames = ["LogReg", "SVM", "DecTree", "KNN", "LinDisc", "GaussianNB"]

2. Comparing 18 methods:
   
  modelnames = ["LogReg", "SVM", "DecTree", "KNN", "LinDisc", "GaussianNB",
              "MLP", "GaussianPC", "RandomForest", "AdaBoost", "QuadraticDisc",
              "SVClinear", "SVCgamma", "KNN3", "GaussianRBF", "DecTreeDepth", "RandomForestDepth", "MLPalpha"]
              
You can see the original script in the following article:
https://pythondata.com/

## You can run this script either using discomp or localy:

1. For a local run,comment in the following line:

    from multiprocessing import Pool

2. For discomp comment in the following line:
   
   from discomp import Pool
  

You also have the possibility to run it in linear mode, for that you just need to comment in the linear() function.

## The Data

To have a more significant comparing the original data from the articale was replaced with the following data: http://archive.ics.uci.edu/ml/datasets/hepmass
The demo data is stored in the following location:
1. For a data file of 10000 lines: https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_10000.csv
2. For a data file of 50000 lines: https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_50000.csv
3. For a data file of 30000 lines: https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_30000.csv
4. For a data file of 7 million lines (5GB file): https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train.csv


## Statistic for 6 tasks:

#lines |local mp(sec) | iqoqmp(sec) |
--- | --- | --- |
10000	 | 30 | 30 | 
30000 | 260 | 180 |
50000 | 960 | 840 |


## Statistic for 18 tasks:

#lines |local mp(sec) | iqoqmp(sec) |
--- | --- | --- |
10000	 | 1300 | 720 | 

