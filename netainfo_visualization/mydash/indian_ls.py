import dash
import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from plotly import tools
from dash.dependencies import Input, Output
from cachetools import cached, TTLCache
import plotly.graph_objs as go
import geojson
import geopandas as gpd

cache = TTLCache(maxsize=100, ttl=300)

# read ls election file
df_ls = pd.read_csv('ls_cleaned.csv')

# read geojson file using geopandas
india_map = gpd.read_file('india_criminal.geojson')


# Traces
@cached(cache)
def fig(year, section, result):
    if result != 'All':
        candidates = df_ls[(df_ls.Year == year) & (df_ls.Winner == result)]
    else:
        candidates = df_ls[(df_ls.Year == year)]

    if section == 'State':
        candidates_group = candidates.groupby('State')
    elif section == 'Party':
        candidates_group = candidates.groupby('Party')

    candidate_group_crim = candidates_group['Criminal_Case'].mean(
    ).sort_values(ascending=False).head(5)

    candidate_group_assets = candidates_group['Assets_num'].mean(
    ).sort_values(ascending=False).head(5)

    candidates_group_age = candidates_group['Age'].mean(
    ).sort_values(ascending=False).head(5)

    traces = [{
        "x": candidate_group_crim.index.values,
        "y": np.around(candidate_group_crim.values, 1),
        "name": "<i><b>{} wise average no. of criminal cases</b></i>".format(section),
        "type": "bar",
        "text": "criminal case(s)",
        "marker": dict(
            # color =  'rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        "opacity": 0.7
    },
        {
        "x": candidate_group_assets.index.values,
        "y": np.around(candidate_group_assets.values/10000000, 2),
        "name": "{} wise average assets (in Cr.)".format(section),
        "type": "bar",
        "text": "Crores",
        "marker": dict(
            # color =  'rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        "opacity": 0.7
    },
        {
        "x": candidates_group_age.index.values,
        "y": np.around(candidates_group_age.values, 1),
        "name": "{} wise average age (in Yrs.)".format(section),
        "type": "bar",
        "text": "Years",
        "marker": dict(
            # color =  'rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        "opacity": 0.7
    }
    ]
    return traces


# Layout for all the traces/divs/plots
def figlayout(year, section, result):
    layouts = [
        go.Layout(  # layout1
            #     images= [dict(
            #           source= "https://images.indianexpress.com/2017/12/indian-parliament-express75911.jpg",
            #           xref= "x",
            #           yref= "y",
            #           x = 0,
            #           y = 0,
            #           sizex = 2,
            #           sizey = 2,
            #           sizing = "stretch",
            #           opacity = 0.5,
            #           layer = "below")],
            margin=dict(t=100),  # it is margin within a graph
            title='<b>{} wise top 5 average no. of criminal cases</b>'.format(
                section),
            showlegend=False,
            xaxis=dict(
                title='<i><b>{}</i></b>'.format(section),
                # tickangle=-25,
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            ),
            yaxis=dict(
                title='<i><b>No. of Cases</i></b>',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            )
        ),
        go.Layout(  # layout2
            # margin=dict(t=150),
            title='<b>{} wise top 5 average assets (in Cr.)</b>'.format(
                section),
            showlegend=False,
            xaxis=dict(
                title='<i><b>{}</i></b>'.format(section),
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            ),
            yaxis=dict(
                title='<i><b>Assets (in Cr.)</i></b>',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            )
        ),
        go.Layout(  # layout3
            # margin=dict(t=150),
            title='<b>{} wise top 5 average age (in Yrs.)</b>'.format(section),
            showlegend=False,
            xaxis=dict(
                title='<i><b>{}</i></b>'.format(section),
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            ),
            yaxis=dict(
                title='<i><b>Age (in Yrs.)<i><b>',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                autorange=False,
                nticks=10,
                range=[30, 80],
                showticklabels=True,
                # tickangle=45,
                tickfont=dict(
                    family='Old Standard TT, serif',
                    size=10,
                    color='black'
                )
            )
        )
    ]
    return layouts


# color settings
colors = {
    'background': '#21618C',
    'text': '#AED6F1'
}

app = dash.Dash()

app.title = 'Indian Lok Sabha'

app.layout = html.Div([
    html.Div([
    html.H1('Analysis of candidates in Indian elections', style={
            'textAlign': 'center', 'fontFamily': 'system-ui'}),
    html.A(html.I('Data source'), href="http://www.myneta.info")],  style = {'textAlign' : 'center',
             'color': colors['text'], 'backgroundColor': colors['background'],}),#, style={'color':'#BFC9CA'}),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Lok Sabha', children=[
            html.Div([  # year drop down
                dcc.Dropdown(
                    id='year-slider',
                    options=[
                       {'label': '2004', 'value': '2004'},
                       {'label': '2009', 'value': '2009'},
                       {'label': '2014', 'value': '2014'}
                    ],
                    value="2004"
                )],
                className='three columns'),

            html.Div([  # party drop down
                dcc.Dropdown(
                    id='section-slider',
                    options=[
                        {'label': 'State', 'value': 'State'},
                        {'label': 'Party', 'value': 'Party'}
                    ],
                    value="State"
                )],
                className='three columns'),

            html.Div([  # results dropdown
                dcc.Dropdown(
                    id='result-slider',
                    options=[
                        {'label': 'Winners', 'value': 'Yes'},
                        {'label': 'Losers', 'value': 'No'},
                        {'label': 'All', 'value': 'All'}
                    ],
                    value="Yes"
                )],
                className='three columns'  # ,
                # style={'marginBottom': 50, 'marginTop': 25}
            ),

            html.Div(id='divgraph1', children=dcc.Graph(
                id='graph1',
                config={
                    'displayModeBar': False
                    # "displaylogo": False,
                    # 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
                },
                style={'width': "70vw"}
            ),
                style={'marginLeft': 50, 'marginBottom': 50, 'marginTop': 125}
            ),

            html.Div(id='divgraph2', children=dcc.Graph(
                id='graph2',
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
                },
                style={'width': "70vw"}
            ),
                style={'marginLeft': 50, 'marginBottom': 50}
            ),

            html.Div(id='divgraph3', children=dcc.Graph(
                id='graph3',
                config={
                    "displaylogo": False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
                },
                style={'width': "70vw"}
            ),
                style={'marginLeft': 50, 'marginBottom': 50}
            )
        ]),
        dcc.Tab(label='Assembly', children=[
            html.Div([
                html.H1("Tab 2 content")
            ]),
            html.Div(id='divgraph11', children=dcc.Graph(
                id='graph4',
                config={
                    'displayModeBar': False
                },
                style={'width': "70vw"}
            ),
                style={'marginLeft': 50, 'marginBottom': 50, 'marginTop': 125}
            ),
        ])
    ]
    )
])

