echo 
"""
---- Running full cycle of train and prediction ----

"""

python3 build_dataset.py &&
echo """ build DONE """ &&
python3 extract_features.py &&
echo """ extract features DONE """ &&
python3 train.py &&
echo """ train DONE """ &&
python3 predict.py &&
echo """ predict DONE """ 



