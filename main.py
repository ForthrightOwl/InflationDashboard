import dash
from dash import html, dcc, Dash
import pandas as pd
import datetime as dt
import plotly.express as px
from dash.dependencies import Input, Output

"""Load all the datasets"""
YoY_NSA_data = pd.read_csv("venv/Data/YoY_NSA_data.csv")
YoY_SA_data = pd.read_csv("venv/Data/YoY_SA_data.csv")
MoM_NSA_data = pd.read_csv("venv/Data/MoM_NSA_data.csv")
MoM_SA_data = pd.read_csv("venv/Data/MoM_SA_data.csv")
relative_importance = pd.read_csv("venv/Data/relative_importance.csv")

"""Set indexes in date time format and add a CPI column to relative importance data"""
YoY_NSA_data.set_index(pd.to_datetime(YoY_NSA_data["date"]).dt.date, inplace=True)
YoY_SA_data.set_index(pd.to_datetime(YoY_SA_data["date"]).dt.date, inplace=True)
MoM_NSA_data.set_index(pd.to_datetime(MoM_NSA_data["date"]).dt.date, inplace=True)
MoM_SA_data.set_index(pd.to_datetime(MoM_SA_data["date"]).dt.date, inplace=True)
relative_importance.set_index("Unnamed: 0", inplace=True)
relative_importance["CPI"] = 100

"""Styling parameters"""
background_color = "#d6e4ea"
figure_color = "white"
border_color = "#8EA9C1"
text_color = "#004172"
discrete_colors = ["#4c78a8", "#fa4f56", "#54a24b", "#eeca3b", "#72b7b2", "#b279a2", "#ff9da6", "#9d755d"]
font = "Times New Roman"

"""Creates the timeseries graph"""
def timeseries_graph(series, data, start_date, end_date):
    fig_data = globals()[series][data].loc[start_date:end_date]
    fig = px.line(fig_data*100, labels={"value":"Index % Change", "date":"Date"},
                    color_discrete_sequence=discrete_colors)
    fig.update_layout(plot_bgcolor=figure_color, paper_bgcolor=figure_color,
                        colorway=discrete_colors, font={"family":font})
    fig.update_yaxes(zeroline=True, zerolinecolor="black", zerolinewidth=0.3),
    return fig

"""Creating contribution dataset"""
def calc_contributions(series , date, cats):
    data = series[cats].loc[:date]
    data2 = data.reset_index()
    data2["Year"] = pd.to_datetime(data2["date"]).dt.year - 1
    data2.set_index("Year", inplace=True)
    ri_data = relative_importance
    for cat in cats:
        data2[str(cat)+"_ri"] = data2.index.map(ri_data[str(cat)])
    for cat in cats:
        data2[str(cat)] = data2[str(cat)] * data2[str(cat)+"_ri"]
    data2 = data2.reset_index()
    data2.set_index("date", inplace=True)
    ct_cats = [str(cat) for cat in cats]
    cont = data2[ct_cats]
    return cont


"""Defining composition graphs"""
def composition_graph(series, date, cats, period, core):
    df = calc_contributions(series=series, date=date, cats=cats)
    df_core = calc_contributions(series=series, date=date, cats=[core, "Food away from home"])
    df["core"] = df.index.map(df_core[str(core)])
    df["Other"] = df["core"]
    for cat in cats:
        df["Other"] = df["Other"] - df[str(cat)]
    df = df.drop(columns="core")
    df2 = df.iloc[[-5 * period - 1, -4 * period - 1, -3 * period - 1, -2 * period - 1, -1 * period - 1, -1]]
    fig = px.bar(df2.round(2), labels={"value":"% Contribution", "date":"Time period", "variable":"Category"},
                 color_discrete_sequence=discrete_colors, hover_name="variable", text="value")
    fig.update_layout(plot_bgcolor=figure_color, paper_bgcolor=figure_color, font={"family":font},
                      uniformtext_minsize=12, uniformtext_mode='hide')
    fig.update_yaxes(showgrid=False),
    fig.update_xaxes(showgrid=False, gridwidth=1, gridcolor='#D1D1D1'),
    fig.update_yaxes(zeroline=True, zerolinecolor="black", zerolinewidth=0.3)
    fig.update_annotations(font={"family":font, "color":"white"})
    fig.update_traces(textposition="auto", textfont={"color":"white", "size":12})
    return fig

"""Defining base composition graph"""
def base_composition_graph(series, date):
    cats=["Food at home", "Food away from home", "Energy commodities", "Energy services",
          "Apparel", "New vehicles", "Used cars and trucks", "Medical care commodities",
          "Alcoholic beverages", "Tobacco and smoking products", "Shelter", "Medical care services",
          "Transportation services"]
    df = calc_contributions(series=series, date=date, cats=cats)
    df = df.iloc[-1]
    fig = px.bar(df.round(1), color_discrete_sequence=discrete_colors, text="value",
                 labels={"value":"% Contribution", "index":"Category"})
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor=figure_color, paper_bgcolor=figure_color, font={"family":font})
    fig.update_yaxes(showgrid=False),
    fig.update_xaxes(showgrid=False),
    fig.update_yaxes(zeroline=True, zerolinecolor="black", zerolinewidth=0.3)
    fig.update_traces(textfont={"color": "white"})
    return fig



