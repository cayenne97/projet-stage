
import dash
from dash import dcc, html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from IPython.display import clear_output
from datetime import datetime as dt
from statsmodels.regression.rolling import RollingOLS
from sklearn.linear_model import LinearRegression
from statsmodels.tools import add_constant
from datetime import date
import datetime,glob
import pandas as pd
import os,sys
import plotly.express as px

os.chdir('/home/thomas973/mysite/')
parent_path = os.path.dirname('task/')
sys.path.append(parent_path)
from app_utils import (dataframe_linReg3factors,dataframe_linReg3factors_ew,dataframe_linReg5factors_vw,table_of_content,get_data_table_description,
get_team_table_description,resume_project,ff_factors_def,industry_12_def,ff_factors_5_def,concat,concat5factors,concat_3factors_and_dev,
concat_5factors_and_dev)


# =============================================================================
# Téléchargement des bases de données:
# =============================================================================

# Fama_French 3 and 5 Factors[daily]:
ff_factors_def()
ff_factors_5_def()

# 12 Industry Portfolios[daily]:
industry_12_def()

# =============================================================================
# Séparation de la base de données "12 Industry Portofolios[daily]" en Average Value Weighted Returns (vw)
# et Average Equal Weighted Returns (ew)
# =============================================================================
index=industry_12_def()[industry_12_def()["index"]=="Average Equal Weighted Returns -- Daily"].index[0]

Firstpart=industry_12_def()[0:index].rename(columns= {'NoDur':'NoDur_vw',"Durbl":"Durbl_vw","Manuf":"Manuf_vw",
                                              "Enrgy":"Enrgy_vw","Chems":"Chems_vw","BusEq":"BusEq_vw",
                                             "Telcm":"Telcm_vw","Utils":"Utils_vw","Shops":"Shops_vw","Hlth":"Hlth_vw"
                                              ,"Money":"Money_vw","Other":"Other_vw"})

Secondpart=industry_12_def()[index:].rename(columns={'NoDur':'NoDur_ew',"Durbl":"Durbl_ew","Manuf":"Manuf_ew",
                                              "Enrgy":"Enrgy_ew","Chems":"Chems_ew","BusEq":"BusEq_ew",
                                             "Telcm":"Telcm_ew","Utils":"Utils_ew","Shops":"Shops_ew","Hlth":"Hlth_ew"
                                             ,"Money":"Money_ew","Other":"Other_ew"})
Secondpart.dropna(inplace=True)
index_1963_vw=Firstpart[Firstpart["index"]=="19630701"].index[0]
index_1963_ew=Secondpart[Secondpart["index"]=="19630701"].index[0]
Secondpart.dropna(inplace=True)

Industry_12_vw_1963_2021= Firstpart.loc[index_1963_vw:].dropna()
Industry_12_ew_1963_2021= Secondpart.loc[index_1963_ew:].dropna()
Industry_12_vw_1963_2021.reset_index(inplace=True,drop=True)
Industry_12_ew_1963_2021.reset_index(inplace=True,drop=True)

# =============================================================================
# List of Dropdowns
# =============================================================================

