from fastapi import FastAPI
from flask import request
from fastapi import FastAPI, File, UploadFile
from ml_dna.preprocessor import *
import io
import tensorflow
import numpy as np


app = FastAPI()

app.state.model = tensorflow.keras.models.load_model('cnn_model.h5')


#the fucntion for the hardcoded Dictionary, maybe we can put it somewhere else

def create_dict(val1, val2, val3, val4, val5):
    my_dict = {
        "Australian": val1,
        "Canadian": val2,
        "England": val3,
        "Indian": val4,
        "US": val5
        }
    return my_dict


@app.post("/uploadfile")
async def create_upload_file(wav: bytes = File(...)):

    model = app.state.model
    assert model is not None
    res_arr = preprocess(io.BytesIO(wav))
    res_arr_pred = res_arr.reshape((1,128,302,1))
    res_lst = list(res_arr)

    pred = model.predict(res_arr_pred)
    pred_list = list(pred)
    dic = create_dict(float(pred_list[0][0]),float(pred_list[0][1]),float(pred_list[0][2]),float(pred_list[0][3]), float(pred_list[0][4]))
    print(type(dic))
    print(dic)
    #resp_dict = dict(resp=float(res_lst[0][0]))
    return dic




"""
@app.get('/predict')
def predict("data"):

    code here where we get data as input and then have to tiurn it into a dataframe that can be fed to our model
    stored in X_pred
    then use already created function that will preprocess the input
    and then use the model that we got wih load model fucntion and apply it to our X
    return it un the format we want

    model = app.state.model
    assert model is not None

    X_processed_audio = preprocess_features(X_pred)
    y_pred = model.predict(X_processed_audio)

    hard_code your dictionary function:


    return {'format':'as we like'}
"""

@app.get('/')
def root():
    return {"British":"50%",
            "American": "20%",
            "Australian": "10%",
            "Canadian": "20%"}
