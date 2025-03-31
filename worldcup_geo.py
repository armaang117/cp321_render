# Deployed at: https://myworldcupdashboard.render.com (Password: worldcup2023)

import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, Dash
from dash.exceptions import PreventUpdate


# Step 1: dataset for the dashboard
data = [
    {"Year": 1930, "Winner": "Uruguay",      "RunnerUp": "Argentina"},
    {"Year": 1934, "Winner": "Italy",         "RunnerUp": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy",         "RunnerUp": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay",       "RunnerUp": "Brazil"},
    {"Year": 1954, "Winner": "West Germany",  "RunnerUp": "Hungary"},
    {"Year": 1958, "Winner": "Brazil",        "RunnerUp": "Sweden"},
    {"Year": 1962, "Winner": "Brazil",        "RunnerUp": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England",       "RunnerUp": "West Germany"},
    {"Year": 1970, "Winner": "Brazil",        "RunnerUp": "Italy"},
    {"Year": 1974, "Winner": "West Germany",  "RunnerUp": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina",     "RunnerUp": "Netherlands"},
    {"Year": 1982, "Winner": "Italy",         "RunnerUp": "West Germany"},
    {"Year": 1986, "Winner": "Argentina",     "RunnerUp": "West Germany"},
    {"Year": 1990, "Winner": "West Germany",  "RunnerUp": "Argentina"},
    {"Year": 1994, "Winner": "Brazil",        "RunnerUp": "Italy"},
    {"Year": 1998, "Winner": "France",        "RunnerUp": "Brazil"},
    {"Year": 2002, "Winner": "Brazil",        "RunnerUp": "Germany"},
    {"Year": 2006, "Winner": "Italy",         "RunnerUp": "France"},
    {"Year": 2010, "Winner": "Spain",         "RunnerUp": "Netherlands"},
    {"Year": 2014, "Winner": "Germany",       "RunnerUp": "Argentina"},
    {"Year": 2018, "Winner": "France",        "RunnerUp": "Croatia"},
    {"Year": 2022, "Winner": "Argentina",     "RunnerUp": "France"}
]

df = pd.DataFrame(data)

# country names:
df['Winner'] = df['Winner'].replace({
    'West Germany': 'Germany',
    'England': 'United Kingdom',
    'Czechoslovakia': 'Czech Republic'
})
df['RunnerUp'] = df['RunnerUp'].replace({
    'West Germany': 'Germany',
    'England': 'United Kingdom',
    'Czechoslovakia': 'Czech Republic'
})

# Wins per country for the choropleth map.
wins = df['Winner'].value_counts().reset_index()
wins.columns = ['Country', 'Wins']

# Step 2: Create a choropleth map 
fig_choropleth = px.choropleth(
    wins,
    locations="Country",
    locationmode="country names", 
    color="Wins",
    hover_name="Country",
    color_continuous_scale=["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"],
    range_color=[1, 5],
    title="FIFA World Cup Wins by Country"
)
fig_choropleth.update_geos(fitbounds="locations")
fig_choropleth.update_layout(
    margin={"r":0, "t":60, "l":0, "b":0},
    template=None,
    coloraxis_colorbar=dict(
        tickmode="array",
        tickvals=[1, 2, 3, 4, 5],
        ticktext=["1", "2", "3", "4", "5"]
    )
)

# Prepare unique lists for dropdowns
countries = sorted(wins['Country'].unique())
years = sorted(df['Year'].unique())

# Step 3: Build the Dash dashboard 
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Finals Dashboard", style={'text-align': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Choropleth Map', children=[
            dcc.Graph(figure=fig_choropleth)
        ]),
        dcc.Tab(label='Country Wins', children=[
            html.Div([
                html.Label("Select a country:"),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': c, 'value': c} for c in countries],
                    placeholder="Select a country",
                    value=countries[0] if countries else None
                ),
                html.Div(id='country-wins-output', style={'margin-top': '20px', 'font-size': '18px'})
            ], style={'padding': '20px'})
        ]),
        dcc.Tab(label='Yearly Final Result', children=[
            html.Div([
                html.Label("Select a year:"),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in years],
                    placeholder="Select a year",
                    value=years[0] if years else None
                ),
                html.Div(id='year-result-output', style={'margin-top': '20px', 'font-size': '18px'})
            ], style={'padding': '20px'})
        ])
    ])
])

# Callback for displaying the number of wins for a selected country.
@app.callback(
    Output('country-wins-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_wins(selected_country):
    if not selected_country:
        raise PreventUpdate
    win_count = wins[wins['Country'] == selected_country]['Wins'].values[0]
    return f"{selected_country} has won the FIFA World Cup {win_count} time{'s' if win_count != 1 else ''}."

# Callback for displaying the final result for a selected year.
@app.callback(
    Output('year-result-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_result(selected_year):
    if not selected_year:
        raise PreventUpdate
    result = df[df['Year'] == selected_year].iloc[0]
    return f"In {selected_year}, the winner was {result['Winner']} and the runner-up was {result['RunnerUp']}."

if __name__ == '__main__':
    app.run_server(debug=True)