import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd

surface_cols = ['Clay', 'Hard', 'Grass']
surfaces = [{'label': i, 'value': i} for i in surface_cols]

df = pd.read_csv("data/tournaments_1877-2017_unindexed.csv")
df.columns.str.startswith('doubles')
df = df.loc[:, ~df.columns.str.startswith('doubles')]

# Grand slam champions
df_gs = df.loc[df['tourney_name'].isin(['Wimbledon', 'Roland Garros', 'US Open', 'Australian Open'])]
counts = df_gs.singles_winner_name.value_counts()
# print(counts)

column_names = ['name', 'type', 'count']
df_bar = pd.DataFrame(columns=column_names)

for name in ['Roger Federer', 'Rafael Nadal', 'Novak Djokovic']:
    df_temp = df.loc[df['singles_winner_name'] == name]

    clay = (df_temp['tourney_surface'] == 'Clay').sum()
    grass = (df_temp['tourney_surface'] == 'Grass').sum()
    hard = (df_temp['tourney_surface'] == 'Hard').sum()

    df_bar.loc[len(df_bar.index)] = [name, 'hard', hard]
    df_bar.loc[len(df_bar.index)] = [name, 'clay', clay]
    df_bar.loc[len(df_bar.index)] = [name, 'grass', grass]

figure1 = px.bar(df_bar, x="name", y='count', color='type',
                 labels={"year": "Name", "suicides_no": "count"}
                 )

df_b3 = df_gs.loc[df_gs['singles_winner_name'].isin(['Roger Federer', 'Rafael Nadal', 'Novak Djokovic'])]

column_names = ['year', 'winner', 'count']
df_f = pd.DataFrame(columns=column_names)

win_f = 0
win_n = 0
win_d = 0

for year in range(2003, 2018):
    df_y = df_b3.loc[df_b3['tourney_year'] == year]

    win_f += (df_y['singles_winner_name'] == 'Roger Federer').sum()
    win_n += (df_y['singles_winner_name'] == 'Rafael Nadal').sum()
    win_d += (df_y['singles_winner_name'] == 'Novak Djokovic').sum()

    df_f.loc[len(df_f.index)] = [year, 'Roger Federer', win_f]
    df_f.loc[len(df_f.index)] = [year, 'Rafael Nadal', win_n]
    df_f.loc[len(df_f.index)] = [year, 'Novak Djokovic', win_d]

figure2 = px.line(df_f.copy(), x="year", y='count', color='winner',
                  labels={"year": "Name", "suicides_no": "count"}
                  )

# All Wins

df_b3 = df.loc[df['singles_winner_name'].isin(['Roger Federer', 'Rafael Nadal', 'Novak Djokovic'])]

column_names = ['year', 'winner', 'count']
df_f = pd.DataFrame(columns=column_names)

win_f = 0
win_n = 0
win_d = 0

for year in range(2003, 2018):
    df_y = df_b3.loc[df_b3['tourney_year'] == year]

    win_f += (df_y['singles_winner_name'] == 'Roger Federer').sum()
    win_n += (df_y['singles_winner_name'] == 'Rafael Nadal').sum()
    win_d += (df_y['singles_winner_name'] == 'Novak Djokovic').sum()

    df_f.loc[len(df_f.index)] = [year, 'Roger Federer', win_f]
    df_f.loc[len(df_f.index)] = [year, 'Rafael Nadal', win_n]
    df_f.loc[len(df_f.index)] = [year, 'Novak Djokovic', win_d]

figure3 = px.line(df_f.copy(), x="year", y='count', color='winner',
                  labels={"year": "Year", "count": "Wins"}
                  )

df_clay = df.loc[df['tourney_surface'] == 'Clay']
tmp_data = df_clay.singles_winner_name.value_counts()[:5]
df_clay_chart = pd.DataFrame({'winner': tmp_data.index, 'count': tmp_data.values})

figure4 = px.bar(df_clay_chart, x="winner", y='count',
                 labels={"year": "Year", "count": "Wins"}
                 )

df_grass = df.loc[df['tourney_surface'] == 'Grass']
tmp_data = df_grass.singles_winner_name.value_counts()[:5]
df_grass_chart = pd.DataFrame({'winner': tmp_data.index, 'count': tmp_data.values})

figure5 = px.bar(df_grass_chart, x="winner", y='count',
                 labels={"year": "Year", "count": "Wins"}
                 )

df_hard = df.loc[df['tourney_surface'] == 'Hard']
tmp_data = df_hard.singles_winner_name.value_counts()[:5]
df_hard_chart = pd.DataFrame({'winner': tmp_data.index, 'count': tmp_data.values})

figure6 = px.bar(df_hard_chart, x="winner", y='count',
                 labels={"year": "Year", "count": "Wins"}
                 )

tmp_data = df_hard.tourney_conditions.value_counts()
df_indoor = pd.DataFrame({'type': tmp_data.index, 'count': tmp_data.values})

figure7 = px.pie(df_indoor, values='count', names='type')

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
    }
]

app = dash.Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([html.H1('Big 3: Surfaces')], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=figure1)], className='twelve columns'),
        ], className='row')
    ]),
    html.Div([html.H1('Big 3: Grand Slams')], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=figure2)], className='twelve columns'),
        ], className='row')
    ]),
    html.Div([html.H1('Big 3: All tournaments')], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=figure3)], className='twelve columns'),
        ], className='row')
    ]),
    html.Div([html.H1('Best players on surface')], className='row'),
    html.Div([dcc.Dropdown(
        id='surface_input',
        options=surfaces, value=surfaces[0]['value'], className='five columns')],
        className='twelve columns'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=figure4, id='surface_chart')], className='twelve columns'),
        ], className='row')
    ]),
    html.Div([html.H1('Tournament condition')], className='row'),
    html.Div([
        html.Div([
            html.Div([dcc.Graph(figure=figure7)], className='twelve columns'),
        ], className='row')
    ]),
], className='container')


@app.callback(
    Output(component_id='surface_chart', component_property='figure'),
    [Input(component_id='surface_input', component_property='value')]
)
def update_surface_type(input_):
    data = 0
    if input_ == 'Clay':
        data = df_clay_chart
    elif input_ == 'Grass':
        data = df_grass_chart
    else:
        data = df_hard_chart

    figure = px.bar(data, x="winner", y='count',
                    title='Winners on {} surface'.format(input_),
                    labels={"year": "Year", "count": "Wins"}
                    )

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
