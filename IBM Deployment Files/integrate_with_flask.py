#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 20:52:19 2022

@author: sakai
"""
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('/home/sakai/ADS-2022/Project/Flask/model0.pkl','rb'))
API_KEY = "VRPKD1qVgUgqtLpDzESBUnBSykdvOGmUNou5Z065rfbq"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

    
@app.route('/sy_predict',methods=['POST'])
def sy_predict():
    inp1=[]
    inp1.append(random.randint(0,100)) #id
    inp1.append(random.randint(0,365)) #cycle
    for i in range(0,24):
        inp1.append(random.uniform(0,1))
    inp1.append(random.randint(0,365)) #ttf
    pred=model.predict([inp1])
    payload_scoring = {"input_data": 
			[{"field": [['Wind Speed | (m/s)','Wind Direction | (deg)','Pressure | (atm)', 'Air Temperature | (\'C)']], "values": [(inp1)]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7488912b-b6aa-4b62-a92b-8273bfcc6da6/predictions?version=2022-05-29', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions =response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        pred = "No failure expected within 30 days."
    else:
        pred = "Maintenance Required!! Expected a failure within 30 days."
    return render_template('Sensor_predict.html', prediction_text=pred,data=inp1)

if __name__=="__main__":
    app.run(debug=True)

