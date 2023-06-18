from django.apps import AppConfig
from django.conf import settings
import os
import pickle
import pandas as pd
import xgboost as xgb
from AppCantine.settings import BASE_DIR

class CantinedataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cantinedata'

# create path to models
    path_model = os.path.join(BASE_DIR, 'cantinedata','predict', 'xgb_model_grcv.json')
    path_artefacts = os.path.join(BASE_DIR, 'cantinedata','predict', 'artefacts_model_xgb_grcv.pkl')
    predict_model = xgb.XGBRegressor()
    predict_model.load_model(path_model)
    
    # these will be accessible via this class
    with open(path_artefacts, 'rb') as f:
        dump_var = pd.read_pickle(f)
    
    global XParam 
    XParam = dump_var['X']
    global datetable 
    datetable = dump_var['Date']
    
    global getDateIndex
    getDateIndex = lambda str1 : datetable[datetable == str1].index.min()
    getDateParam = lambda str1 : XParam[getDateIndex(str1)]
    
    