app = Dash(__name__)

app.layout = html.Div(children=[

    html.H1("Inflation Explorer", style={"text-align": "center", "font-family":font, "color":text_color}),

    html.Div(children=[
            html.Div(children=[
                html.Label(['Choose a frequency:'], style={"margin-left":"1%", "font-family":font}),
                dcc.Dropdown(
                    id='freq_dropdown',
                    options=[
                        {'label': 'Annual', 'value': 'YoY'},
                        {'label': 'Monthly', 'value': 'MoM'}
                    ],
                    value='YoY',
                    style={"width":"95%", "background-color":figure_color, "font-family":font}
                    )], style={"width": "20%", "margin-left":"1%", "display":"inline-block"}),
            html.Div(children=[
                html.Label(['Adjust for seasonality?'], style={"margin-left":"1%", "font-family":font}),
                dcc.Dropdown(
                    id='seas_dropdown',
                    options=[
                        {'label': 'Yes', 'value': 'SA'},
                        {'label': 'No', 'value': 'NSA'},
                    ],
                    value='NSA',
                    style={"width":"95%", "background-color":figure_color, "font-family":font}
                    )], style={"width": "20%", "margin-left":"1%", "display":"inline-block"}),
            html.Div(children=[
                html.Label(['Select timeframe:'], style={"margin-left":"1%", "font-family":font}),
                dcc.DatePickerRange(id="tsdate", start_date=dt.date(1920, 1, 1), end_date=dt.date.today(),
                                    style={"background-color":figure_color, "font-family":font}
                                    )], style={"width":"25%", "display":"inline-block"}
            )

    ],style={"border-style": "solid", "border-width": "1.5px", "border-color":border_color, "width":"95%",
             "background-color":figure_color, "margin":"auto", "display":"flex", "justify-content":"space-around"}
    ),

    html.Div(children=[
        html.H1("Timeseries Analysis", style={"margin-left":"1%", "font-family":font, "color":text_color}),
        html.Div(children=("Percentage change in selected indexes over time."),
                 style={"margin-left":"1%", "font-family":font}),
        html.Div(children=[
                html.Label(['Choose the data:'], style={"margin-left":"1%", "font-family":font}),
                dcc.Dropdown(
                    id='data_dropdown',
                    options=[
                        {'label': 'CPI', 'value': 'CPI'},
                        {'label': 'Core components', 'value': 'core_components'},
                        {'label': 'Core CPI', 'value': 'core_cpi'},
                        {'label': 'Food', 'value': 'food'},
                        {'label': 'Energy', 'value': 'energy'}
                    ],
                    value='CPI',
                    style={"width":"95%", "background-color":figure_color, "font-family":font}
                    )], style={"width": "20%", "margin-left":"1%", "display":"inline-block","vertical-align":"top"}),
        dcc.Graph(id="timeseries_graph", style={"width": "95%","margin-right":"1%", "background-color":figure_color})

    ],
        style={"border-style": "solid", "border-width": "1.5px", "border-color":border_color, "width":"95%", "background-color":figure_color,
               "margin":"auto", "margin-top":"0.5cm"}),

    html.Div(children=[
        html.Div(children=[
            html.H1(children="Composition Analysis", style={"margin-left":"1%", "font-family":font, "color":text_color}),
            html.Div(children="Contribution of sub-categories to the overall CPI measure expressed in % contributed.",
                     style={"margin-left":"1%", "font-family":font}),
            dcc.Graph(figure=composition_graph(YoY_NSA_data, dt.date.today(),["Core CPI", "Food", "Energy"], 12, "CPI"),
                      id="composition_graph", style={"width": "95%", "margin-left":"1%", "font-family":font})],
            style={"border-style": "solid", "border-width": "1.5px", "border-color":border_color,
                  "background-color":figure_color, "margin-top":"0.5cm", "margin-bottom":"0.5cm", "width":"53%",
                   "display":"inline-block"}
        ),

        html.Div(children=[
            html.H1(children="Base Composition", style={"margin-left":"1%", "font-family":font, "color":text_color}),
            html.Div(children="Base category composition of the CPI on the selected end date.",
                     style={"margin-left":"1%","margin-right":"1%", "font-family":font}),
            dcc.Graph(figure= base_composition_graph(YoY_NSA_data, dt.date.today())
                      ,id="base_composition_graph", style={"width": "95%", "margin-left":"1%", "font-family":font})],
            style={"border-style": "solid", "border-width": "1.5px", "border-color":border_color, "width":"45%",
                  "background-color":figure_color,  "margin-top":"0.5cm", "margin-bottom":"0.5cm",
                    "display":"inline-block", "margin-left":"0.5cm"}
        )
    ],style={"width":"95%", "margin":"auto"})
],
    style={"background-color":background_color}
)


