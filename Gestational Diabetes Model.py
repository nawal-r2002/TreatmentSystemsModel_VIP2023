import pandas as pd
from dash import Dash, html, dcc, callback, dash_table, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

df = pd.read_csv("Interactions Database.csv")

app = Dash(__name__)

colors = {
    'text': '#000000'
}    

dff = df.copy()
dff = dff.drop(columns=dff.columns[0:1])

app.layout = html.Div(children=[
    html.H1(
        children='Gestational Diabetes Drug-Drug Interactions',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div([
        dcc.Dropdown(
            df['Observed Drug-Drug Interaction'].unique(), 
            placeholder = "Select an Interaction",
            id='currInteraction'
        ),

    html.Div(dcc.Graph(id='fig')),
    html.Div(dcc.Graph(id='severeInteraction')),

    dbc.Row([
        dbc.Col([
            ingredient_drop := dcc.Dropdown([x for x in sorted(df['Suspect Product Names'].unique())], placeholder = "Select Product Name")
        ], width=3),
        dbc.Col([
            reason_drop := dcc.Dropdown([x for x in sorted(df['Reason for Use'].unique())], placeholder = "Reason for Use")
        ], width=3),
        dbc.Col([
            serious_drop := dcc.Dropdown([x for x in sorted(df['Serious'].unique())], placeholder = "Is the Case Serious?")
        ], width=3),
        dbc.Col([
            outcome_drop := dcc.Dropdown([x for x in sorted(df['Outcomes'].unique())], placeholder= "What was the Outcome")
        ], width=3),
        dbc.Col([
            priority_drop := dcc.Dropdown([x for x in sorted(df['Case Priority'].unique())], placeholder= "Select the Priority")
        ], width=3),
        dbc.Col([
            reporter_drop := dcc.Dropdown([x for x in sorted(df['Reporter Type'].unique())], placeholder="How was the case Reported?")
        ], width=3),
        dbc.Col([
            location_drop := dcc.Dropdown([x for x in sorted(df['Country where Event occurred'].unique())], placeholder="Select Country where Case Occured")
        ], width=3)
    ], justify="between", className='mt-3 mb-4'),

    my_table := dash_table.DataTable(
        data = dff.to_dict('records'),
        columns=[{"name": i, "id": i} for i in dff.columns],
        style_cell={
            'textAlign': 'left', 
            'minWidth': '200px', 
            'width': '300px', 
            'maxWidth': '1000px', 
            'whiteSpace':'normal', 
            'height':'auto', 
            'lineHeight':'35px'},
        style_table={'overflowX': 'auto'},
        style_data={
            'whiteSpace': 'normal',
            'minWidth': '200px', 
            'width': '300px', 
            'maxWidth': '1000px',
            'height': 'auto',
        },
        hidden_columns = ['Observed Drug-Drug Interaction'],
        css=[{
            "selector": ".show-hide", 
            "rule": "display: none"}]
    )
    ])
])

@callback(
    Output('fig', 'figure'),
    Input('currInteraction', 'value')
)

def updateMedicationGraph(currInteraction):
    temp = df.loc[df['Observed Drug-Drug Interaction'] == currInteraction]
    data = temp['Suspect Product Names']
    fig = px.histogram(data, x = "Suspect Product Names", title = 'Cases of Patients that Used Drugs')
    return fig

@callback(
    Output('severeInteraction', 'figure'),
    Input('currInteraction', 'value')
)

def updateSeverityGraph(currInteraction):
    temp = df.loc[df['Observed Drug-Drug Interaction'] == currInteraction]
    seriousData = temp['Serious']
    severeInteraction = px.histogram(seriousData, x = "Serious", title = "Severity of Drug-Drug Interactions")
    return severeInteraction

@callback(
    Output(my_table, 'data'),
    Input('currInteraction', 'value'),
    Input(ingredient_drop, 'value'),
    Input(reason_drop, 'value'),
    Input(serious_drop, 'value'),
    Input(outcome_drop, 'value'),
    Input(priority_drop, 'value'),
    Input(reporter_drop, 'value'),
    Input(location_drop, 'value')
)

def updateTable(currInteraction, ingredient, reason, serious, outcome, priority, reporterType, location):
    data = dff.copy()

    data = data.loc[df['Observed Drug-Drug Interaction'] == currInteraction]
    data = data.drop(columns=data.columns[0:1])

    if ingredient:
        data = data[data['Suspect Product Names'] == ingredient]

    if reason:
        data = data[data['Reason for Use'] == reason]

    if serious:
        data = data[data['Serious'] == serious]

    if outcome:
        data = data[data['Outcomes'] == outcome]

    if priority:
        data = data[data['Case Priority'] == priority]

    if reporterType:
        data = data[data['Reporter Type'] == reporterType]

    if location:
        data = data[data['Country where Event occurred'] == location]

    return data.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)