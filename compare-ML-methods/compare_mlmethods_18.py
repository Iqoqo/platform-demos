import pandas as pd

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis




### define the models pool
modelnames = ["LogReg", "SVM", "DecTree", "KNN", "LinDisc", "GaussianNB",
              "MLP", "GaussianPC", "RandomForest", "AdaBoost", "QuadraticDisc",
              "SVClinear", "SVCgamma", "KNN3", "GaussianRBF", "DecTreeDepth", "RandomForestDepth", "MLPalpha"]

random_seed = 12


def analyse(model_name):
    ### read in the data (HEP)
    data = pd.read_csv('https://s3-us-west-2.amazonaws.com/iqoqo.temp/demo/all_train_10000.csv')
    data.head()
    data_to_use = data
    data_to_use.dropna(inplace=True)
    data_to_use.head()
    values = data_to_use.values
    Y = values[:,0]
    X = values[:,1:28]
    
    
    print "--- starting "+model_name+" analysis ---"
    model = []
    if(model_name=='LogReg'):              model.append( LogisticRegression() )
    elif(model_name=='SVM'):               model.append( SVC() )
    elif(model_name=='DecTree'):           model.append( DecisionTreeClassifier() )
    elif(model_name=='KNN'):               model.append( KNeighborsClassifier() )
    elif(model_name=='LinDisc'):           model.append( LinearDiscriminantAnalysis() )
    elif(model_name=='GaussianNB'):        model.append( GaussianNB() )
    elif(model_name=='MLP'):               model.append( MLPClassifier() )
    elif(model_name=='GaussianPC'):        model.append( GaussianProcessClassifier() )
    elif(model_name=='RandomForest'):      model.append( RandomForestClassifier() )
    elif(model_name=='AdaBoost'):          model.append( AdaBoostClassifier() )
    elif(model_name=='QuadraticDisc'):     model.append( QuadraticDiscriminantAnalysis() )
    elif(model_name=='SVClinear'):         model.append( SVC(kernel="linear", C=0.025) )
    elif(model_name=='SVCgamma'):          model.append( SVC(gamma=2, C=1) )
    elif(model_name=='KNN3'):              model.append( KNeighborsClassifier(3) )
    elif(model_name=='GaussianRBF'):       model.append( GaussianProcessClassifier(1.0 * RBF(1.0)) )
    elif(model_name=='DecTreeDepth'):      model.append( DecisionTreeClassifier(max_depth=5) )
    elif(model_name=='RandomForestDepth'): model.append( RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1) )
    elif(model_name=='MLPalpha'):          model.append( MLPClassifier(alpha=1) )
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
       plotsummary(names,results)
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