dropdown_portfolios_vw_3factors= dcc.Dropdown(
    id= 'Portfolios_vw_3factors',
    options=[{'label':i, 'value':i} for i in Firstpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_portfolios_vw_5factors= dcc.Dropdown(
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_portfolios_ew_3factors= dcc.Dropdown(
    id= 'Portfolios_ew_3factors',
    options=[{'label':i, 'value':i} for i in Secondpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown_portfolios_ew_5factors= dcc.Dropdown(
    id= 'Portfolios_ew_5factors',
    options=[{'label':i, 'value':i} for i in Secondpart.columns],
    multi= False,
    placeholder="Select a portefolio...",
    style={'width':'40%'},
    className= "portfolios_rolling")

dropdown3factors_vw=dcc.Dropdown(
    id= 'dropdown_3factors_vw',
    options=[({'label':i, 'value':i}) for i in ff_factors_def().columns],
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

dropdown5factors_vw=dcc.Dropdown(
    id= 'dropdown_5factors_vw',
    options=[({'label':i, 'value':i}) for i in ff_factors_5_def().columns],
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

dropdown3factors_ew=dcc.Dropdown(
    id= 'dropdown_3factors_ew',
    options=[({'label':i, 'value':i}) for i in ff_factors_def().columns],
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

dropdown5factors_ew=dcc.Dropdown(
    id= 'dropdown_5factors_ew',
    options=[({'label':i, 'value':i}) for i in ff_factors_5_def().columns],
    multi= True,
    placeholder="Select a factor...",
    className= 'dropdown_factors')

# =============================================================================
# Range slider
# =============================================================================
rangeSlider_vw= dcc.RangeSlider(id='my_rangeslider_vw',
                    min= concat()["year"].min(),
                    max= concat()["year"].max(),
                    value= [1926,concat()["date"].iloc[-1].year],
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
                    min= concat()["year"].min(),
                    max= concat()["year"].max(),
                    value= [1926,concat()["year"].iloc[-1]],
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
                    min= concat().year[10420:].min(),
                    max= concat().year[10420:].max(),
                    value= [1963,2022],
                    marks={1963: {"label": "1963"},
                           1970: {"label": "1970"},
                           1980: {"label": "1980"},
                           1990: {"label": "1990"},
                           2000: {"label": "2000"},
                           2010: {"label": "2010"},
                           2020: {"label": "2020"}}),

rangeSlider_5factors_ew= dcc.RangeSlider(id='my_rangeslider_5factors_ew',
                    min= concat().year[10420:].min(),
                    max= concat().year[10420:].max(),
                    value= [1963,2022],
                    marks={1963: {"label": "1963"},
                           1970: {"label": "1970"},
                           1980: {"label": "1980"},
                           1990: {"label": "1990"},
                           2000: {"label": "2000"},
                           2010: {"label": "2010"},
                           2020: {"label": "2020"}})
model= LinearRegression()
# =============================================================================
# Start of the code:
# =============================================================================
app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width", "title":"Project about K.f"}],
                prevent_initial_callbacks=True,suppress_callback_exceptions=True)
app.title="project about K.F"
app.description="my app's description"

app.layout=(html.Div(
        className="page",
        children=[
            html.Div(className="border",
                     children=[
             html.Img(src="/assets/amse_logo.svg", style= {"width":"10%"},id="top"),
             html.A(html.Button("Learn more", className="learn-more-button"),
                    href="https://www.amse-aixmarseille.fr/en/",target="_blank"),

    html.H1(children='Kenneth French data library',style={"text-align":"center"}),
    html.Br(),
    html.Div(className="Nav",children=[
        html.A('Concatenation', href='#concatenation'),
        html.A('OLS Regression', href="#OLS Regression",className="Nav"),
        html.A('Rolling OLS',href="#rolling OLS",className="Nav"),
        html.A('State space', href='#state space',className="Nav"),
        html.A('Glossary',href='#glossary',className="Nav"),
        html.A("Contact",href='mailto:thomas.mille973@gmail.com',className="Nav")]),

        html.P("Last update:"+datetime.datetime.now().strftime("%B")+" "+str(datetime.datetime.now().year))]),
        html.Div(className= "product",
        style={"border-radius":"10px","background":"red" },
        children=[
        html.H3("Project overview"),
        html.P(resume_project(), style={"color": "white"}, className="text")
        ]),

     html.Div(children=[
                 html.H4('Descriptions of the datasets', className="subtitle"),
                 html.Div(children=[
                          html.Div( className="data_table",
                          children=[get_data_table_description()]),
                    ])]),
    html.Div(className="sub-page",
    children=[
    html.H4("Members"),
    html.Div(style= {"width":"35%","position":"relative","top":"1cm"},
             children=[get_team_table_description()])]),

    html.Div(className= "TOC",
             children=[
    html.H4(children='Table of content', id="toc"),
    html.P("Step 1: Download automatically datasets from Kenneth French\'s website."),
    html.P("Step 2: Clean the data (remove the first and the last lines of each dataset)"),
    html.P("Step 3: Separate the 12 industry portfolios into two categories: equal weighted (ew) or value weighted (vw))"),
    html.P("Step 4: Compute the market risk premium (the deviations with respect to RF)"),
    html.P("Step 5: Allow the user to select one of the 12 portfolios (equal weighted or value weighted) and the 3 factors"),
    html.P("Step 6: Plot the estimated coeficients all along the period and the estimated coeficients on rolling window."),
    html.P("Step 7: Estimate again the same model using state space method, thanks to constants and betas estimated with random walks."),
    ]),
    html.Div(className= "Producer",
             children=[
    html.H4("Kenneth French Data Library:", id="producer"),
    html.Img(src= app.get_asset_url("website K.F.png"),style={"width":"30%"}),
    html.Div(children=[
    html.P(table_of_content())]),
    html.A('Kenneth French data library', href='https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html',target="_blank"),
    ]),
# =============================================================================
#     Affichage des datasets :
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
                     columns= [{"name":i, "id": i} for i in concat().columns],
                     data=concat().to_dict('records'),
                     page_size=6,
                     style_table={'overflowX': 'auto'})),

                  html.H4('Concatenation of the 5 factors[daily] and the 12 industry portfolios[daily]'),
      html.Div(dash_table.DataTable(id="Industry_12_portfolios",
          columns= [{"name":i, "id": i} for i in concat5factors().columns],
          data=concat5factors().to_dict('records'),
          page_size=6,
          style_table={'overflowX': 'auto'})),

                  html.H4('Concatenation of the 3 factors[daily], the 12 industry portfolios[daily] and the deviations with respect to RF for the State Space method'),
                  html.Div(dash_table.DataTable(id='concatwithDev',
         columns=[{'name': i, 'id':i} for i in concat_3factors_and_dev().columns],
         data= concat_3factors_and_dev().to_dict('records'),
         page_size=6,
         style_table={'overflowX': 'auto'})),

                  html.H4('Concatenation of the 5 factors[daily], the 12 industry portfolios and the deviations with respect to RF for the State Space method'),
                  html.Div(dash_table.DataTable(id='concat5factorswithDev',
                      columns=[{'name': i, 'id':i} for i in concat_5factors_and_dev().columns],
                      data= concat_5factors_and_dev().to_dict('records'),
                      page_size=6,
                      style_table={'overflowX': 'auto'})),
     html.Br(),
     ]),

     html.Br(),
     html.H2('OLS Regression', id='OLS Regression'),
     html.A("Back to top", href="#top", className="Link"),
     html.A('Concatenation',href="#concatenation", style={"margin-left":"1cm"}),

     html.Div(className="boards",
     children=[
         html.H4("Summary of the results of the regression of value weighted on the 3 factors:"),
         html.Div(dash_table.DataTable(
             id='OLSReg_vw',
             columns=[{'name': i, 'id':i} for i in dataframe_linReg3factors().columns],
             data= dataframe_linReg3factors().to_dict('records'),
             page_size=10,
             style_table={'overflowX': 'auto'}
                         )),
         html.H4("Summary of the results of the regression of equal weighted on the 3 factors:"),
         html.Div(dash_table.DataTable(
             id='OLSReg_ew',
             columns=[{'name': i, 'id':i} for i in  dataframe_linReg3factors_ew().columns],
             data=  dataframe_linReg3factors_ew().to_dict('records'),
             style_table={'overflowX': 'auto'})),

         html.H4("Summary of the results of the regression of value weighted on the 5 factors:"),
         html.Div(dash_table.DataTable(id='OLSReg5factors_vw',columns=[{'name': i, 'id':i} for i in dataframe_linReg5factors_vw().columns],
         data= dataframe_linReg5factors_vw().to_dict('records'),
         style_table={'overflowX': 'auto'})),

        #  html.Div(dash_table.DataTable(
        #      id='OLSReg5factors_vw',
        #      columns=[{'name': i, 'id':i} for i in df5factors_vw.columns],
        #      data= df5factors_vw.to_dict('records'),
        #      style_table={'overflowX': 'auto'})),

        #  html.H4("Summary of the results of the regression of equal weighted on the 5 factors:"),
        #  html.Div(dash_table.DataTable(
        #      id='OLSReg5factors_ew',
        #      columns=[{'name': i, 'id':i} for i in df5factors_ew.columns],
        #      data= df5factors_ew.to_dict('records'),
        #      style_table={'overflowX': 'auto'})),
         ]),
     html.Br(),
     html.H2("Rolling OLS", id="rolling OLS"),
     html.A("Back to top",href="#top", className="Link"),
     html.A("OLS Regression",href="#OLS Regression",className= "Link"),
     html.A("Concatenation",href="#concatenation", className= "Link"),
     html.Br(),
     html.H4('Rolling OLS for 3 factors:', className= "title_tab"),
     html.Div(className="Tabs",
             children=[
         dcc.Tabs([
              dcc.Tab(label='Value Weighted',children=[
                  html.Div(dropdown_portfolios_vw_3factors),
                  html.Div(dropdown3factors_vw),
                  html.Div(id="container-button-3factors_vw"),
                  html.Button("RolingOLS", id="3factors_vw", n_clicks=0, className= "buttonrolOLS"),
                  html.Button("tab",id="table_click", n_clicks=0),
                  html.Div(id= "container-graph-3factors_vw"),
                  html.Div(id="display_tab"),
                  html.H4("Select a period of time:"),
                  html.Div(rangeSlider_vw),
                  html.H4("Select a window:"),
                  dcc.Slider(id= "Window_vw",
                             min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)},
                             className="windowsilder_vw"),
              ]),

          dcc.Tab(label= 'Equal Weighted', children=[
              html.Div(dropdown_portfolios_ew_3factors),
              html.Div(dropdown3factors_ew),
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
              html.Div(dropdown_portfolios_vw_5factors),
              html.Div(dropdown5factors_vw),
              dcc.Checklist(id="all-or-none",
                            options=[{"label": "Select All", "value": "All"}],
                            value=[],
                            labelStyle={"display": "inline-block"},
                            className="Select-all"),
              html.Div(id="container-button-5factors_vw"),
              html.Button("RolingOLS", id="5factors_vw", n_clicks=0, className= "buttonrolOLS_5factors"),
              html.Div(id= "container-graph-5factors_vw"),
              html.Div(id= "container-graph-rol-5factors_vw"),
              html.H4("Select a period of time:"),
              html.Div(rangeSlider_5factors_vw),
              html.H4("Select a window:"),
              dcc.Slider(id= "Window_5factors_vw",
                         min=0, max=400, value= 50,marks= {i*10: str(i*10) for i in range(0,41)})
              ]),

          dcc.Tab(label= 'Equal Weighted', children=[
              html.Div(dropdown_portfolios_ew_5factors),
              html.Div(dropdown5factors_ew),
              dcc.Checklist(id="checklist_5factors_ew",
                            options=[{"label": "Select All", "value": "All"}],
                            value=[],
                            labelStyle={"display": "inline-block"},
                            className="Select-all"),
              html.Button("RolingOLS",id="5factors_ew",className="buttonrolOLS_5factors"),
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
html.A("Back to top",href="#top", className="Link"),
html.A("Rolling OLS",href= "#rolling OLS",className="Link"),
html.A("OLS Regression",href= "#OLS Regression",className="Link"),
html.A("Concatenation",href= "#concatenation",className="Link"),
html.A("open the software", href="https://www.oxrun.dev",className="Link"),

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
                          options=[{'label':i, "value":i} for i in concat().date],
                          multi= False,
                          placeholder="Select a start date",
                          className= "dropdown_SP_start"),
             dcc.Dropdown(id= 'end_date',
                          options=[{'label':i, "value":i} for i in concat().date],
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
                                              options=[{'label':i, "value":i} for i in concat5factors().date],
                                              multi= False,
                                              placeholder="Select a start date",
                                              className= "dropdown_SP_start"),
                                 dcc.Dropdown(id= 'end_date_5factors',
                                              options=[{'label':i, "value":i} for i in concat5factors().date],
                                              multi= False,
                                              placeholder="Select an end date",
                                              className="dropdown_SP_end"),
                                 html.Button("Run the batch file", id="run_5factors",n_clicks=0, className= "ButtonRUN"),
                                 html.Button("Make graph", id='graph_5factors',n_clicks=0,className="ButtonGraph"),
                                 html.Button("Make table", id="table_5factors", n_clicks=0, className="ButtonTable "),
                                 html.Div(id= "container-button-table_5factors"),
                                 html.Div(id='container-button_5factors'),
                                 html.Div(id="container-graph_5factors")])])])]),

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
            html.P("RF:the risk free rate; rate of return of an investissment without risk of loss."),
            html.P("Formula of the 3 factors model: Rt= RF+β1(Mkt-RF)+β2(SMB)+β3(HML)"),
            html.P("OLS Regression used: y=β0+β1X1+β2X2+β3X3+u"),
            html.P("CAPM model: E(Ra) = RF + βa(E(Rm) − RF)" )]),

        html.H4("Fama/French 5 factors (2x3)[daily]",className="subtitle_glossary"),
        html.Div(className="Descriptions",children=[
            html.P("SMB (Small Minus Big): the average return on the nine small stock portfolios minus the average return on the nine big stock portfolios"),
            html.P("HML (High Minus Low): the average return on the two value portfolios minus the average return on the two growth portfolios"),
            html.P("RMW (Robust Minus Weak): the average return on the two robust operating profitability portfolios minus the average return on the two weak operating profitability portfolios"),
            html.P("CMA (Conservative Minus Aggressive): the average return on the two conservative investment portfolios minus the average return on the two aggressive investment portfolios"),
            html.P("Formula of the 5 factors model: Rt= RF+β1(Mkt-RF)+β2(SMB)+β3(HML)+β4(RMW)+β5(CMA)+u"),
            html.P("OLS Regression used:y=β+β1X1+β2X2+β4X4+β5X5+u")]),

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
            html.P("Other:others goods and services like transports, hotels, constructions..."),
            html.P("The deviations are equal to the value of a portfolio subtracted by the value of the risk-free rate."),

            html.H4("Rolling window method"),
            html.P("This method was proposed by Fama and MacBeth in 1973. In a simple OLS regression, the estimated betas are contants over the period of time."),
            html.P("As betas may vary over time, the assumption according to which the betas are constant become wrong. This method consists in selecting a window,"),
            html.P("of observations and to apply an OLS regression over the first observations, then the window is rolled, and we repeat the same process until the end of the period."),
            html.P("The 24 portfolios are the dependent variables,the 3 and 5 factors are the independent variables."),

            html.H4("State Space method"),
            html.P("The state space method is a method suggested by Adrian and Franzoni in 2009. It comes from the conditional CAPM, and it consists in 2 equations: "),
            html.Img(src="/assets/state space method.jpg",style= {"width": "4cm"}),
            html.P("The state space equations are caracterized by 3 properties: forecasting, filtering and smoothing."),
            html.P("In a state space model, betas are computed following a random walk process")]),

            html.Div(className="border",children=[
            html.P("© Thomas MILLÉ - February 2022.",style={"text-align":"center"}),
            html.P("MÉGA - 424 chemin du Viaduc,13080 Aix-en-Provence""",style={"text-align":"center"}),
            html.A(html.Img(src="/assets/LinkedIn-logo.png", style={"width":"2cm"}),href="https://www.linkedin.com/in/thomas-mill%C3%A9-baabb01ba/",target="_blank", title="Contact me"),
            html.A(html.Img(src="/assets/Github.png",style={"width":"1cm"}), href="https://github.com/cayenne97/projet-stage", target="_blank", title="You can see my code here"),
            html.A('Go to top',href="#top",className="top")])
]))

