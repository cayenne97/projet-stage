# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 11:24:04 2021

@author: thoma
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from dash import dcc
from datetime import date
import sys, os, subprocess

ff_factors= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip",
               skiprows = 3,index_col=0).drop("Copyright 2021 Kenneth R. French",axis=0)
ff_factors= round(ff_factors,3)

ff_factors_5= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",skiprows=3,index_col=0)
                    

Industry_12= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/12_Industry_Portfolios_daily_CSV.zip",
                     skiprows = 9,index_col=0,sep='\s*,\s*',engine="python").drop("Copyright 2021 Kenneth R. French",axis=0)

Industry_12=Industry_12.apply(pd.to_numeric,errors='coerce')

Firstpart=Industry_12[0:round(Industry_12.shape[0]/2)-1].rename(columns= {'NoDur':'NoDur_vw',"Durbl":"Durbl_vw","Manuf":"Manuf_vw", 
                                              "Enrgy":"Enrgy_vw","Chems":"Chems_vw","BusEq":"BusEq_vw",
                                             "Telcm":"Telcm_vw","Utils":"Utils_vw","Shops":"Shops_vw","Hlth":"Hlth_vw"
                                              ,"Money":"Money_vw","Other":"Other_vw"})
Firstpart= Firstpart.dropna()

Secondpart=Industry_12[round(Industry_12.shape[0]/2)+1:].rename(columns={'NoDur':'NoDur_ew',"Durbl":"Durbl_ew","Manuf":"Manuf_ew", 
                                              "Enrgy":"Enrgy_ew","Chems":"Chems_ew","BusEq":"BusEq_ew",
                                             "Telcm":"Telcm_ew","Utils":"Utils_ew","Shops":"Shops_ew","Hlth":"Hlth_ew"
                                             ,"Money":"Money_ew","Other":"Other_ew"})
Secondpart= Secondpart.dropna()

Industry_12_vw_1963_2021= Firstpart[10420:].dropna()
Industry_12_ew_1963_2021= Secondpart[10420:].dropna()



# =============================================================================
# concat= pd.concat([ff_factors, Firstpart, Secondpart],axis=1).reset_index() # Alow to see the index.
# concat["index"]= pd.to_datetime(concat["index"],errors='coerce')
# concat['date']= concat['index'].dt.date
# concat.set_index('index', inplace=True)
# concat['year']=concat.index.year
# =============================================================================