"""Callback that chooses the timeseries graph from the dropdown"""
@app.callback(
    Output('timeseries_graph', 'figure'),
    Input(component_id='seas_dropdown', component_property='value'),
    Input(component_id='freq_dropdown', component_property='value'),
    Input(component_id='data_dropdown', component_property='value'),
    Input(component_id="tsdate", component_property="start_date"),
    Input(component_id="tsdate", component_property="end_date")
)
def select_timeseries_graph(season, frequency, data, start_date, end_date):
    series = frequency + "_" + season + "_data"
    start_date = dt.date.fromisoformat(start_date)
    end_date = dt.date.fromisoformat(end_date)
    if data == "CPI":
        fig = timeseries_graph(series, data, start_date=start_date, end_date=end_date)
        return fig
    elif data == "core_components":
        fig = timeseries_graph(series, data=["Core CPI", "Food", "Energy"], start_date=start_date, end_date=end_date)
        return fig
    elif data == "core_cpi":
        fig = timeseries_graph(series, data=["Commodities (less food and energy)",
                                             "Services (less energy)"],
                               start_date=start_date, end_date=end_date)
        return fig
    elif data == "food":
        fig = timeseries_graph(series, data=["Food at home", "Food away from home"],
                               start_date=start_date, end_date=end_date)
        return fig
    elif data == "energy":
        fig = timeseries_graph(series, data=["Energy commodities", "Energy services"],
                               start_date=start_date, end_date=end_date)
        return fig

"""Callback that creates the drilldown functionality of the composition graph"""
@app.callback(
    Output("composition_graph", "figure"),
    Input(component_id="freq_dropdown", component_property="value"),
    Input(component_id="seas_dropdown", component_property="value"),
    Input(component_id="tsdate", component_property="end_date"),
    Input(component_id='composition_graph', component_property='clickData'),
)
def drilldown_composition_graph(freq, seas, end_date, click_data):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    def pick_data(data):
        if data == "CPI":
            cats = ["Core CPI", "Food", "Energy"]
            return cats
        elif data == "Core CPI":
            cats = ["Commodities (less food and energy)", "Services (less energy)"]
            return cats
        elif data == "Food":
            cats = ["Food at home", "Food away from home"]
            return cats
        elif data == "Energy":
            cats = ["Energy commodities", "Energy services"]
            return cats
        elif data == "Food at home":
            cats = ["Cereals and bakery products", "Meats, poultry, fish, and eggs", "Dairy and related products",
                    "Fruits and vegetables", "Nonalcoholic beverages", "Other food at home"]
            return cats
        elif data == "Energy commodities":
            cats = ["Fuel oil", "Gasoline"]
            return cats
        elif data == "Energy services":
            cats = ["Electricity", "Utility gas service"]
            return cats
        elif data == "Commodities (less food and energy)":
            cats = ["Apparel", "New vehicles", "Used cars and trucks", "Medical care commodities",
                    "Alcoholic beverages", "Tobacco and smoking products"]
            return cats
        elif data == "Services (less energy)":
            cats = ["Shelter", "Medical care services", "Transportation services"]
            return cats

    end_date_2 = dt.datetime.strptime(end_date, "%Y-%m-%d")
    year = int(end_date_2.year)
    month = int(end_date_2.month)
    date = dt.date(year, month, 1)
    series = globals()[freq + "_" + seas + "_data"]
    if trigger_id == "composition_graph":
        if click_data is not None:
            valid = ["CPI", "Core CPI", "Food", "Energy", "Food at home", "Energy commodities",
                     "Energy services", "Commodities (less food and energy)", "Services (less energy)"]
            dummy = click_data['points'][0]['hovertext']
            cats = pick_data(dummy)
            if dummy in valid:
                if freq == "YoY":
                    fig = composition_graph(series, date, cats, 12, dummy)
                    return fig
                elif freq == "MoM":
                    fig = composition_graph(series, date, cats, 1, dummy)
                    return fig
            else:
                if freq == "YoY":
                    return composition_graph(series, date,["Core CPI", "Food", "Energy"], 12, "CPI")
                else:
                    return composition_graph(series, date, ["Core CPI", "Food", "Energy"], 1, "CPI")
        else:
            if freq == "YoY":
                return composition_graph(series, date, ["Core CPI", "Food", "Energy"], 12, "CPI")
            else:
                return composition_graph(series, date, ["Core CPI", "Food", "Energy"], 1, "CPI")
    else:
        if freq == "YoY":
            return composition_graph(series, date, ["Core CPI", "Food", "Energy"], 12, "CPI")
        else:
            return composition_graph(series, date, ["Core CPI", "Food", "Energy"], 1, "CPI")

"""Callback that sets the data for the base composition graph"""
@app.callback(
    Output("base_composition_graph", "figure"),
    Input(component_id="freq_dropdown", component_property="value"),
    Input(component_id="seas_dropdown", component_property="value"),
    Input(component_id="tsdate", component_property="end_date")
)
def pick_base_data(freq, seas, end_date):
    end_date_2 = dt.datetime.strptime(end_date, "%Y-%m-%d")
    year = int(end_date_2.year)
    month = int(end_date_2.month)
    date = dt.date(year, month, 1)
    series = globals()[freq + "_" + seas + "_data"]
    return base_composition_graph(series, date)

app.run_server(debug=True)