# =============================================================================
# Callbacks for the State Space method
# =============================================================================

#=============================================================================
# Run the batch file "runoxwin.bat"
# =============================================================================
@app.callback(
    Output("container-button","children"),
    Input("run","n_clicks"),
    State("dropdown1SP",'value'),
    State("dropdown2SP",'value'),
    State("start_date",'value'),
    State("end_date",'value'),
    prevent_initial_call=True)

def displayclick(n_clicks,portefolios,value,start_date,end_date):
    os.chdir('/home/thomas973/mysite/ox')
    myfile= open("runoxwin.java","r")
    list_of_line= myfile.readlines()
    list_of_line[4]="String firstday={start}\n".format(start=start_date)
    list_of_line[5]="String lastday={end}\n".format(end=end_date)
    list_of_line[6]="String namesY={value}\n".format(value=portefolios)
    list_of_line[7]="String namesX={factors}\n".format(factors=value)
    myfile= open("runoxwin.java","w")
    myfile.writelines(list_of_line)
    myfile.close()
    csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas", "*.csv"))
    latest_file= min(csv_files,key= os.path.getmtime)
    df= pd.read_csv(latest_file).drop("Unnamed: 0",axis=1)
    if n_clicks>0:
        return (os.startfile("runoxwin.java")),