déviations_vw= pd.DataFrame({'DevNoDDur_vw':Firstpart["NoDur_vw"] - ff_factors["RF"],
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

concatDev= pd.concat([déviations_vw, déviations_ew],axis=1).reset_index()
concatDev["index"]= pd.to_datetime(concatDev["index"]).dt.date

concat= pd.concat([ff_factors, Firstpart, Secondpart],axis=1).reset_index() # Alow to see the index.
concat["index"]= pd.to_datetime(concat["index"],errors='coerce')
concat['date']= concat['index'].dt.date
concat.set_index('index', inplace=True)
concat['year']=concat.index.year
concat.insert(0, 'date', concat.pop("date"))

concat5factors= pd.concat([ff_factors_5.reset_index(drop=True),Industry_12_vw_1963_2021.reset_index(),Industry_12_ew_1963_2021.reset_index(drop=True)],axis=1)
concat5factors["index"]=pd.to_datetime(concat5factors["index"],errors="coerce").dt.date
concat5factors= concat5factors.rename(columns={"index":"date"})
concat5factors.insert(0, 'date', concat5factors.pop("date"))

concatwithDev=pd.concat([ff_factors,Firstpart, Secondpart,déviations_vw, déviations_ew],axis=1).reset_index()
concatwithDev["index"]= pd.to_datetime(concatwithDev["index"]).dt.date
concatwithDev=concatwithDev.rename(columns={'index':'date','Mkt-RF':'Mkt'})
concatwithDev.to_csv("C:/Users/thoma/OneDrive/Bureau/projet/ox/data/concat.csv ")

concat5factorswithDev=pd.concat([ff_factors_5.reset_index(drop=True),Industry_12_vw_1963_2021.reset_index(),Industry_12_ew_1963_2021.reset_index(drop=True)],axis=1)
concat5factorswithDev["index"]= pd.to_datetime(concat5factorswithDev["index"]).dt.date
concat5factorswithDev=concat5factorswithDev.rename(columns={'index':'date','Mkt-RF':'Mkt'})
concat5factorswithDev.insert(0, 'date', concat5factorswithDev.pop("date"))

concat5factorswithDev["devNoDur_vw"]=concat5factors["NoDur_vw"] - concat5factors["RF"]
concat5factorswithDev["devManuf_vw"]=concat5factors["Manuf_vw"] - concat5factors["RF"]
concat5factorswithDev["devEnrgy_vw"]=concat5factors["Enrgy_vw"] - concat5factors["RF"]
concat5factorswithDev["devChems_vw"]=concat5factors["Chems_vw"] - concat5factors["RF"]
concat5factorswithDev["devBusEq_vw"]=concat5factors["BusEq_vw"] - concat5factors["RF"]
concat5factorswithDev["devTelcm_vw"]=concat5factors["Telcm_vw"] - concat5factors["RF"]
concat5factorswithDev["devUrils_vw"]=concat5factors["Utils_vw"] - concat5factors["RF"]
concat5factorswithDev["devShops_vw"]=concat5factors["Shops_vw"] - concat5factors["RF"]
concat5factorswithDev["devMoney_vw"]=concat5factors["Money_vw"] - concat5factors["RF"]
concat5factorswithDev["devOther_vw"]=concat5factors["Other_vw"] - concat5factors["RF"]
concat5factorswithDev["devNoDur_ew"]=concat5factors["NoDur_ew"] - concat5factors["RF"]
concat5factorswithDev["devManuf_ew"]=concat5factors["Manuf_ew"] - concat5factors["RF"]
concat5factorswithDev["devEnrgy_ew"]=concat5factors["Enrgy_ew"] - concat5factors["RF"]
concat5factorswithDev["devChems_ew"]=concat5factors["Chems_ew"] - concat5factors["RF"]
concat5factorswithDev["devBusEq_ew"]=concat5factors["BusEq_ew"] - concat5factors["RF"]
concat5factorswithDev["devTelcm_ew"]=concat5factors["Telcm_ew"] - concat5factors["RF"]
concat5factorswithDev["devUtils_ew"]=concat5factors["Utils_ew"] - concat5factors["RF"]
concat5factorswithDev["devShops_ew"]=concat5factors["Shops_ew"] - concat5factors["RF"]
concat5factorswithDev["devMoney_ew"]=concat5factors["Money_ew"] - concat5factors["RF"]
concat5factorswithDev["devOther_ew"]=concat5factors["Other_ew"] - concat5factors["RF"]
concat5factorswithDev= round(concat5factorswithDev,3)

concat5factorswithDev.to_csv("C:/Users/thoma/OneDrive/Bureau/projet/ox/data/concat5factorswithDev.csv")

# =============================================================================
# y= concat["NoDur_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# res= model.fit(X,y)
# print(res.coef_)
# print(res.intercept_)
# 
# y= concat["Durbl_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Durbl_vw= model.fit(X,y)
# print(Durbl_vw.coef_)
# print(Durbl_vw.intercept_)
# 
# y= concat["Manuf_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Manuf_vw= model.fit(X,y)
# print(Manuf_vw.coef_)
# print(Manuf_vw.intercept_)
# 
# y= concat["Enrgy_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Enrgy_vw= model.fit(X,y)
# print(Enrgy_vw.coef_)
# print(Enrgy_vw.intercept_)
# 
# y= concat["Chems_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Chems_vw= model.fit(X,y)
# print(Chems_vw.coef_)
# print(Chems_vw.intercept_)
# 
# y= concat["BusEq_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# BusEq_vw= model.fit(X,y)
# print(BusEq_vw.coef_)
# print(BusEq_vw.intercept_)
# 
# y= concat["Telcm_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Telcm_vw= model.fit(X,y)
# print(Telcm_vw.coef_)
# print(Telcm_vw.intercept_)
# 
# y= concat["Utils_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Utils_vw= model.fit(X,y)
# print(Utils_vw.coef_)
# print(Utils_vw.intercept_)
# 
# y= concat["Shops_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Shops_vw= model.fit(X,y)
# print(Shops_vw.coef_)
# print(Shops_vw.intercept_)
# 
# y= concat["Hlth_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Hlth_vw= model.fit(X,y)
# print(Hlth_vw.coef_)
# print(Hlth_vw.intercept_)
# 
# y= concat["Money_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Money_vw= model.fit(X,y)
# print(Money_vw.coef_)
# print(Money_vw.intercept_)
# 
# y= concat["Other_vw"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Other_vw= model.fit(X,y)
# print(Other_vw.coef_)
# print(Other_vw.intercept_)
# 
# y= concat["NoDur_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# NoDur_ew= model.fit(X,y)
# print(NoDur_ew.coef_)
# print(NoDur_ew.intercept_)
# 
# y= concat["Durbl_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Durbl_ew= model.fit(X,y)
# print(Durbl_ew.coef_)
# print(Durbl_ew.intercept_)
# 
# y= concat["Manuf_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Manuf_ew= model.fit(X,y)
# print(Manuf_ew.coef_)
# print(Manuf_ew.intercept_)
# 
# y= concat["Enrgy_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Enrgy_ew= model.fit(X,y)
# print(Enrgy_ew.coef_)
# print(Enrgy_ew.intercept_)
# 
# y= concat["Chems_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Chems_ew= model.fit(X,y)
# print(Chems_ew.coef_)
# print(Chems_ew.intercept_)
# 
# y= concat["BusEq_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# BusEq_ew= model.fit(X,y)
# print(BusEq_ew.coef_)
# print(BusEq_ew.intercept_)
# 
# y= concat["Telcm_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Telcm_ew= model.fit(X,y)
# print(Telcm_ew.coef_)
# print(Telcm_ew.intercept_)
# 
# y= concat["Utils_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Utils_ew= model.fit(X,y)
# print(Utils_ew.coef_)
# print(Utils_ew.intercept_)
# 
# y= concat["Shops_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Shops_ew= model.fit(X,y)
# print(Shops_ew.coef_)
# print(Shops_ew.intercept_)
# 
# y= concat["Hlth_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Hlth_ew= model.fit(X,y)
# print(Hlth_ew.coef_)
# print(Hlth_ew.intercept_)
# 
# y= concat["Money_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Money_ew= model.fit(X,y)
# print(Money_ew.coef_)
# print(Money_ew.intercept_)
# 
# y= concat["Other_ew"]
# X= concat[["Mkt-RF","SMB","HML"]]
# model= LinearRegression()
# Other_ew= model.fit(X,y)
# print(Other_ew.coef_)
# print(Other_ew.intercept_)
# =============================================================================


# =============================================================================
# List of Dropdowns
# =============================================================================

dropdown_portfolios_3factors_vw= dcc.Dropdown(
    id= 'Portfolios_vw',
    options=[{'label':i, 'value':i} for i in Firstpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling"),


dropdown_portfolios_3factors_ew= dcc.Dropdown(
    id= 'Portfolios_ew',
    options=[{'label':i, 'value':i} for i in Secondpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling"),

dropdown_3factors_vw=dcc.Dropdown(
    id= 'dropdown_vw',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors',
    )

dropdown_3factors_ew=dcc.Dropdown(
    id= 'dropdown_ew',
    options=({'label': "Mkt-RF", 'value':"Mkt-RF"},
             {"label": "SMB", "value": "SMB"},
             {"label": "HML", "value": "HML"}),
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors',
    )
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
                    min= concat["year"].min(),
                    max= concat["year"].max(),
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
                    min= concat["year"].min(),
                    max= concat["year"].max(),
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
picker= dcc.DatePickerRange(id="Mypicker",
    min_date_allowed=date(1926,7,1),
    max_date_allowed=date(2021,10,29),
    initial_visible_month= date(1926,7,1),
    display_format= "YYYY-MM-DD",
    start_date=date(1926,7,1),
    end_date=date(2010,10,29)),

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

def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


        

#For MACOS:
    
# =============================================================================
# with open("runoxmac1", "rt") as bat_file:
#     text = bat_file.readlines()
# 
#     new_text = []
# for line in text:
#     if "Manuf_ew" in line:
#         new_text.append(line.replace("Manuf_ew", "Manuf_vw"))
#     elif "{Mkt,SMB}" in line:
#         new_text.append(line.replace("{Mkt,SMB}", "{Mkt,SMB,HML}"))   
#     elif "1926-07-01" in line:
#          new_text.append(line.replace("1926-07-01", "1926-07-01"))
#     elif "2021-10-28" in line:
#         new_text.append(line.replace("2021-10-27", "2021-10-27")) 
#     else:
#         new_text.append(line)
# 
# with open("runoxmac1", "wt") as bat_file:
#     for line in new_text:
#         bat_file.write(line)
#         
# with open("runoxmac2", "rt") as bat_file:
#     text = bat_file.readlines()
# 
#     new_text = []
# for line in text:
#     if "Manuf_ew" in line:
#         new_text.append(line.replace("Manuf_ew", "Manuf_vw"))
#     elif "{Mkt,SMB,HML}" in line:
#         new_text.append(line.replace("{Mkt,SMB,HML}", "{Mkt,SMB}"))   
#     elif "1926-07-01" in line:
#          new_text.append(line.replace("1926-07-01", "1926-07-01"))
#     elif "2021-10-27" in line:
#         new_text.append(line.replace("2021-10-27", "2021-10-27")) 
#     else:
#         new_text.append(line)
# 
# with open("runoxmac2", "wt") as bat_file:
#     for line in new_text:
#         bat_file.write(line)
# =============================================================================


