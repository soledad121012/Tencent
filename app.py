# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

tmp_lst = []
with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp_lst.append(row)

df = pd.DataFrame(tmp_lst[1:], columns = tmp_lst[0])
modify = ['TRU', 'DAU', 'Items', 'Trans', 'Items Per Trans', 'Items per DAU',
        'Conversion', 'Cash Flow', 'Return Customer', 'Time Spend Per Day(seconds)']
for item in modify:
    df[item] = pd.to_numeric(df[item], errors = 'coerce').round(4)


def generate_table(dataframe, max_rows = 10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
metric = ['TRU', 'DAU', 'Items', 'Trans', 'Items Per Trans', 'Items per DAU',
        'Conversion', 'Cash Flow', 'Return Customer', 'Time Spend Per Day(seconds)']

app.layout = html.Div(children = [
    html.H1(children = 'Topline',
            style = {'textAlign': 'center'}),

    html.H4(children = 'Topline Table Average By Date',
            style = {'textAlign': 'center'}),
    generate_table(df),

    html.Label('Metrics'),
    dcc.Dropdown(
        id = 'variables',
        options = [{'label': i, 'value': i} for i in metric],
        value = 'TRU'
    ),
    dcc.RadioItems(
        id = 'type',
        options = [{'label': i, 'value': i} for i in ['Original', 'Log']],
        value = 'Original',
        labelStyle = {'display': 'inline-block'}
    ),

    dcc.Graph(id = 'time')
])


@app.callback(
    Output('time', 'figure'),
    [Input('variables', 'value'),
    Input('type', 'value')]
)

def update_graph(y_name, y_type):
    val = df[y_name]
    if y_type == 'Log':
        val = np.log(val)
    return {
        'data': [
            {'x': df['Date'], 'y': val, 'type': 'line'},
        ],
        'layout': {
            'title': 'Time Development of ' + y_name
        }
    }

if __name__ == '__main__':
    app.run_server(debug = True)
