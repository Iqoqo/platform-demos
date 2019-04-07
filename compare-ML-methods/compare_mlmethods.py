import pandas as pd

from sklearn import model_selection

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis



### define the models pool
modelnames = ["LogReg", "SVM", "DecTree", "KNN", "LinDisc", "GaussianNB"]

random_seed = 12


def analyse(model_name):
    ### read in the data (HEP)
    data = pd.read_csv('https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_30000.csv')
    data.head()
    data_to_use = data
    data_to_use.dropna(inplace=True)
    data_to_use.head()
    values = data_to_use.values
    Y = values[:,0]
    X = values[:,1:28]
    
    
    print "--- starting "+model_name+" analysis ---"
    model = []
    if(model_name=='LogReg'):       model.append( LogisticRegression() )
    elif(model_name=='SVM'):        model.append( SVC() )
    elif(model_name=='DecTree'):    model.append( DecisionTreeClassifier() )
    elif(model_name=='KNN'):        model.append( KNeighborsClassifier() )
    elif(model_name=='LinDisc'):    model.append( LinearDiscriminantAnalysis() )
    elif(model_name=='GaussianNB'): model.append( GaussianNB() )
    else: 
        print "Model name not found: "+model_name
        quit()
    
    k_fold_validation = model_selection.KFold(n_splits=10, random_state=random_seed)
    results = model_selection.cross_val_score(model[0], X, Y, cv=k_fold_validation, scoring='accuracy')
    output_message = "%s| Mean=%f STD=%f" % (model_name, results.mean(), results.std())
    print(output_message)
    print "--- done "+model_name+" analysis ---"
    return model_name, results


def linear(imodel=-1):
    if(imodel<0):
       results = []
       names = []
       for modelname in modelnames:
          name, result = analyse(modelname)
          results.append(result)
          names.append(name)
    else:
       analyse(modelnames[imodel])

### call linear(...) with integer index to run a specific
### model, or with no arguments to run all sequentially
### comment out if you run through multiprocess manager
# linear()

###########################################################
#################IQOQOmp################################## 
##########################################################
import os
from iqoqomp import Pool
#from multiprocessing import Pool


os.environ['IQOQO_LOGIN_USER'] = 'efrat.tal@iqoqo.co'
os.environ['IQOQO_LOGIN_PASSWORD'] = '12345678'

p = Pool()
collectedoutput = p.map(analyse, modelnames)

###########################################################
#################IQOQOmp################################## 
##########################################################