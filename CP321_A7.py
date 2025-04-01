#LINK TO PROJECT HERE

import numpy as np
import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

def getData():
    dfList = pd.read_html("https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals")
    df = dfList[3]
    df = df[["Year","Winners","Runners-up"]]
    df = df[:-1]
    df = df.replace("West Germany", "Germany")
    winners = df["Winners"].unique()
    winCount = df["Winners"].value_counts()
    mapData = pd.DataFrame({"Country":winCount.index, "Win Count":winCount.values})
    return df, winners, winCount, mapData

df, winners, winCount, mapData = getData()
app = Dash()
server = app.server

app.layout = [
    html.H1(children="World Cup Dashboard", style={"textAlign":"center", "color": "grey"}),
    dcc.Graph(id="graph"),
    html.Br(),
    dcc.Dropdown(winners, "Argentina", id="dropdown-selection"),
    html.Div(id="win-count", style={"color": "green", "font-size": "20px"}),
    html.Br(),
    dcc.RadioItems(df["Year"], 2022, inline=True, id="radio-selection"),
    html.Div(id="winner-runnerup", style={"color": "orange", "font-size": "20px"})
]

@callback(
    Output("graph", "figure"),
    Output("win-count", "children"),
    Output("winner-runnerup", "children"),
    Input("dropdown-selection", "value"),
    Input("radio-selection", "value")
)
def update(value1, value2):
    fig = px.choropleth(mapData, locations="Country", locationmode="country names", color="Win Count", hover_name="Country", title="World Cup Wins")
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0),width=1500,height=650)

    output1 = f'{value1} has won {winCount[value1]} time(s).'

    finals = df[df["Year"] == value2]
    finals = finals.to_numpy()

    output2 = f'Winner: {finals[0][1]}, Runner-up: {finals[0][2]}'

    return fig, output1, output2

if __name__ == '__main__':
    app.run(debug=True)