# =============================================================================
# Create the table with the data from the betas files
# =============================================================================
@app.callback(
    Output("container-button-table","children"),
    Input("table","n_clicks"))

def make_table_3_factors(n_clicks):
    csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas", "*.csv"))
    latest_file= min(csv_files,key= os.path.getmtime)
    df= round(pd.read_csv(latest_file).drop("Unnamed: 0",axis=1),5)
    if n_clicks>0:
        return dash_table.DataTable(id='SF',
                                  columns=[{'name':i,"id":i} for i in df.columns],
                                  data= df.to_dict('records'),
                                  page_size=10)

# =============================================================================
# Plotting the graphs from the betas files
# =============================================================================
@app.callback(
    Output("container-graph-ox","children"),
    State('dropdown2SP','value'),
    Input("graph","n_clicks"),
    prevent_initial_call=True)

def update_graph(value,n_clicks):
     csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas", "*.csv"))
     latest_file= min(csv_files,key= os.path.getmtime)
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
        if not value:
            return clear_output()

@app.callback(
    Output("container-button_5factors","children"),
    Input("run_5factors","n_clicks"),
    State("dropdown1SP_5factors",'value'),
    State("dropdown2SP_5factors",'value'),
    State("start_date_5factors",'value'),
    State("end_date_5factors",'value'),
    prevent_initial_call=True)


