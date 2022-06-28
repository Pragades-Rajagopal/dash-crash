import pandas as pd
import dash
import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

# Dataframe
df = pd.read_csv('app1_covid.csv')
dff = df.groupby('countriesAndTerritories', as_index=False)[['deaths', 'cases']].sum()
# print(df[:5])

app.layout = html.Div([
    html.H2('Covid-19 Distribution'),
    html.Div([dash_table.DataTable(
        id="dataTable_id",
        data=dff.to_dict('records'),
        columns=[{"name":i, "id":i, "deletable":False, "selectable":False} for i in dff.columns],
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=6,
        style_cell_conditional=[
            {'if':{'column_id':'countriesAndTerritories'}, 'width':'40%', 'textAlign':'left'},
            {'if':{'column_id':'deaths'}, 'width':'30%', 'textAlign':'left'},
            {'if':{'column_id':'cases'}, 'width':'30%', 'textAlign':'left'},
        ],
    ),], className='row'),

    html.Div([
        html.Div([
            dcc.Dropdown(id='dropdown-line',
            options=[{'label':'Deaths', 'value':'deaths'},
            {'label':'Cases', 'value':'cases'}],
            value='deaths',
            multi=False,
            clearable=False),
        ], className='six columns'),

        html.Div([
            dcc.Dropdown(id='dropdown-pie',
            options=[{'label':'Deaths', 'value':'deaths'},
            {'label':'Cases', 'value':'cases'}],
            value='cases',
            multi=False,
            clearable=False),
        ], className='six columns'),

    ], className='row'),

    html.Div([
        html.Div([dcc.Graph(id='linegraph',),], className='six columns'),
        html.Div([dcc.Graph(id='piechart',),], className='six columns'),
    ], className='row'),

])

@app.callback(
    [Output('linegraph', 'figure'), Output('piechart', 'figure')],
    [Input('dataTable_id', 'selected_rows'), Input('dropdown-pie', 'value'),
    Input('dropdown-line', 'value')]
)

def update_data(rows, pievalue, linevalue):
    
    if(len(rows) == 0):
        df_filtered = dff[dff['countriesAndTerritories'].isin(['United_States_of_America', 'Italy', 'China', 'India'])]

    else:
        print(rows)
        df_filtered = dff[dff.index.isin(rows)]

    pie_chart = px.pie(
        data_frame=df_filtered,
        names='countriesAndTerritories',
        values=pievalue,
        hole=0.3,
        labels={'countriesAndTerritories':'Countries'}
    )

    x = df_filtered['countriesAndTerritories'].to_list() #assigning selected countries as list
    df_line = df[df['countriesAndTerritories'].isin(x)]

    line_chart = px.line(
        data_frame=df_line,
        x='dateRep',
        y=linevalue,
        color='countriesAndTerritories',
        labels={'countriesAndTerritories':'Countries', 'dateRep':'Date'},
    )

    # line_chart.update_layout(uiversionn='foo')

    return(line_chart, pie_chart)


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

