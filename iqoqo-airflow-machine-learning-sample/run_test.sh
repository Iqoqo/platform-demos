#requires pytest 
#pip install pytest

echo """
 ----TEST----- 
 tests are dependent so must run in this order
 only testing code functionality, not the prediction accuracy
 """

pytest -s --disable-warnings build_dataset.py extract_features.py train.py predict.py