def displayclick_5factors(n_clicks,portefolios,value,start_date,end_date):
    os.chdir('/home/thomas973/mysite/ox')
    myfile= open("runoxwin1.bat","r")
    list_of_line= myfile.readlines()
    list_of_line[4]="SET firstday={start}\n".format(start=start_date)
    list_of_line[5]="SET lastday={end}\n".format(end=end_date)
    list_of_line[6]="SET namesY={value}\n".format(value=portefolios)
    list_of_line[7]="SET namesX={factors}\n".format(factors=value)
    myfile= open("runoxwin1.bat","w")
    myfile.writelines(list_of_line)
    myfile.close()
    csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas1", "*.csv"))
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
     csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas1", "*.csv"))
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
         if not value:
             return clear_output()
@app.callback(
Output("container-button-table_5factors","children"),
Input("table_5factors","n_clicks"))

def make_table_5factors(n_clicks):
    csv_files = glob.glob(os.path.join("/home/thomas973/mysite/ox/betas1", "*.csv"))
    latest_file= max(csv_files,key= os.path.getmtime)
    df= round(pd.read_csv(latest_file).drop("Unnamed: 0",axis=1),5)
    if n_clicks>0:
        return(dash_table.DataTable(id='SF',
                                  columns=[{'name':i,"id":i} for i in df.columns],
                                  data= df.to_dict('records'),
                                  page_size=10,
                                  ))
