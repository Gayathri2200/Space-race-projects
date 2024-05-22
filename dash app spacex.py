#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import pandas as pd
from dash import html
from dash import dcc
import plotly.express as px
from dash.dependencies import Input,Output


# In[2]:


spacex_df = pd.read_csv("Downloads/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# In[3]:


spacex_df.head()


# In[4]:


app = dash.Dash(__name__)


# In[5]:


app.layout = html.Div(children=[html.H1('Spacex Launch Records Dashboard',style = {'textAlign': 'center','color':'#503D36',
                                                                                  'font-size':40}),
                               dcc.Dropdown(id = 'site-dropdown',
                                           options =[
                                               {'label':'All Sites','value':'ALL'},
                                               {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                               {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                               {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                               {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'}],
                                            value = 'ALL', placeholder = "State",searchable = True
                                           ),
                               html.Br(),
                               # Add a pie chart
                               html.Div(dcc.Graph(id = 'success-pie-chart')),
                               html.Br(),
                               
                               html.P("Payload range(kg):"),
                               #Add a slider
                               dcc.RangeSlider(id = 'payload-slider',
                                              min=0, max = 10000, step=1000,marks ={0: '0',100: '100'},
                                              value =[min_payload,max_payload]),
                               #Scatterplot to show the correlation between payload and launch success
                               html.Div(dcc.Graph(id ='success-payload-scatter-chart')),
                               ])

# add a callback function
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
             Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
    if entered_site == 'All':
        fig = px.pie(spacex_df,
                    values = 'class',
                    names = 'Launch Site',
                    title = 'Total success launch by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site]
        filtered_df = filtered_df.groupby('class').count().reset_index()
        fig = px.pie(filtered_df,
                    values ='Unnamed: 0',
                    names ='class',
                    title ='Total launches for site {}'. format(entered_site))
    return fig

@app.callback(Output(component_id ='success-payload-scatter-chart', component_property ='figure'),
             Input(component_id = 'site-dropdown', component_property = 'value'),
             Input(component_id = 'payload-slider', component_property = 'value'))

def get_scatter_plot(entered_site,payload_range):
    print('Params: {} {}'.format(entered_site,payload_range))
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &
                               (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))
                               ]
        fig = px.scatter(filtered_df, x ='Payload Mass (kg)', y ='class', color = 'Booster Version Category',title = 'All-sites-payload mass between {:8,d}kg and {:8,d}kg'.format(int(payload_range[0]),int(payload_range[1])))
    else:
        filtered_df = spacexdf[(spacex_df['Launch Site'] == entered_site) &
                              (spacex_df['Payload Mass (kg)'] >= int(payload_range[0])) &
                              (spacex_df['Payload Mass (kg)'] <= int(payload_range[1]))
                              ]
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category', title ='Site{}- payload mass between {:8,d}kg and {:8,d}kg'.format(entered_site,int(payload_range[0]),int(payload_range[1])))
        
    return fig
   


# In[6]:


if __name__ == '__main__':
    app.run_server(debug = False)

