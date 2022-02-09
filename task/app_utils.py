# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 16:47:29 2021

@author: thoma
"""

from dash import html, dcc
import pandas as pd

ff_factors= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip",
               skiprows = 3,index_col=0).drop("Copyright 2021 Kenneth R. French",axis=0)
ff_factors= round(ff_factors,3)

Industry_12= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/12_Industry_Portfolios_daily_CSV.zip",
                     skiprows = 9,index_col=0,sep='\s*,\s*',engine='python').drop("Copyright 2021 Kenneth R. French",axis=0)

ff_factors_5= pd.read_csv("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip",skiprows=3,index_col=0)
          


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    html_row = [html.Td([col]) for col in df.columns]
    table = [html.Tr(html_row)]
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
    
def generate_table(dataframe,max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns
                    ])
            ),      
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])





def get_team_table_description(): 
    return html.Table(
        [html.Thead([
            html.Th(''),
            html.Th('Names')
            ]
        ),
        html.Tbody([
            html.Tr(
                [html.Td('Intern'),
                 html.Td("MILLE Thomas")]
              ),
            html.Tr(
                [html.Td("Tutor"),
                 html.Td("Tanguy VAN YPERSELE"),
                 ]
                ),
            html.Tr(
                [html.Td("Manager"),
                 html.Td("Sébastien LAURENT")]
                ),
            ]
        )
     ]
)
def get_data_table_description():
    return html.Table(
        [
            html.Thead(
                 [html.Th(''),
                  html.Th('dataset 1 '),
                  html.Th("dataset 2"),
                  html.Th("dataset 3")
                  ],
                 ),
            html.Tbody([
                html.Tr([
                    html.Td("Producer"),
                    html.Td("Kenneth French data library"),
                    html.Td("Kenneth French data library"),
                    html.Td("Kenneth French data library")]
                    ),
                html.Tr(
                    [html.Td('Names'),
                     html.Td('Fama/French 3 Factors[daily]'),
                     html.Td('Fama/French 5 Factors[daily]'),
                     html.Td('12 Industry Portfolios[daily] ')]
                    ),
                html.Tr(
                    [html.Td('Observations'),
                     html.Td(ff_factors.shape[0]),
                     html.Td(ff_factors_5.shape[0]),
                     html.Td(Industry_12.shape[0])
                     ]
                    ),
                html.Tr(
                    [html.Td("Variables"),
                     html.Td(ff_factors.shape[1]),
                     html.Td(ff_factors_5.shape[1]),
                     html.Td(Industry_12.shape[1])
                     ]
                    ),
                     
            
                ]
            )
        ]
    )


def resume_project(): 
    p=(
    html.P("This project consists in downloading and analyzing several datasets from a website untitled Kenneth French data library."),
    html.P("We will analyse the datasets using the OLS regression, on the estimated intercept and the estimated betas all along the period first and then on the estimated intercept and the"), 
    html.P("estimated betas on Rolling windows and we will plot the results."),
    html.P("Then, we will implement an other method called State Space with some random walk."))
    return p  