# =============================================================================
# Callbacks for the Rolling OLS method for the 3 factors and value weighted.
# =============================================================================

@app.callback(
Output("display_tab","children"),
Input("table_click","n_clicks"),
State("Portfolios_vw_3factors","value"),
State("dropdown_3factors_vw","value"),
Input("Window_vw","value"),
prevent_initial_call=True)

def make_table(n_clicks,dropdown_value,Portfolios_vw_value,window_vw):
    exog= add_constant(concat()[Portfolios_vw_value])
    tab= RollingOLS(concat()[dropdown_value],exog, window=window_vw)
    tab= tab.fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3"})
    tab['year']=concat()["date"]
    if n_clicks>0:
        return (dash_table.DataTable(id='SF',
                                  columns=[{'name':i,"id":i} for i in tab.columns],
                                  data= tab.to_dict('records'),
                                  ))
@app.callback(
    Output("container-graph-3factors_vw","children"),
    Input("3factors_vw","n_clicks"),
    State("Portfolios_vw_3factors","value"),
    State("dropdown_3factors_vw","value"),
    Input('my_rangeslider_vw',"value"),
    Input("Window_vw","value"),
    prevent_initial_call=True)

def make_graphics_vw(n_clicks, Portfolios_vw_value,dropdown_value, year, window_vw):
     exog= add_constant(concat()[dropdown_value])
     tab= RollingOLS(concat()[Portfolios_vw_value],exog, window=window_vw)
     tab= tab.fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3"})
     tab['year']=pd.to_datetime(concat()["date"]).dt.year
     tab= tab[(tab["year"] >= year[0]) & (tab["year"] <= year[1])]
     régression_intercept= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_
     régression_béta1=model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0]

     if n_clicks>0:
             if dropdown_value==["Mkt-RF"]:
                 fig1= px.line(tab,x= tab["year"], y="intercept",labels={"index":'date'}).add_hline(y=régression_intercept ,annotation_text=régression_intercept,
                                                                                        annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab["year"], y="Bêta1",labels={"index":'date'}).add_hline(y= régression_béta1, annotation_text= régression_béta1,
                                                                                        annotation_font_size=14,annotation_font_color="red")
                 return (dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2))

             elif dropdown_value==["SMB"]:
                fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y=régression_intercept,annotation_text=régression_intercept,
                                                                                        annotation_font_size=14,annotation_font_color="red")
                fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y=régression_béta1,annotation_text=régression_béta1,annotation_font_size=14,annotation_font_color="red")

                return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig3))

             elif dropdown_value==["HML"]:

                 fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                      annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],annotation_font_size=14,annotation_font_color="red")
                 return (dcc.Graph(figure=fig1),
                  dcc.Graph(figure=fig4))


             elif dropdown_value==["Mkt-RF","SMB"] :
                 fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2),
                        dcc.Graph(figure=fig3))

             elif dropdown_value==["Mkt-RF","HML"]:
                 fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig2),
                        dcc.Graph(figure=fig4))
             elif dropdown_value==["SMB","HML"]:
                 fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                        dcc.Graph(figure=fig3),
                        dcc.Graph(figure=fig4))

             elif dropdown_value==["Mkt-RF","SMB","HML"] :
                 fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
                 fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y=model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[2],
                                                                                    annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_vw_value]).coef_[2],
                                                                                   annotation_font_size=14,annotation_font_color="red")
                 return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3),
                 dcc.Graph(figure=fig4))

             elif dropdown_value=="":
                 return ""