@app.callback(
    Output('graph1', 'figure'),
    [Input('year-slider', 'value'),
    Input('section-slider', 'value'),
    Input('result-slider', 'value')])
def update_output_graph(input_value1, input_value2, input_value3):
    year, section, result = int(input_value1), input_value2, input_value3
    traces = fig(year, section, result)
    layouts = figlayout(year, section, result)
    return go.Figure(data=[traces[0]], layout=layouts[0])

@app.callback(
    Output('graph2', 'figure'),
    [Input('year-slider', 'value'),
    Input('section-slider', 'value'),
    Input('result-slider', 'value')])
def update_output_graph(input_value1, input_value2, input_value3):
    year, section, result = int(input_value1), input_value2, input_value3
    traces = fig(year, section, result)
    layouts = figlayout(year, section, result)
    return go.Figure(data=[traces[1]], layout=layouts[1])


@app.callback(
    Output('graph3', 'figure'),
    [Input('year-slider', 'value'), 
    Input('section-slider', 'value'),
    Input('result-slider', 'value')])
def update_output_graph(input_value1, input_value2, input_value3):
    year, section, result = int(input_value1), input_value2, input_value3
    traces = fig(year, section, result)
    layouts = figlayout(year, section, result)
    return go.Figure(data=[traces[2]], layout=layouts[2])


if __name__ == '__main__':
    app.run_server(debug=True)
