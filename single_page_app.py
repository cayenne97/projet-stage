# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 11:19:23 2022

@author: thomas
"""
import dash
from dash import dcc, html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.linear_model import LinearRegression
from datetime import datetime as dt
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tools import add_constant
from datetime import date
from urllib import request 
from zipfile import ZipFile 
import os
import sys
import io
import base64
import datetime 
import subprocess
import pandas as pd
import glob
import matplotlib.pyplot as plt
import plotly.express as px
import statsmodels.formula.api as smf
import plotly.graph_objs as go

os.chdir('C:/Users/thoma/Desktop/projet/')
parent_path = os.path.dirname('task/')
sys.path.append(parent_path)
from app_utils import ( 
    get_data_table_description, 
    get_team_table_description,
    resume_project)

   
    
# Fama_French 3 and 5 Factors[daily]:
    
ff_factors= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip",
               skiprows = 3,index_col=0).drop("Copyright 2021 Kenneth R. French",axis=0)
ff_factors= round(ff_factors,3)

ff_factors_5= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",skiprows=3,index_col=0)
                        
Industry_12_portfolios= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/12_Industry_Portfolios_daily_CSV.zip",skiprows=10430,index_col=0).drop("Copyright 2021 Kenneth R. French",axis=0).reset_index()

# =============================================================================
# 12 Industry Portfolios[daily]:
# =============================================================================
    
Industry_12= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/12_Industry_Portfolios_daily_CSV.zip",
                     skiprows = 9,index_col=0,sep='\s*,\s*', engine='python').drop("Copyright 2021 Kenneth R. French",axis=0)



# =============================================================================
# Conversion des types de données "objets" en "float":
# =============================================================================

Industry_12=Industry_12.apply(pd.to_numeric,errors='coerce')





Firstpart=Industry_12[0:round(Industry_12.shape[0]/2)-1].rename(columns= {'NoDur':'NoDur_vw',"Durbl":"Durbl_vw","Manuf":"Manuf_vw", 
                                              "Enrgy":"Enrgy_vw","Chems":"Chems_vw","BusEq":"BusEq_vw",
                                             "Telcm":"Telcm_vw","Utils":"Utils_vw","Shops":"Shops_vw","Hlth":"Hlth_vw"
                                              ,"Money":"Money_vw","Other":"Other_vw"})


Secondpart=Industry_12[round(Industry_12.shape[0]/2)+1:].rename(columns={'NoDur':'NoDur_ew',"Durbl":"Durbl_ew","Manuf":"Manuf_ew", 
                                              "Enrgy":"Enrgy_ew","Chems":"Chems_ew","BusEq":"BusEq_ew",
                                             "Telcm":"Telcm_ew","Utils":"Utils_ew","Shops":"Shops_ew","Hlth":"Hlth_ew"
                                             ,"Money":"Money_ew","Other":"Other_ew"})


Industry_12_vw_1963_2021= Firstpart[10420:].dropna()
Industry_12_ew_1963_2021= Secondpart[10420:].dropna()


# =============================================================================
# SP= pd.read_csv("C:/Users/thoma/OneDrive/Bureau/projet stage/ox/betas/betas_SFF_2010-01-04_2021-10-29_NoDur_vw_{Mkt,SMB,HML}.csv")
# FIG= px.line(SP, x='Date', y= SP["Mkt"].rolling(window=7).mean())
# =============================================================================



# =============================================================================
# Calcul des dévitations par rapport à RF
# =============================================================================

déviations_vw= pd.DataFrame({'DevNoDur_vw':Firstpart["NoDur_vw"] - ff_factors["RF"],
                           'DevManuf_vw':Firstpart["Manuf_vw"] - ff_factors["RF"],
                           'DevEnergy_vw':Firstpart["Enrgy_vw"] - ff_factors["RF"],
                           'DevChemsr_vw':Firstpart["Chems_vw"] - ff_factors["RF"],
                           'DevBusEq_vw':Firstpart["BusEq_vw"] - ff_factors["RF"],
                          'DevTelcm_vw':Firstpart["Telcm_vw"] - ff_factors["RF"],
                           'DevUtils_vw':Firstpart["Utils_vw"] - ff_factors["RF"],
                           'DevShpos_vw':Firstpart["Shops_vw"] - ff_factors["RF"],
                           'DevMoney_vw':Firstpart["Money_vw"] - ff_factors["RF"],
                           'DevOther_vw':Firstpart["Other_vw"] - ff_factors["RF"]
                           })
déviations_vw= round(déviations_vw,3)



déviations_ew= pd.DataFrame({'DevNoDDur_ew':Secondpart["NoDur_ew"] - ff_factors["RF"],
                           'DevManuf_ew':Secondpart["Manuf_ew"] - ff_factors["RF"],
                           'DevEnergy_ew':Secondpart["Enrgy_ew"] - ff_factors["RF"],
                           'DevChemsr_ew':Secondpart["Chems_ew"] - ff_factors["RF"],
                           'DevBusEq_ew':Secondpart["BusEq_ew"] - ff_factors["RF"],
                          'DevTelcm_ew':Secondpart["Telcm_ew"] - ff_factors["RF"],
                           'DevUtils_ew':Secondpart["Utils_ew"] - ff_factors["RF"],
                           'DevShpos_ew':Secondpart["Shops_ew"] - ff_factors["RF"],
                           'DevMoney_ew':Secondpart["Money_ew"] - ff_factors["RF"],
                           'DevOther_ew':Secondpart["Other_ew"] - ff_factors["RF"]
                           })
déviations_ew=round(déviations_ew,3)


# =============================================================================
# Concaténation des dataframes:
# =============================================================================

concat= pd.concat([ff_factors, Firstpart, Secondpart],axis=1).reset_index() # Alow to see the index.
concat["index"]= pd.to_datetime(concat["index"],errors='coerce')
concat['date']= concat['index'].dt.date
concat.set_index('index', inplace=True)
concat['year']=concat.index.year
concat.insert(0, 'date', concat.pop("date"))

concatDev= pd.concat([déviations_vw, déviations_ew],axis=1).reset_index()
concatDev["index"]= pd.to_datetime(concatDev["index"]).dt.date

# =============================================================================
# concatwithDev= pd.read_csv("C:/Users/thoma/OneDrive/Bureau/projet/ox/data/concat.csv")
# concatwithDev=round(concatwithDev,3)
# =============================================================================

concatwithDev=pd.concat([ff_factors,Firstpart, Secondpart,déviations_vw, déviations_ew],axis=1).reset_index()
concatwithDev["index"]= pd.to_datetime(concatwithDev["index"]).dt.date
concatwithDev=concatwithDev.rename(columns={'index':'date','Mkt-RF':'Mkt'})
concatwithDev.to_csv("C:/Users/thoma/Desktop/projet/ox/data/concat.csv ")


concat5factors= pd.concat([ff_factors_5.reset_index(drop=True),Industry_12_vw_1963_2021.reset_index(),Industry_12_ew_1963_2021.reset_index(drop=True)],axis=1)
concat5factors["index"]=pd.to_datetime(concat5factors["index"],errors="coerce").dt.date
concat5factors= concat5factors.rename(columns={"index":"date"})
concat5factors.insert(0, 'date', concat5factors.pop("date"))


concat5factorswithMkt=pd.concat([ff_factors_5.reset_index(drop=True),Industry_12_vw_1963_2021.reset_index(),Industry_12_ew_1963_2021.reset_index(drop=True)],axis=1)
concat5factorswithMkt["index"]= pd.to_datetime(concat5factorswithMkt["index"]).dt.date
concat5factorswithMkt=concat5factorswithMkt.rename(columns={'index':'date','Mkt-RF':'Mkt'})
concat5factorswithMkt.insert(0, 'date', concat5factorswithMkt.pop("date"))
concat5factorswithMkt["devNoDur_vw"]=concat5factors["NoDur_vw"] - concat5factors["RF"]
concat5factorswithMkt["devManuf_vw"]=concat5factors["Manuf_vw"] - concat5factors["RF"]
concat5factorswithMkt["devEnrgy_vw"]=concat5factors["Enrgy_vw"] - concat5factors["RF"]
concat5factorswithMkt["devChems_vw"]=concat5factors["Chems_vw"] - concat5factors["RF"]
concat5factorswithMkt["devBusEq_vw"]=concat5factors["BusEq_vw"] - concat5factors["RF"]
concat5factorswithMkt["devTelcm_vw"]=concat5factors["Telcm_vw"] - concat5factors["RF"]
concat5factorswithMkt["devUrils_vw"]=concat5factors["Utils_vw"] - concat5factors["RF"]
concat5factorswithMkt["devShops_vw"]=concat5factors["Shops_vw"] - concat5factors["RF"]
concat5factorswithMkt["devMoney_vw"]=concat5factors["Money_vw"] - concat5factors["RF"]
concat5factorswithMkt["devOther_vw"]=concat5factors["Other_vw"] - concat5factors["RF"]
concat5factorswithMkt["devNoDur_ew"]=concat5factors["NoDur_ew"] - concat5factors["RF"]
concat5factorswithMkt["devManuf_ew"]=concat5factors["Manuf_ew"] - concat5factors["RF"]
concat5factorswithMkt["devEnrgy_ew"]=concat5factors["Enrgy_ew"] - concat5factors["RF"]
concat5factorswithMkt["devChems_ew"]=concat5factors["Chems_ew"] - concat5factors["RF"]
concat5factorswithMkt["devBusEq_ew"]=concat5factors["BusEq_ew"] - concat5factors["RF"]
concat5factorswithMkt["devTelcm_ew"]=concat5factors["Telcm_ew"] - concat5factors["RF"]
concat5factorswithMkt["devUtils_ew"]=concat5factors["Utils_ew"] - concat5factors["RF"]
concat5factorswithMkt["devShops_ew"]=concat5factors["Shops_ew"] - concat5factors["RF"]
concat5factorswithMkt["devMoney_ew"]=concat5factors["Money_ew"] - concat5factors["RF"]
concat5factorswithMkt["devOther_ew"]=concat5factors["Other_ew"] - concat5factors["RF"]
concat5factorswithMkt= round(concat5factorswithMkt,3)
concat5factorswithMkt.to_csv("C:/Users/thoma/Desktop/projet/ox/data/concat5factors.csv")


# =============================================================================
# OLS Regression of the varible on "MkT-RF", "SMB","RF"
# =============================================================================

y= concat["NoDur_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
res= model.fit(X,y)


y= concat["Durbl_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Durbl_vw= model.fit(X,y)

y= concat["Manuf_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Manuf_vw= model.fit(X,y)


y= concat["Enrgy_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Enrgy_vw= model.fit(X,y)

y= concat["Chems_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Chems_vw= model.fit(X,y)


y= concat["BusEq_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
BusEq_vw= model.fit(X,y)


y= concat["Telcm_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Telcm_vw= model.fit(X,y)


y= concat["Utils_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Utils_vw= model.fit(X,y)

y= concat["Shops_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Shops_vw= model.fit(X,y)


y= concat["Hlth_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Hlth_vw= model.fit(X,y)


y= concat["Money_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Money_vw= model.fit(X,y)


y= concat["Other_vw"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Other_vw= model.fit(X,y)


y= concat["NoDur_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
NoDur_ew= model.fit(X,y)


y= concat["Durbl_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Durbl_ew= model.fit(X,y)


y= concat["Manuf_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Manuf_ew= model.fit(X,y)


y= concat["Enrgy_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Enrgy_ew= model.fit(X,y)


y= concat["Chems_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Chems_ew= model.fit(X,y)


y= concat["BusEq_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
BusEq_ew= model.fit(X,y)


y= concat["Telcm_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Telcm_ew= model.fit(X,y)


y= concat["Utils_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Utils_ew= model.fit(X,y)


y= concat["Shops_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Shops_ew= model.fit(X,y)

y= concat["Hlth_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Hlth_ew= model.fit(X,y)


y= concat["Money_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Money_ew= model.fit(X,y)


y= concat["Other_ew"]
X= concat[["Mkt-RF","SMB","HML"]]
model= LinearRegression()
Other_ew= model.fit(X,y)



# =============================================================================
# List of Dropdowns
# =============================================================================

dropdown_portfolios_3factors_vw= dcc.Dropdown(
    id= 'Portfolios_vw',
    options=[{'label':i, 'value':i} for i in Firstpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_portfolios_3factors_ew= dcc.Dropdown(
    id= 'Portfolios_ew',
    options=[{'label':i, 'value':i} for i in Secondpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_3factors_vw=dcc.Dropdown(
    id= 'dropdown_vw',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')
    

dropdown_3factors_ew=dcc.Dropdown(
    id= 'dropdown_ew',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')
    

dropdown_5factors_vw=dcc.Dropdown(
    id= 'dropdown_5_factors_vw',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"},
             {"label": "RMW", "value": "RMW"},
             {"label": "CMA", "value": "CMA"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

dropdown_5factors_ew=dcc.Dropdown(
    id= 'dropdown_5_factors_ew',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"},
             {"label": "RMW", "value": "RMW"},
             {"label": "CMA", "value": "CMA"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

dropdown_portfolios_5factors_vw= dcc.Dropdown(
    id= 'Portfolios_5factors_vw',
    options=[{'label':i, 'value':i} for i in Firstpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_portfolios_5factors_ew= dcc.Dropdown(
    id= 'Portfolios_5factors_ew',
    options=[{'label':i, 'value':i} for i in Secondpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

# =============================================================================
# Range slider
# =============================================================================

rangeSlider_vw= dcc.RangeSlider(id='my_rangeslider_vw',
                    min= concat.index.year.min(),
                    max= concat.index.year.max(),
                    value= [1926,2021],
                    marks={
                        1926: {"label": "1926"},
                        1930: {"label": "1330"},
                        1940: {"label": "1940"},
                        1950: {"label": "1950"},
                        1960: {"label": "1960"},
                        1970: {"label": "1970"},
                        1980: {"label": "1980"},
                        1990: {"label": "1990"},
                        2000: {"label": "2000"},
                        2010: {"label": "2010"},
                        2020: {"label": "2020"}}),

rangeSlider_ew= dcc.RangeSlider(id='my_rangeslider_ew',
                    min= concat.index.year.min(),
                    max= concat.index.year.max(),
                    value= [1926,2021],
                    marks={
                        1926: {"label": "1926"},
                        1930: {"label": "1330"},
                        1940: {"label": "1940"},
                        1950: {"label": "1950"},
                        1960: {"label": "1960"},
                        1970: {"label": "1970"},
                        1980: {"label": "1980"},
                        1990: {"label": "1990"},
                        2000: {"label": "2000"},
                        2010: {"label": "2010"},
                        2020: {"label": "2020"}}),
                


rangeSlider_5factors_vw= dcc.RangeSlider(id='my_rangeslider_5factors_vw',
                    min= concat.index[10420:].year.min(),
                    max= concat.index[10420:].year.max(),
                    value= [1963,2021],
                    marks={1963: {"label": "1963"},
                           1970: {"label": "1970"},
                           1980: {"label": "1980"},
                           1990: {"label": "1990"},
                           2000: {"label": "2000"},
                           2010: {"label": "2010"},
                           2020: {"label": "2020"}}),

rangeSlider_5factors_ew= dcc.RangeSlider(id='my_rangeslider_5factors_ew',
                    min= concat.index[10420:].year.min(),
                    max= concat.index[10420:].year.max(),
                    value= [1963,2021],
                    marks={1963: {"label": "1963"},
                           1970: {"label": "1970"},
                           1980: {"label": "1980"},
                           1990: {"label": "1990"},
                           2000: {"label": "2000"},
                           2010: {"label": "2010"},
                           2020: {"label": "2020"}})


    

NoDur={"Intercept":res.intercept_, "Mkt-RF": res.coef_[0], "SMB":res.coef_[1],"HML":res.coef_[2]}
Durbl= {"Intercept":Durbl_vw.intercept_, "Mkt-RF": Durbl_vw.coef_[0], "SMB":Durbl_vw.coef_[1],"HML":Durbl_vw.coef_[2]}
Manuf={"Intercept":Manuf_vw.intercept_, "Mkt-RF": Manuf_vw.coef_[0], "SMB":Manuf_vw.coef_[1],"HML":Manuf_vw.coef_[2]}
Enrgy= {"Intercept":Enrgy_vw.intercept_, "Mkt-RF": Enrgy_vw.coef_[0], "SMB":Enrgy_vw.coef_[1],"HML":Enrgy_vw.coef_[2]}
Chems= {"Intercept":Chems_vw.intercept_, "Mkt-RF": Chems_vw.coef_[0], "SMB":Chems_vw.coef_[1],"HML":Chems_vw.coef_[2]}
BusEq= {"Intercept":BusEq_vw.intercept_, "Mkt-RF": BusEq_vw.coef_[0], "SMB":BusEq_vw.coef_[1],"HML":BusEq_vw.coef_[2]}
Telcm= {"Intercept":Telcm_vw.intercept_, "Mkt-RF": Telcm_vw.coef_[0], "SMB":Telcm_vw.coef_[1],"HML":Telcm_vw.coef_[2]}
Utils= {"Intercept":Utils_vw.intercept_, "Mkt-RF": Utils_vw.coef_[0], "SMB":Utils_vw.coef_[1],"HML":Utils_vw.coef_[2]}
Shops={"Intercept":Shops_vw.intercept_, "Mkt-RF": Shops_vw.coef_[0], "SMB":Shops_vw.coef_[1],"HML":Shops_vw.coef_[2]}
Hlth= {"Intercept":Hlth_vw.intercept_, "Mkt-RF": Hlth_vw.coef_[0], "SMB":Hlth_vw.coef_[1],"HML":Hlth_vw.coef_[2]}
Money= {"Intercept":Money_vw.intercept_, "Mkt-RF": Money_vw.coef_[0], "SMB":Money_vw.coef_[1],"HML":Money_vw.coef_[2]}
Other= {"Intercept":Other_vw.intercept_, "Mkt-RF": Other_vw.coef_[0], "SMB":Other_vw.coef_[1],"HML":Other_vw.coef_[2]}


df_vw= pd.DataFrame({"NoDur":NoDur,"Durbl":Durbl,"Manuf":Manuf, "Enrgy":Enrgy,"Chems":Chems,"BusEq":BusEq,
                  "Utils":Utils,"Shops":Shops,"Hlth":Hlth,"Money":Money,"Other":Other}).reset_index()
df_vw= round(df_vw,4)

NoDur={"Intercept":NoDur_ew.intercept_, "Mkt-RF": NoDur_ew.coef_[0], "SMB":NoDur_ew.coef_[1],"HML":NoDur_ew.coef_[2]}
Durbl= {"Intercept":Durbl_ew.intercept_, "Mkt-RF": Durbl_ew.coef_[0], "SMB":Durbl_ew.coef_[1],"HML":Durbl_ew.coef_[2]}
Manuf={"Intercept":Manuf_ew.intercept_, "Mkt-RF": Manuf_ew.coef_[0], "SMB":Manuf_ew.coef_[1],"HML":Manuf_ew.coef_[2]}
Enrgy= {"Intercept":Enrgy_ew.intercept_, "Mkt-RF": Enrgy_ew.coef_[0], "SMB":Enrgy_ew.coef_[1],"HML":Enrgy_ew.coef_[2]}
Chems= {"Intercept":Chems_ew.intercept_, "Mkt-RF": Chems_ew.coef_[0], "SMB":Chems_ew.coef_[1],"HML":Chems_ew.coef_[2]}
BusEq= {"Intercept":BusEq_ew.intercept_, "Mkt-RF": BusEq_ew.coef_[0], "SMB":BusEq_ew.coef_[1],"HML":BusEq_ew.coef_[2]}
Telcm= {"Intercept":Telcm_ew.intercept_, "Mkt-RF": Telcm_ew.coef_[0], "SMB":Telcm_ew.coef_[1],"HML":Telcm_ew.coef_[2]}
Utils= {"Intercept":Utils_ew.intercept_, "Mkt-RF": Utils_ew.coef_[0], "SMB":Utils_ew.coef_[1],"HML":Utils_ew.coef_[2]}
Shops={"Intercept":Shops_ew.intercept_, "Mkt-RF": Shops_ew.coef_[0], "SMB":Shops_ew.coef_[1],"HML":Shops_ew.coef_[2]}
Hlth= {"Intercept":Hlth_ew.intercept_, "Mkt-RF": Hlth_ew.coef_[0], "SMB":Hlth_ew.coef_[1],"HML":Hlth_ew.coef_[2]}
Money= {"Intercept":Money_ew.intercept_, "Mkt-RF": Money_ew.coef_[0], "SMB":Money_ew.coef_[1],"HML":Money_ew.coef_[2]}
Other= {"Intercept":Other_ew.intercept_, "Mkt-RF": Other_ew.coef_[0], "SMB":Other_ew.coef_[1],"HML":Other_ew.coef_[2]}

                               

df_ew= pd.DataFrame({"NoDur":NoDur,"Dubl":Durbl,"Manuf":Manuf,"Enrgy":Enrgy,"Chems":Chems,"BusEq":BusEq,
                     "Telcm":Telcm,"Utils":Utils,"Shops":Shops,"Hlth":Hlth,"Money":Money,'Other':Other}).reset_index()
df_ew= round(df_ew,4)

model.fit(concat5factors[["Mkt-RF","SMB","HML","RMW","CMA"]],concat5factors.iloc[:,7:19])
model.intercept_
model.coef_

df5factors_vw= pd.DataFrame({"NoDur":{"intercept":model.intercept_[0],"Mkt":model.coef_[0,0],"SMB":model.coef_[0,1],
                      "HML":model.coef_[0,2],"RMW":model.coef_[0,3],"CMA":model.coef_[0,4]},
             "Durbl":{"intercept":model.intercept_[1],"Mkt":model.coef_[1,0],"SMB":model.coef_[1,1],
                      "HML":model.coef_[1,2],"RMW":model.coef_[1,3],"CMA":model.coef_[1,4]},
             "Manuf":{"intercept":model.intercept_[2],"Mkt":model.coef_[2,0],"SMB":model.coef_[2,1],
                      "HML":model.coef_[2,2],"RMW":model.coef_[2,3],"CMA":model.coef_[2,4]},
             "Enrgy":{"intercept":model.intercept_[3],"Mkt":model.coef_[3,0],"SMB":model.coef_[3,1],
                      "HML":model.coef_[3,2],"RMW":model.coef_[3,3],"CMA":model.coef_[3,4]},
             "Chems":{"intercept":model.intercept_[4],"Mkt":model.coef_[4,0],"SMB":model.coef_[4,1],
                      "HML":model.coef_[4,2],"RMW":model.coef_[4,3],"CMA":model.coef_[4,4]},
             "BusEq":{"intercept":model.intercept_[5],"Mkt":model.coef_[5,0],"SMB":model.coef_[5,1],
                      "HML":model.coef_[5,2],"RMW":model.coef_[5,3],"CMA":model.coef_[5,4]},
              "Telcm":{"intercept":model.intercept_[6],"Mkt":model.coef_[6,0],"SMB":model.coef_[6,1],
                      "HML":model.coef_[6,2],"RMW":model.coef_[6,3],"CMA":model.coef_[6,4]},
              "Utils":{"intercept":model.intercept_[7],"Mkt":model.coef_[7,0],"SMB":model.coef_[7,1],
                      "HML":model.coef_[7,2],"RMW":model.coef_[7,3],"CMA":model.coef_[7,4]},
              "Shops":{"intercept":model.intercept_[8],"Mkt":model.coef_[8,0],"SMB":model.coef_[8,1],
                      "HML":model.coef_[8,2],"RMW":model.coef_[8,3],"CMA":model.coef_[8,4]},
              "Hlth":{"intercept":model.intercept_[9],"Mkt":model.coef_[9,0],"SMB":model.coef_[9,1],
                      "HML":model.coef_[9,2],"RMW":model.coef_[9,3],"CMA":model.coef_[9,4]},
              "Money":{"intercept":model.intercept_[10],"Mkt":model.coef_[10,0],"SMB":model.coef_[10,1],
                      "HML":model.coef_[10,2],"RMW":model.coef_[10,3],"CMA":model.coef_[10,4]},
              "Other":{"intercept":model.intercept_[11],"Mkt":model.coef_[11,0],"SMB":model.coef_[11,1],
                      "HML":model.coef_[11,2],"RMW":model.coef_[11,3],"CMA":model.coef_[11,4]},
             }).reset_index()
df5factors_vw=round(df5factors_vw,4)

model.fit(concat5factors[["Mkt-RF","SMB","HML","RMW","CMA"]],concat5factors.iloc[:,19:31])
model.intercept_
model.coef_

df5factors_ew= pd.DataFrame({"NoDur":{"intercept":model.intercept_[0],"Mkt":model.coef_[0,0],"SMB":model.coef_[0,1],
                      "HML":model.coef_[0,2],"RMW":model.coef_[0,3],"CMA":model.coef_[0,4]},
             "Durbl":{"intercept":model.intercept_[1],"Mkt":model.coef_[1,0],"SMB":model.coef_[1,1],
                      "HML":model.coef_[1,2],"RMW":model.coef_[1,3],"CMA":model.coef_[1,4]},
             "Manuf":{"intercept":model.intercept_[2],"Mkt":model.coef_[2,0],"SMB":model.coef_[2,1],
                      "HML":model.coef_[2,2],"RMW":model.coef_[2,3],"CMA":model.coef_[2,4]},
             "Enrgy":{"intercept":model.intercept_[3],"Mkt":model.coef_[3,0],"SMB":model.coef_[3,1],
                      "HML":model.coef_[3,2],"RMW":model.coef_[3,3],"CMA":model.coef_[3,4]},
             "Chems":{"intercept":model.intercept_[4],"Mkt":model.coef_[4,0],"SMB":model.coef_[4,1],
                      "HML":model.coef_[4,2],"RMW":model.coef_[4,3],"CMA":model.coef_[4,4]},
             "BusEq":{"intercept":model.intercept_[5],"Mkt":model.coef_[5,0],"SMB":model.coef_[5,1],
                      "HML":model.coef_[5,2],"RMW":model.coef_[5,3],"CMA":model.coef_[5,4]},
              "Telcm":{"intercept":model.intercept_[6],"Mkt":model.coef_[6,0],"SMB":model.coef_[6,1],
                      "HML":model.coef_[6,2],"RMW":model.coef_[6,3],"CMA":model.coef_[6,4]},
              "Utils":{"intercept":model.intercept_[7],"Mkt":model.coef_[7,0],"SMB":model.coef_[7,1],
                      "HML":model.coef_[7,2],"RMW":model.coef_[7,3],"CMA":model.coef_[7,4]},
              "Shops":{"intercept":model.intercept_[8],"Mkt":model.coef_[8,0],"SMB":model.coef_[8,1],
                      "HML":model.coef_[8,2],"RMW":model.coef_[8,3],"CMA":model.coef_[8,4]},
              "Hlth":{"intercept":model.intercept_[9],"Mkt":model.coef_[9,0],"SMB":model.coef_[9,1],
                      "HML":model.coef_[9,2],"RMW":model.coef_[9,3],"CMA":model.coef_[9,4]},
              "Money":{"intercept":model.intercept_[10],"Mkt":model.coef_[10,0],"SMB":model.coef_[10,1],
                      "HML":model.coef_[10,2],"RMW":model.coef_[10,3],"CMA":model.coef_[10,4]},
              "Other":{"intercept":model.intercept_[11],"Mkt":model.coef_[11,0],"SMB":model.coef_[11,1],
                      "HML":model.coef_[11,2],"RMW":model.coef_[11,3],"CMA":model.coef_[11,4]},
              }).reset_index()

df5factors_ew=round(df5factors_ew,4)


tab= RollingOLS(concat5factors["NoDur_vw"],add_constant(concat5factors["CMA"]),window=50).fit().params.reset_index()
tab=tab.replace(tab.index,concat.date[10420:])




app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                prevent_initial_callbacks=True,suppress_callback_exceptions=True)
                
app.layout=(html.Div(
        className="page",
        children=[
            html.Div(className="border",
                     children=[
             html.Img(src="https://www.amse-aixmarseille.fr/sites/default/files/amse_logo.svg", style= {"width":"10%"},id="top"),
             html.A(html.Button("Learn more", className="learn-more-button"),
                    href="https://www.amse-aixmarseille.fr/en/",target="_blank"),
                    
             
            
    html.H1(children='Project about Kenneth French data library',style={"text-align":"center"}),
    html.Br(),
        html.A('Concatenation', href='#concatenation',className="Nav"),
        html.A('OLS Regression', href="#OLS Regression", className='Nav'),
        html.A('Rolling OLS',href="#rolling OLS", className="Nav"),
        html.A('State space', href='#state space', className='Nav')]),
        
        html.Div(
        className= "product",
        style={"border-radius":"10px","background":"red" },
        children=[
        html.H3("Project overview"),
        html.P(resume_project(), style={"color": "white"}, className="text")
        ]),
    
     html.Div(className="data table",
             children=[
   html.H4('Descriptions of the datasets', className="subtitle"),
   html.Div(
             children=[
                    html.Div(
                        children=[
                           get_data_table_description(),
                            ]
                        )
                    ])]),
    html.Div(className="sub-page",
    children=[
    html.H4("Members"),
    html.Div(style= {"width":"48%"},
             children=[
                 html.Div(
                        children=[
                            get_team_table_description()]
                            
                        )])]),
    html.Div(className= "TOC",
             children=[
    html.H4(children='Table of content', id="toc"),
    html.P(children='Step 1: Download automatically datasets from Kenneth French\'s website'),
    html.P(children='Step 2: Clean the data and compute the market risk premium'),
    html.P(children="Step 3: Allow the user to select one of the 12 portfolios,the 3 factors,equal weighted or value weighted"),
    html.P("and plot the estimated coeficients all along the period and the estimated coeficients on rolling window",style={"line-height":"20%"}),
    html.P(children="Step 4: estimate again the same model using State Space method, thanks to constants and betas estimated with random walks")   
    ]),
    html.Div(className= "Producer",
             children=[
    html.H4("Kenneth French Data Library:", id="producer"),
    html.Img(src= app.get_asset_url("website K.F.png"),style={"width":"30%"}),
    html.P("Kenneth French is an American economist born in 1954.", className='text'),
    html.P(" With Nobel 2013 Eugene Fama, he developped the Fama-French model with 3 factors.",className='text'),
    html.P('The website contains the model of Fama-French with 3 and 5 factors', className='text'),
    html.P("several portfolios and industry portfolios.",className='text'),
    html.P("This website updates once a month.",className='text'),
    html.A('Kenneth French data library', href='https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html',target="_blank"),
    ]),
    
# =============================================================================
#     Affichage des datasets concaténnés :
# =============================================================================

    html.Div(className="boards_and_graphs",
         children=[
             html.H2("Concatenation",id= "concatenation",className= "section_concatenation"),
             dbc.NavLink("Back to top",href="#concatenation", className="Link"),
    html.Div(className="boards",
             children=[ 
                 
                 html.H4('Concatenation of the 3 factors[daily] and the 12 industry portfolios[daily]'),
                 html.Div(dash_table.DataTable(
                     id='concat',
                     columns= [{"name":i, "id": i} for i in concat.columns],
                     data=concat.to_dict('records'),
                     page_size=6,
                     style_table={'overflowX': 'auto'})),
                 
                  html.H4('Concatenation of the 5 factors[daily] and the 12 industry portfolios[daily]'),
      html.Div(dash_table.DataTable(
          id="Industry_12_portfolios",
          columns= [{"name":i, "id": i} for i in concat5factors.columns],
          data=concat5factors.to_dict('records'),
          page_size=6,
          style_table={'overflowX': 'auto'})),
                 
                  html.H4('Concatenation of the 3 factors[daily], the 12 industry portfolios[daily] and the deviations with respect to RF for the State Space method'),
                  html.Div(dash_table.DataTable(	
         id='concatwithDev',
         columns=[{'name': i, 'id':i} for i in concatwithDev.columns],
         data= concatwithDev.to_dict('records'),
         page_size=6,
         style_table={'overflowX': 'auto'})),
                  
                  html.H4('Concatenation of the 5 factors[daily], the 12 industry portfolios and the deviations with respect to RF for the State Space method'),
                  html.Div(dash_table.DataTable(	
                      id='concat5factorswithDev',
                      columns=[{'name': i, 'id':i} for i in concat5factorswithMkt.columns],
                      data= concat5factorswithMkt.to_dict('records'),
                      page_size=6,
                      style_table={'overflowX': 'auto'})),
      
     html.Br(),
    
     
     ]),
              
     html.Br(),
     html.H2('OLS Regression', id='OLS Regression'),
   
     dbc.NavLink("Back to top", href="#top",external_link=True, className="Link"),
     dbc.NavLink('Concatenation',href="#concatenation",external_link=True, style={"margin-left":"1cm"}),
      
     html.Div(className="boards",
     children=[
         
         html.H4("Summary of the results of the regression of value weighted on the 3 factors:"),
         html.Div(dash_table.DataTable(
             id='OLSReg_vw',
             columns=[{'name': i, 'id':i} for i in df_vw.columns],
             data= df_vw.to_dict('records'),
             page_size=10,
             style_table={'overflowX': 'auto'}
                         )),
         html.Br(),
         html.Br(),
         html.H4("Summary of the results of the regression of equal weighted on the 3 factors:"),
         html.Div(dash_table.DataTable(	
             id='OLSReg_ew',
             columns=[{'name': i, 'id':i} for i in df_ew.columns],
             data= df_ew.to_dict('records'),
             style_table={'overflowX': 'auto'})),
         
         html.H4("Summary of the results of the regression of value weighted on the 5 factors:"),
         html.Div(dash_table.DataTable(	
             id='OLSReg5factors_vw',
             columns=[{'name': i, 'id':i} for i in df5factors_vw.columns],
             data= df5factors_vw.to_dict('records'),
             style_table={'overflowX': 'auto'})),
         
         html.H4("Summary of the results of the regression of equal weighted on the 5 factors:"),
         html.Div(dash_table.DataTable(	
             id='OLSReg5factors_ew',
             columns=[{'name': i, 'id':i} for i in df5factors_ew.columns],
             data= df5factors_ew.to_dict('records'),
             style_table={'overflowX': 'auto'})),
         
         
         
         ]),
     
     
     html.Br(),
     html.H2("Rolling OLS", id="rolling OLS"),
     dbc.Nav([
     dbc.NavLink("Back to top",href="#rolling OLS", className="Link"),
     dbc.NavLink("OLS Regression",href="#OLS Regression",external_link=True, className= "Link"),
     dbc.NavLink("Concatenation",href="#concatenation",external_link=True, className= "Link")
     ]),
     html.Br(),
     html.H4('Rolling OLS for 3 factors:', className= "title_tab"),
     html.Div(className="Tabs",
             children=[
         dcc.Tabs([
              dcc.Tab(label='Value Weighted',children=[
                  html.Div(dropdown_portfolios_3factors_vw),
                  html.Div(dropdown_3factors_vw),
                  html.Div(id="container-button-3factors_vw"),
                  html.Button("RolingOLS", id="3factors_vw", n_clicks=0, className= "buttonrolOLS"),
                  html.Div(id= "container-graph-3factors_vw"),
                  html.H4("Select a period of time:"),
                  html.Div(rangeSlider_vw,),
                  html.H4("Select a window:"),
                  dcc.Slider(id= "Window_vw",
                             min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)}, 
                             className="windowsilder_vw"),
              ]),
              
          dcc.Tab(label= 'Equal Weighted', children=[
              html.Div(dropdown_portfolios_3factors_ew),
              html.Div(dropdown_3factors_ew),
              html.Button("RolingOLS",id="3factors_ew",className="buttonrolOLS"),
              html.Div(id='container-button-3factors_ew'),
              html.Div(id="container-graph-3factors_ew"),
              html.H4("Select a period of time:"),
              html.Div(rangeSlider_ew),
              html.H4("Select a window:"),
              dcc.Slider(id= "Window_ew",
                         min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)})
           ])
              ])
             
         ]),
     html.Br(),
     html.Br(),
     html.H4('Rolling OLS for 5 factors:',className= "title_tab"),
      html.Div(className="Tabs",
             children=[
         dcc.Tabs([
              dcc.Tab(label='Value Weighted',children=[
              html.Div(dropdown_portfolios_5factors_vw),
              html.Div(dropdown_5factors_vw),
              dcc.Checklist(id="all-or-none",
                            options=[{"label": "Select All", "value": "All"}],
                            value=[],
                            labelStyle={"display": "inline-block"},
                            className="Select-all"),
              html.Div(id="container-button-5factors_vw"),
              html.Button("RolingOLS", id="5factors_vw", n_clicks=0, className= "buttonrolOLS"),
              html.Div(id= "container-graph-5factors_vw"),
              html.Div(id= "container-graph-rol-5factors_vw"),
              html.H4("Select a period of time:"),
              html.Div(rangeSlider_5factors_vw),
              html.H4("Select a window:"),
              dcc.Slider(id= "Window_5factors_vw",
                         min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)})
              ]),
              
          dcc.Tab(label= 'Equal Weighted', children=[
              html.Div(dropdown_portfolios_5factors_ew),
              html.Div(dropdown_5factors_ew),
              dcc.Checklist(id="checklist_5factors_ew",
                            options=[{"label": "Select All", "value": "All"}],
                            value=[],
                            labelStyle={"display": "inline-block"},
                            className="Select-all"),
              html.Button("RolingOLS",id="5factors_ew",className="buttonrolOLS"),
              html.Div(id='container-button-5factors_ew'),
              html.Div(id="container-graph-5factors_ew"),
              html.Div(id= "container-graph-rol-5factors_ew"),
              html.H4("Select a period of time:"),
              html.Div(rangeSlider_5factors_ew),
              html.H4("Select a window:"),
               dcc.Slider(id= "Window_5_factors_ew",
                          min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)})
           ])
              ])
             
         ]),
      html.Br(),
      html.Br(),
      html.H2("State Space", id="state space"),
dbc.Nav([
dbc.NavLink("Back to top",href="#state space", className="Link"),
dbc.NavLink("Rolling OLS",href= "#rolling OLS", external_link=True,className="Link"),
dbc.NavLink("OLS Regression",href= "#OLS Regression", external_link=True, className="Link"),
dbc.NavLink("Concatenation",href= "#concatenation", external_link=True,className="Link")
]),
              html.Div(className="Tabs_state_space", children=[
                         dcc.Tabs([                    
                             dcc.Tab(label= "3 factors", children=[
                                  dcc.Dropdown(id= "dropdown1SP",
                          options= [{"label": i, "value": i} for i in pd.concat([Firstpart, Secondpart]).columns],
                          multi= False,
                          placeholder="Select a portfolios...",
                          className= "dropdown_SP_portfolios"),
             dcc.Dropdown(id= "dropdown2SP",
                          options=({"label": "{Mkt}", "value": "{Mkt}"},
                                   {"label":"{SMB}", "value":"{SMB}"},
                                   {"label":"{HML}","value":"{HML}"},
                                   {"label":"{Mkt,SMB}","value":"{Mkt,SMB}"},
                                   {"label":"{Mkt,HML}","value":"{Mkt,HML}"},
                                   {"label":"{SMB,HML}","value":"{SMB,HML}"},
                                   {"label":"{Mkt,SMB,HML}","value":"{Mkt,SMB,HML}"}
                                   ),
                          multi= False,
                          placeholder="Select a factors...",
                          className= "dropdown_SP_factors"),
                          
             dcc.Dropdown(id= 'start_date',
                          options=[{'label':i, "value":i} for i in concat.date],
                          multi= False,
                          placeholder="Select a start date",
                          className= "dropdown_SP_start"),
             dcc.Dropdown(id= 'end_date',
                          options=[{'label':i, "value":i} for i in concat.date],
                          multi= False,
                          placeholder="Select an end date",
                          className="dropdown_SP_end"),
             html.Button("Run the batch file", id='run',n_clicks=0, className="ButtonRUN"),
             html.Button("Make graph",id="graph",n_clicks=0,className="ButtonGraph"),
             html.Button("Make table", id="table", n_clicks=0, className="ButtonTable "),
             html.Div(id='container-button'),
             html.Div(id= "container-button-table"),
             html.Div(id="container-graph-ox"),
                                 ]),
                             
                             dcc.Tab(label='5 factors', children=[
                                 dcc.Dropdown(id= "dropdown1SP_5factors",
                                              options= [{"label": i, "value": i} for i in pd.concat([Firstpart, Secondpart]).columns],
                                              multi= False,
                                              placeholder="Select a portfolios...",
                                              className= "dropdown_SP_portfolios"),
                                 dcc.Dropdown(id= "dropdown2SP_5factors",
                                              options=({"label": "{Mkt}", "value": "{Mkt}"},
                                                       {"label":"{SMB}", "value":"{SMB}"},
                                                       {"label":"{HML}","value":"{HML}"},
                                                       {"label":"{RMW}","value":"{RMW}"},
                                                       {"label":"{CMA}","value":"{CMA}"},
                                                       {"label":"{Mkt,SMB}","value":"{Mkt,SMB}"},
                                                       {"label":"{Mkt,HML}","value":"{Mkt,HML}"},
                                                       {"label":"{Mkt,RMW}","value":"{Mkt,RMW}"},
                                                       {"label":"{Mkt,CMA}","value":"{Mkt,CMA}"},
                                                       {"label":"{SMB,HML}","value":"{SMB,HML}"},
                                                       {"label":"{SMB,RMW}","value":"{SMB,RMW}"},
                                                       {"label":"{SMB,CMA}","value":"{SMB,CMA}"},
                                                       {"label":"{HML,RMW}","value":"{HML,RMW}"},
                                                       {"label":"{HML,CMA}","value":"{HML,CMA}"},                                                       
                                                       {"label":"{RMW,CMA}","value":"{RMW,CMA}"},
                                                       {"label":"{Mkt,SMB,HML}","value":"{Mkt,SMB,HML}"},
                                                       {"label":"{Mkt,SMB,HML,RMW}","value":"{Mkt,SMB,HML,RMW}"},
                                                       {"label":"{Mkt,SMB,HML,CMA}","value":"{Mkt,SMB,HML,CMA}"},                                                       
                                                       {"label":"{Mkt,SMB,HML,RMW,CMA}","value":"{Mkt,SMB,HML,RMW,CMA}"}),                                
                                              multi= False,
                                              placeholder="Select a factors...",
                                              className= "dropdown_SP_factors"),
                                 dcc.Dropdown(id= 'start_date_5factors',
                                              options=[{'label':i, "value":i} for i in concat5factors.date],
                                              multi= False,
                                              placeholder="Select a start date",
                                              className= "dropdown_SP_start"),
                                 dcc.Dropdown(id= 'end_date_5factors',
                                              options=[{'label':i, "value":i} for i in concat5factors.date],
                                              multi= False,
                                              placeholder="Select an end date",
                                              className="dropdown_SP_end"),
                                 html.Button("Run the batch file", id="run_5factors",n_clicks=0, className= "ButtonRUN"),
                                 html.Button("Make graph", id='graph_5factors',n_clicks=0,className="ButtonGraph"),
                                 html.Button("Make table", id="table_5factors", n_clicks=0, className="ButtonTable "),
                                 html.Div(id= "container-button-table_5factors"),
                                 html.Div(id='container-button_5factors'),
                                 html.Div(id="container-graph_5factors")
                                 
                                                                              
                                     ])
                                 ])
                             ])
                          ]),
        html.H2("Glossary",className="Glossary",id="glossary"),
        html.A("Back to top",href="#top",className="Link"),
        html.A('Concatenation', href='#concatenation',className="Link"),
        html.A('OLS Regression', href="#OLS Regression", className='Link'),
        html.A('Rolling OLS',href="#rolling OLS", className="Link"),
        html.A('State space', href='#state space', className='Link'),
        html.H4("Fama/French 3 factors[daily]",className="subtitle_glossary"),
        html.Div(className="Descriptions",children=[
            html.P("Mkt-RF:the market risk premium"),
            html.P("SMB(Small Minus Big):the average return on the three small portfolios minus the average return on the three big portfolios"),
            html.P("HML(High Minus Low): the average return on the two value portfolios minus the average return on the two growth portfolios"),
            html.P("RF:the risk free rate; rate of return of an investissment without risk of loss.")]),
        html.Br(),
        html.H4("Fama/French 5 factors (2x3)[daily]",className="subtitle_glossary"),
        html.Div(className="Descriptions",children=[
            html.P("SMB (Small Minus Big): the average return on the nine small stock portfolios minus the average return on the nine big stock portfolios"),
            html.P("HML (High Minus Low): the average return on the two value portfolios minus the average return on the two growth portfolios"),
            html.P("RMW (Robust Minus Weak): the average return on the two robust operating profitability portfolios minus the average return on the two weak operating profitability portfolios"),
            html.P("CMA (Conservative Minus Aggressive): the average return on the two conservative investment portfolios minus the average return on the two aggressive investment portfolios")]),
        html.H4("12 Industry Portfolios[daily]",className="subtitle_glossary"),
        html.Div(className="Descriptions",children=[
            html.P("NoDur:consumer not durables"),
            html.P("Durbl:consumer durables"),
            html.P("Manuf:manufacturing goods"),
            html.P("Enrgy:energy goods"),
            html.P("Chems:chemical goods"),
            html.P("BusEq:business equipment"),
            html.P("Telcm:telephone and television transmission"),
            html.P("Utils:utilities"),
            html.P("Shops:retail and others services"),
            html.P("Hilth:healthcare goods"),
            html.P("Money:financial goods"),
            html.P("Other:others goods and services like transports, hotels, constructions...")]),
            html.P("© Thomas Mille - all rights reserved", style={"text-align":"center"}),
            html.A(html.Img(src="/assets/LinkedIn-logo.png", style={"width":"2cm"}),href="https://www.linkedin.com/in/thomas-mill%C3%A9-baabb01ba/",target="_blank", title="Contact me"),
            html.A(html.Img(src="/assets/Github.png",style={"width":"1cm"}), href="https://github.com/cayenne97/projet-stage", target="_blank", title="You can see my code here"),


dbc.Nav([
        dbc.NavLink('Go to top',href="#top",external_link=True,className="top")])

        
]))
     



@app.callback(
    Output("container-button","children"),
    Input("run","n_clicks"),
    State("dropdown1SP",'value'),
    State("dropdown2SP",'value'),
    State("start_date",'value'),
    State("end_date",'value'),
    prevent_initial_call=True
    
    )
    
def displayclick(n_clicks,portefolios,value,start_date,end_date):
    os.chdir('C:/Users/thoma/OneDrive/Bureau/projet/ox')
    myfile= open("runoxwin.bat","r")
    list_of_line= myfile.readlines()
    list_of_line[4]="SET firstday={start}\n".format(start=start_date)
    list_of_line[5]="SET lastday={end}\n".format(end=end_date)
    list_of_line[6]="SET namesY={value}\n".format(value=portefolios)
    list_of_line[7]="SET namesX={factors}\n".format(factors=value)
    myfile= open("runoxwin.bat","w")
    myfile.writelines(list_of_line)
    myfile.close()
    csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas", "*.csv"))
    latest_file= max(csv_files,key= os.path.getmtime)
    df= pd.read_csv(latest_file).drop("Unnamed: 0",axis=1)
    if n_clicks>0:
        return (
               os.startfile("runoxwin.bat"),
               os.remove(max(csv_files,key= os.path.getmtime)))
@app.callback(
    Output("container-button-table","children"),
    Input("table","n_clicks"))
def make_table_3_factors(n_clicks): 
    csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas", "*.csv"))
    latest_file= max(csv_files,key= os.path.getmtime)
    df= round(pd.read_csv(latest_file).drop("Unnamed: 0",axis=1),5)
    if n_clicks>0:
        return dash_table.DataTable(id='SF',
                                  columns=[{'name':i,"id":i} for i in df.columns],
                                  data= df.to_dict('records'),
                                  page_size=10)
                                  
                       
@app.callback(
    Output("container-graph-ox","children"),
    State('dropdown2SP','value'),
    Input("graph","n_clicks"),
    prevent_initial_call=True
    
    )
def update_graph(value,n_clicks):
     csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas", "*.csv"))
     latest_file= max(csv_files,key= os.path.getmtime)
     df= pd.read_csv(latest_file).drop("Unnamed: 0",axis=1)
     if n_clicks>0:
        if value=="{Mkt,SMB,HML}":
           SFF1= px.line(df, x="Date",y= "Constant")
           SFF2= px.line(df, x="Date",y= "Mkt")
           SFF3= px.line(df, x="Date",y= "SMB")
           SFF4= px.line(df, x="Date",y= "HML")
           return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure= SFF2),
                    dcc.Graph(figure=SFF3),
                    dcc.Graph(figure=SFF4))
                   
        if value=="{Mkt,SMB}":
            SFF1= px.line(df, x="Date",y= "Constant")
            SFF2= px.line(df, x="Date",y= "Mkt")
            SFF3= px.line(df, x="Date",y= "SMB")
            return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure= SFF2),
                    dcc.Graph(figure=SFF3))
        if value=="{Mkt,HML}":
            SFF1= px.line(df, x="Date",y= "Constant")
            SFF2= px.line(df, x="Date",y= "Mkt")
            SFF4= px.line(df, x="Date",y= "HML")
            return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure= SFF2),
                    dcc.Graph(figure=SFF4))
        if value=="{SMB,HML}":
            SFF1= px.line(df, x="Date",y= "Constant")
            SFF3= px.line(df, x="Date",y= "SMB") 
            SFF4= px.line(df, x="Date",y= "HML")
            return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure=SFF3),
                    dcc.Graph(figure=SFF4))
        if value=="{Mkt}":
            SFF1= px.line(df, x="Date",y= "Constant")
            SFF2= px.line(df, x="Date",y= "Mkt")
            return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure= SFF2))
        if value=="{SMB}":
            SFF1= px.line(df, x="Date",y= "Constant")
            SFF3= px.line(df, x="Date",y= "SMB")
            return (dcc.Graph(figure= SFF1),
                    dcc.Graph(figure=SFF3))
         
        if value=="{HML}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML")
             return (dcc.Graph(figure=SFF1),
                     dcc.Graph(figure=SFF4))

@app.callback(
    Output("container-button_5factors","children"),
    Input("run_5factors","n_clicks"),
    State("dropdown1SP_5factors",'value'),
    State("dropdown2SP_5factors",'value'),
    State("start_date_5factors",'value'),
    State("end_date_5factors",'value'),
    prevent_initial_call=True)
    
    
def displayclick_5factors(n_clicks,portefolios,value,start_date,end_date):
    os.chdir('C:/Users/thoma/OneDrive/Bureau/projet/ox')
    myfile= open("runoxwin1.bat","r")
    list_of_line= myfile.readlines()
    list_of_line[4]="SET firstday={start}\n".format(start=start_date)
    list_of_line[5]="SET lastday={end}\n".format(end=end_date)
    list_of_line[6]="SET namesY={value}\n".format(value=portefolios)
    list_of_line[7]="SET namesX={factors}\n".format(factors=value)
    myfile= open("runoxwin1.bat","w")
    myfile.writelines(list_of_line)
    myfile.close()
    csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas1", "*.csv"))
    latest_file= max(csv_files,key= os.path.getmtime)
    df= pd.read_csv(latest_file).drop("Unnamed: 0",axis=1)
    if n_clicks>0:
        return (os.startfile("runoxwin1.bat"),
                os.remove(max(csv_files,key= os.path.getmtime)))
                
               

@app.callback(
    Output("container-graph_5factors","children"),
    Input("graph_5factors","n_clicks"),
    State('dropdown2SP_5factors','value'),
    prevent_initial_call=True)
    
def update_graph_5factors(n_clicks, value):
     csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas1", "*.csv"))
     latest_file= max(csv_files,key= os.path.getmtime)
     df= pd.read_csv(latest_file).drop("Unnamed: 0",axis=1)
     if n_clicks>0:
         if value=="{Mkt,SMB,HML}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF3= px.line(df, x="Date",y= "SMB")
             SFF4= px.line(df, x="Date",y= "HML")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4))
         if value=="{Mkt,SMB,HML,RMW}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF3= px.line(df, x="Date",y= "SMB")
             SFF4= px.line(df, x="Date",y= "HML")
             SFF5= px.line(df,x="Date",y= "RMW")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF5))
         
         if value=="{Mkt,SMB,HML,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF3= px.line(df, x="Date",y= "SMB")
             SFF4= px.line(df, x="Date",y= "HML")
             SFF6= px.line(df,x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF6))
         
         if value=="{Mkt,SMB,HML,RMW,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF3= px.line(df, x="Date",y= "SMB")
             SFF4= px.line(df, x="Date",y= "HML")
             SFF5= px.line(df,x="Date",y= "RMW")
             SFF6= px.line(df,x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF5),
                     dcc.Graph(figure=SFF6))
                   
         if value=="{Mkt,SMB}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF3= px.line(df, x="Date",y= "SMB")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF3))
         
         if value=="{Mkt,HML}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF4= px.line(df, x="Date",y= "HML")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF4))
         
         if value=="{Mkt,RMW}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF5= px.line(df, x="Date",y= "RMW")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF5))
         
         if value=="{Mkt,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             SFF6= px.line(df,x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2),
                     dcc.Graph(figure=SFF6))
                             
         if value=="{SMB,HML}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF3= px.line(df, x="Date",y= "SMB") 
             SFF4= px.line(df, x="Date",y= "HML")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4))
         
         if value=="{SMB,RMW}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF3= px.line(df, x="Date",y= "SMB") 
             SFF4= px.line(df, x="Date",y= "RMW")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4))
         
         if value=="{SMB,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF3= px.line(df, x="Date",y= "SMB") 
             SFF4= px.line(df, x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF3),
                     dcc.Graph(figure=SFF4))
         
         if value=="{HML,Mkt}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML") 
             SFF2= px.line(df, x="Date",y= "Mkt")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF2))
         
         if value=="{HML,SMB}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML") 
             SFF3= px.line(df, x="Date",y= "SMB")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF3))
         
         if value=="{HML,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML") 
             SFF6= px.line(df, x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF6))
         
         if value=="{HML,RMW}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML") 
             SFF5= px.line(df, x="Date",y= "RMW")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF4),
                     dcc.Graph(figure=SFF5))
         
         if value=="{RMW,CMA}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF5= px.line(df, x="Date",y= "RMW") 
             SFF6= px.line(df, x="Date",y= "CMA")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF5),
                     dcc.Graph(figure=SFF6))
                     
         
         if value=="{Mkt}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF2= px.line(df, x="Date",y= "Mkt")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure= SFF2))
         
         if value=="{SMB}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF3= px.line(df, x="Date",y= "SMB")
             return (dcc.Graph(figure= SFF1),
                     dcc.Graph(figure=SFF3))
         
         if value=="{HML}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "HML")
             return (dcc.Graph(figure=SFF1),
                     dcc.Graph(figure=SFF4))
         if value=="{RMW}":
             SFF1= px.line(df, x="Date",y= "Constant")
             SFF4= px.line(df, x="Date",y= "RMW")
             return (dcc.Graph(figure=SFF1),
                     dcc.Graph(figure=SFF4))
         
         if value=="{CMA}":
              SFF1= px.line(df, x="Date",y= "Constant")
              SFF4= px.line(df, x="Date",y= "CMA")
              return (dcc.Graph(figure=SFF1),
                      dcc.Graph(figure=SFF4))
@app.callback(
Output("container-button-table_5factors","children"),
Input("table_5factors","n_clicks"))

def make_table_5factors(n_clicks):
    csv_files = glob.glob(os.path.join("C:/Users/thoma/OneDrive/Bureau/projet/ox/betas1", "*.csv"))
    latest_file= max(csv_files,key= os.path.getmtime)
    df= round(pd.read_csv(latest_file).drop("Unnamed: 0",axis=1),5)  
    if n_clicks>0:
        return(dash_table.DataTable(id='SF',
                                  columns=[{'name':i,"id":i} for i in df.columns],
                                  data= df.to_dict('records'),
                                  page_size=10,
                                  ))
        
@app.callback(
    Output("container-graph-3factors_vw","children"),
    Input("3factors_vw","n_clicks"),
    State("Portfolios_vw","value"),
    State("dropdown_vw","value"),
    Input('my_rangeslider_vw',"value"),
    Input("Window_vw","value"),
    prevent_initial_call=True
    )

def make_graphics_vw(n_clicks, Portfolios_vw_value,dropdown_value, year, window_vw):
     exog= add_constant(concat[dropdown_value])
     tab= RollingOLS(concat[Portfolios_vw_value],exog, window=window_vw)
     tab= tab.fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3"})
     tab['year']=tab.index.year
     tab= tab[(tab["year"] >= year[0]) & (tab["year"] <= year[1])]
       
     if n_clicks>0:
             
             if dropdown_value==["Mkt-RF"]:
                 
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return (dcc.Graph(figure=fig1),
                    dcc.Graph(figure=fig2))
             
             elif dropdown_value==["SMB"]:
                fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],annotation_font_size=14,annotation_font_color="red")
                                                                                   
                return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig3))
            
             elif dropdown_value==["HML"]:
         
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                      annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],annotation_font_size=14,annotation_font_color="red")
                 return (dcc.Graph(figure=fig1),
                  dcc.Graph(figure=fig4))
            
            
             elif dropdown_value==["Mkt-RF","SMB"] :
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2),
                        dcc.Graph(figure=fig3))
             
             elif dropdown_value==["Mkt-RF","HML"]:
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2),
                        dcc.Graph(figure=fig4))
             elif dropdown_value==["SMB","HML"]:
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig3),
                        dcc.Graph(figure=fig4))
             
             elif dropdown_value==["Mkt-RF","SMB","HML"] :
                 fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red") 
                 fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[2],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_vw_value]).coef_[2],
                                                                                   annotation_font_size=14,annotation_font_color="red") 
                 return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3),
                 dcc.Graph(figure=fig4))
             
         
@app.callback(
    Output("container-graph-3factors_ew","children"),
    Input("3factors_ew","n_clicks"),
    State("Portfolios_ew","value"),
    State("dropdown_ew","value"),
    Input('my_rangeslider_ew',"value"),
    Input("Window_ew","value"),
    prevent_initial_call=True
    )
        

def updategraph_ew(n_clicks,Portfolios_ew_value,dropdown_value, year, window_ew):
    tab= RollingOLS(concat[Portfolios_ew_value],add_constant(concat[dropdown_value]), window=window_ew)
    tab= tab.fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3"})
    tab['year']=tab.index.year
    tab= tab[(tab["year"] >= year[0]) & (tab["year"] <= year[1])]
    

    if n_clicks>0:
        if dropdown_value==["Mkt-RF"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                          annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                          annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2))
        
        elif dropdown_value==["SMB"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig3))
        
        elif dropdown_value==["HML"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                      annotation_text= model.fit(concat[dropdown_value],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                  dcc.Graph(figure=fig4))
        
        elif dropdown_value==["Mkt-RF","SMB"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF',"SMB"]],concat[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3))
      
        elif dropdown_value==["Mkt-RF","HML"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                         annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig4))
        elif dropdown_value==["SMB","HML"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                         annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF','HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4))
     
        elif dropdown_value==["Mkt-RF","SMB","HML"]:
            fig1= px.line(tab,x= tab.index, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                            annotation_text= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.index, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.index, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                    annotation_text= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[1],
                                                                                       annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.index, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[2],
                                                                                     annotation_text= model.fit(concat[['Mkt-RF',"SMB",'HML']],concat[Portfolios_ew_value]).coef_[2],
                                                                                     annotation_font_size=14,annotation_font_color="red") 
            return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3),
                 dcc.Graph(figure=fig4))
        
@app.callback(
     Output("dropdown_5_factors_vw","value"),
     Input('all-or-none',"value"),
     State("dropdown_5_factors_vw", "options")
     )
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [options["value"] for options in options if all_selected]
    return all_or_none
   
        
@app.callback(
    Output("container-graph-rol-5factors_vw","children"),
    Input("5factors_vw","n_clicks"),
    State("Portfolios_5factors_vw","value"),
    State("dropdown_5_factors_vw","value"),
    Input("my_rangeslider_5factors_vw","value"),
    Input("Window_5factors_vw","value"),
    prevent_initial_call=True
    )  
      
def make_graphics_5_factors_vw(n_clicks, Portfolios_vw_value,dropdown_5factors,year, window_vw):
    tab1= RollingOLS(concat5factors[Portfolios_vw_value],add_constant(concat5factors[dropdown_5factors]),window=window_vw).fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3","RMW":"Bêta4", "CMA": "Bêta5"}).reset_index()
    tab1=tab1.replace(tab1.index,concat.date[10420:])
    tab1["year"]=concat.index[10420:].year
    tab1= tab1[(tab1["year"] >= year[0]) & (tab1["year"] <= year[1])]
    if n_clicks>0:
        if dropdown_5factors==["Mkt-RF"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                            annotation_text= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2))
        
        elif dropdown_5factors==["SMB"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig3))
        
        elif dropdown_5factors==["HML"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig4))
        
        elif dropdown_5factors==["RMW"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig5))
        
        elif dropdown_5factors==["CMA"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                    dcc.Graph(figure=fig6))
        
        elif dropdown_5factors==["Mkt-RF","SMB"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig3))
        
        elif dropdown_5factors==["Mkt-RF","HML"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig4))
         
        elif dropdown_5factors==["Mkt-RF","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["Mkt-RF","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig6))         
                          
         
        elif dropdown_5factors==["SMB","HML"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig4))
         
        elif dropdown_5factors==["SMB","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["SMB","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["RMW","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["Mkt-RF","SMB","HML"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig3),
                    dcc.Graph(figure=fig4)
                    )
        
        elif dropdown_5factors==["Mkt-RF","SMB","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["Mkt-RF","SMB","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["Mkt-RF","HML","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["Mkt-RF","HML","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["Mkt-RF","RMW","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["SMB","HML","RMW"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["SMB","HML","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["SMB","RMW","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","RMW","CMA"]:
             fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
         
         
        elif dropdown_5factors==["Mkt-RF","SMB","HML","RMW"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig5))
        
        elif dropdown_5factors==["Mkt-RF","SMB","HML","CMA"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig6))
                 
        elif dropdown_5factors==["Mkt-RF","SMB","HML","RMW","CMA"]:
            fig1=px.line(tab1, x="index",y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab1, x="index",y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red") 
            fig3=px.line(tab1, x="index",y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab1, x="index",y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab1, x="index",y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab1, x="index",y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[4],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_vw_value]).coef_[4],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig5),
                   dcc.Graph(figure=fig6))
@app.callback(
     Output("dropdown_5_factors_ew","value"),
     Input('checklist_5factors_ew',"value"),
     State("dropdown_5_factors_ew", "options")
     )
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [options["value"] for options in options if all_selected]
    return all_or_none        
        
        
@app.callback(
    Output("container-graph-rol-5factors_ew","children"),
    Input("5factors_ew","n_clicks"),
    State("Portfolios_5factors_ew","value"),
    State("dropdown_5_factors_ew","value"),
    Input("my_rangeslider_5factors_ew","value"),
    Input("Window_5_factors_ew","value"),
    prevent_initial_call=True
    )  
      
def make_graphics_5_factors_ew(n_clicks, Portfolios_ew_value,dropdown_5factors,year, window_vw):
    tab_ew= RollingOLS(concat5factors[Portfolios_ew_value],add_constant(concat5factors[dropdown_5factors]),window=window_vw).fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3","RMW":"Bêta4", "CMA": "Bêta5"})
    tab_ew["index"]=concat.index[10420:].date
    tab_ew["year"]=concat.index[10420:].year
    tab_ew= tab_ew[(tab_ew["year"] >= year[0]) & (tab_ew["year"] <= year[1])]
    if n_clicks>0:
        if dropdown_5factors==["Mkt-RF"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                            annotation_text= model.fit(concat5factors[['Mkt-RF']],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                            annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2))
        
        elif dropdown_5factors==["SMB"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[['SMB']],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig3))
        
        elif dropdown_5factors==["HML"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig4))
        
        elif dropdown_5factors==["RMW"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig5))
        
        elif dropdown_5factors==["CMA"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                    dcc.Graph(figure=fig6))
        
        elif dropdown_5factors==["Mkt-RF","SMB"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig3))
        
        elif dropdown_5factors==["Mkt-RF","HML"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig4))
                  
        elif dropdown_5factors==["Mkt-RF","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["Mkt-RF","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig6))
        elif dropdown_5factors==["SMB","HML"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig4))
         
        elif dropdown_5factors==["SMB","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["SMB","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["RMW","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             
             return (dcc.Graph(figure=fig1),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["Mkt-RF","SMB","HML"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure= fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig3),
                    dcc.Graph(figure=fig4)
                    )
        
        elif dropdown_5factors==["Mkt-RF","SMB","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["Mkt-RF","SMB","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig6))
        elif dropdown_5factors==["Mkt-RF","HML","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig5))
        elif dropdown_5factors==["Mkt-RF","HML","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["Mkt-RF","RMW","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig5),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["SMB","HML","RMW"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig3),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig5))
         
        elif dropdown_5factors==["SMB","HML","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
        elif dropdown_5factors==["SMB","RMW","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
         
        elif dropdown_5factors==["HML","RMW","CMA"]:
             fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
             return (dcc.Graph(figure= fig1),
                     dcc.Graph(figure=fig2),
                     dcc.Graph(figure=fig4),
                     dcc.Graph(figure=fig6))
         
         
         
        elif dropdown_5factors==["Mkt-RF","SMB","HML","RMW"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig5))
        
        elif dropdown_5factors==["Mkt-RF","SMB","HML","CMA"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig6))
                 
        elif dropdown_5factors==["Mkt-RF","SMB","HML","RMW","CMA"]:
            fig1=px.line(tab_ew, x=tab_ew["index"],y="intercept" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2=px.line(tab_ew, x=tab_ew["index"],y="Bêta1" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[0],
                                                                                  annotation_font_size=14,annotation_font_color="red") 
            fig3=px.line(tab_ew, x=tab_ew["index"],y="Bêta2" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[1],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4=px.line(tab_ew, x=tab_ew["index"],y="Bêta3" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[2],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig5=px.line(tab_ew, x=tab_ew["index"],y="Bêta4" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[3],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig6=px.line(tab_ew, x=tab_ew["index"],y="Bêta5" ).add_hline(y= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[4],
                                                                                           annotation_text= model.fit(concat5factors[dropdown_5factors],concat5factors[Portfolios_ew_value]).coef_[4],
                                                                                  annotation_font_size=14,annotation_font_color="red")
            
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4),
                   dcc.Graph(figure=fig5),
                   dcc.Graph(figure=fig6))        
        
        
             
if __name__ == '__main__': 
    app.run_server(debug=True,use_reloader=False) 