# =============================================================================
# Callbacks for the Rolling OLS method for the 3 factors and equal weighted
# =============================================================================
@app.callback(
    Output("container-graph-3factors_ew","children"),
    Input("3factors_ew","n_clicks"),
    State("Portfolios_ew_3factors","value"),
    State("dropdown_3factors_ew","value"),
    Input('my_rangeslider_ew',"value"),
    Input("Window_ew","value"),
    prevent_initial_call=True
    )


def updategraph_ew(n_clicks,Portfolios_ew_value,dropdown_value, year, window_ew):
    tab= RollingOLS(concat()[Portfolios_ew_value],add_constant(concat()[dropdown_value]), window=window_ew)
    tab= tab.fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3"})
    tab['year']=pd.to_datetime(concat()["date"]).dt.year
    tab= tab[(tab["year"]>= year[0]) & (tab["year"] <= year[1])]

    if n_clicks>0:
        if dropdown_value==["Mkt-RF"]:
            fig1= px.line(tab,x=tab.year, y="intercept",labels={"index":'date'}).add_hline(y=model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,
            annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y=model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],
                                                                                          annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2))

        elif dropdown_value==["SMB"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig3))

        elif dropdown_value==["HML"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],
                                                                                      annotation_text= model.fit(concat()[dropdown_value],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return (dcc.Graph(figure=fig1),
                  dcc.Graph(figure=fig4))

        elif dropdown_value==["Mkt-RF","SMB"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF',"SMB"]],concat()[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3))

        elif dropdown_value==["Mkt-RF","HML"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                         annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig2),
                   dcc.Graph(figure=fig4))
        elif dropdown_value==["SMB","HML"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                        annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                         annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF','HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                   dcc.Graph(figure=fig3),
                   dcc.Graph(figure=fig4))

        elif dropdown_value==["Mkt-RF","SMB","HML"]:
            fig1= px.line(tab,x= tab.year, y="intercept",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                            annotation_text= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).intercept_,
                                                                                  annotation_font_size=14,annotation_font_color="red")
            fig2= px.line(tab, x= tab.year, y="Bêta1",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[0],
                                                                                   annotation_font_size=14,annotation_font_color="red")
            fig3= px.line(tab, x= tab.year, y="Bêta2",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                    annotation_text= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[1],
                                                                                       annotation_font_size=14,annotation_font_color="red")
            fig4= px.line(tab, x= tab.year, y="Bêta3",labels={"index":'date'}).add_hline(y= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[2],
                                                                                     annotation_text= model.fit(concat()[['Mkt-RF',"SMB",'HML']],concat()[Portfolios_ew_value]).coef_[2],
                                                                                     annotation_font_size=14,annotation_font_color="red")
            return(dcc.Graph(figure=fig1),
                 dcc.Graph(figure=fig2),
                 dcc.Graph(figure=fig3),
                 dcc.Graph(figure=fig4))

