# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:06:57 2023

@author: lujai
"""

import flask 
from flask import request, jsonify 
import pandas as pd

app=flask.Flask(__name__)
app.config["DEBUG"]=True

pl=pd.read_csv("C:/Users/lujai/OneDrive/Desktop/Ca4/df.csv")

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Flight price prediction in India</h1>
    <p>A prototype API for data on fligh price prediction.</p>'''
    
@app.route('/api/v1/flight/pl/all', methods=['GET'])
def api_all():
    result = {}
    for index, row in pl.iterrows():
        result[index] = dict(row)
    return jsonify(result)

@app.route('/api/v1/flight/pl', methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    names = ['Airline' , 'Source' , 'Destination' , 'Class','Duration_In_Minutes' , 'Journey_month']
    
    for param in query_parameters:
        if param not in names:
            return page_not_found(404)
    
    airline = query_parameters.get('Airline')
    source = query_parameters.get('Source')
    destination = query_parameters.get('Destination')
    clas = query_parameters.get('Class')
    duration = query_parameters.get('Duration_In_Minutes')
    month = query_parameters.get('Journey_month')
    
    if duration:
        duration = int(duration) 
    
    if month:
        month = int(month)
    new_pl = pl.copy()
    if airline:
        flights_pl=new_pl.loc[new_pl['Airline'] == airline]
        new_pl = pd.merge(new_pl, flights_pl)
    if source:
        city_pl = new_pl.loc[new_pl['Source'] == source]
        new_pl = pd.merge(new_pl, city_pl)
    if destination:
        des_pl = new_pl.loc[new_pl['Destination'] == destination]
        new_pl = pd.merge(new_pl, des_pl)
    if clas:
        type_pl = new_pl.loc[new_pl['Class'] == clas]
        new_pl = pd.merge(new_pl,type_pl)
    if duration:
        duration_pl = new_pl.loc[new_pl['Duration_In_Minutes'] == duration]
        new_pl = pd.merge(new_pl,duration_pl)
    if month:
        months_pl = new_pl.loc[new_pl['Journey_month'] == duration]
        new_pl = pd.merge(new_pl,months_pl)
        
    if not(airline or source or destination or clas or duration or month):
        return page_not_found(404)
    
    result = {}
    for index , row in new_pl.iterrows():
        result[index] = dict(row)
    return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.<p>",  404

app.run()