# =============================================================================
# Callbacks for the RollingOLS method for the 5 factors and value weighted
# =============================================================================
@app.callback(
     Output("dropdown_5factors_vw","value"),
     Input('all-or-none',"value"),
     State("dropdown_5factors_vw", "options")
     )
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [options["value"] for options in options if all_selected]
    return all_or_none


@app.callback(
    Output("container-graph-rol-5factors_vw","children"),
    Input("5factors_vw","n_clicks"),
    State("Portfolios_vw_5factors","value"),
    State("dropdown_5factors_vw","value"),
    Input("my_rangeslider_5factors_vw","value"),
    Input("Window_5factors_vw","value"),
    prevent_initial_call=True
    )

def make_graphics_5_factors_vw(n_clicks, Portfolios_vw_value,dropdown_5factors,year, window_vw):
    tab1= RollingOLS(concat5factors()[Portfolios_vw_value],add_constant(concat5factors()[dropdown_5factors]),window=window_vw).fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3","RMW":"Bêta4", "CMA": "Bêta5"}).reset_index()
    tab1=tab1.replace(tab1.index,concat.date[10420:])
    tab1["year"]=concat().index[10420:].year
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
# =============================================================================
# Callbacks for the RollingOLS method for the 5 factors and equal weighted
# =============================================================================
@app.callback(
     Output("dropdown_5factors_ew","value"),
     Input('checklist_5factors_ew',"value"),
     State("dropdown_5factors_ew", "options")
     )
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [options["value"] for options in options if all_selected]
    return all_or_none


@app.callback(
    Output("container-graph-rol-5factors_ew","children"),
    Input("5factors_ew","n_clicks"),
    State("Portfolios_ew_5factors","value"),
    State("dropdown_5factors_ew","value"),
    Input("my_rangeslider_5factors_ew","value"),
    Input("Window_5_factors_ew","value"),
    prevent_initial_call=True
    )

def make_graphics_5_factors_ew(n_clicks, Portfolios_ew_value,dropdown_5factors,year, window_vw):
    tab_ew= RollingOLS(concat5factors()[Portfolios_ew_value],add_constant(concat5factors()[dropdown_5factors]),window=window_vw).fit().params.rename(columns={"const":"intercept","Mkt-RF":"Bêta1","SMB":"Bêta2","HML":"Bêta3","RMW":"Bêta4", "CMA": "Bêta5"})
    tab_ew["index"]=concat().index[10420:].date
    tab_ew["year"]=concat().index[10420:].year
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
