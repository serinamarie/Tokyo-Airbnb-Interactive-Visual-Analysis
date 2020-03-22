import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def data_wrangling(neighbourhood, beds, superhost, accommodates, localhost, hottub):
    df = pd.read_csv('data/tsne_final.csv')

    # filter the dataframe to show only data by neighborhood and bedrooms.
    df = df[(df.neighbourhood_cleansed == neighbourhood) & (
        df.beds == beds) & (df.accommodates == accommodates) &
        (df.host_is_superhost == superhost) & (df.local_host == localhost) &
        (df.hot_tub == hottub)]

    # get only required cols
    cols = ['TSNE1', 'TSNE2', 'TSNE3', 'name', 'profit_category', 'price_per_night_in_USD',
            'beds', 'minimum_nights', 'accommodates', 'estimated_monthly_income_in_USD',
            'host_is_superhost', 'local_host', 'hot_tub']

    df = df[cols]

    return df


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

text_style = dict(color='#444', fontFamily='raleway', fontWeight=300)
# plotly_figure = update_function()

navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            color='success',
            label="Serina Grill",
            children=[
                dbc.DropdownMenuItem(
                    "GitHub",
                    href='https://github.com/serinamarie',
                    external_link=True),
                dbc.DropdownMenuItem(
                    "LinkedIn",
                    href='https://linkedin.com/in/serina-grill-25492720/',
                    external_link=True),
            ],
        ),
    ],
    brand="AirBnb Optimal Price Predictor",
    brand_href="#",
    sticky="top",


)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(children=[
                            html.Div(children=[
                                dcc.Tabs(value='what-is', children=[
                                    dcc.Tab(label='About', value='what-is', children=html.Div(children=[
                                        html.Br(),
                                        html.H4(
                                            children='For what price should you list your AirBnb in order to make the highest income each month?'),
                                        html.P(
                                            'Select the features of the AirBnb you rent out and take a look at the graph to the right, which will update with your specified features. You can use your touchpad to zoom in on the graph and view similar listings.'),
                                        html.P('Hovering over a data point highlights a AirBnb with the same features as you, including the same neighborhood. Take a look at estimated monthly income (converted to USD) for each listing as well as the price per night to create a good idea of a competitive rate at which to list your own.'),
                                    ]
                                    )
                                    ),
                                    dcc.Tab(label='Predict', value='predict', children=html.Div(children=[
                                        html.Br(),
                                        html.H3(children='Graph will update as you select features'),
                                        html.Br(),
                                        html.H6("Select your AirBnb's neighbourhood:"),
                                        dcc.Dropdown(id='dropdown',
                                                     options=[
                                                         {'label': 'Sumida', 'value': 'Sumida Ku'},
                                                         {'label': 'Chuo', 'value': 'Chuo Ku'},
                                                         {'label': 'Shinjuku', 'value': 'Shinjuku Ku'}],
                                                     value='Sumida Ku'),
                                        html.Br(),
                                        html.H6('Choose number of beds', className='my-class'),
                                        dcc.Slider(id='beds-slider',
                                                   min=0,
                                                   max=2,
                                                   step=1,
                                                   value=2,
                                                   marks={
                                                       0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                       1: {'label': '1'},
                                                       2: {'label': '2', 'style': {'color': '#f50'}}
                                                   },
                                                   ),
                                        html.Br(),
                                        html.H6('Are you a Superhost?', className='my-class'),
                                        dbc.RadioItems(id='superhost-radio',
                                                       options=[
                                                           {'label': 'Yes', 'value': 1},
                                                           {'label': 'No', 'value': 0}],
                                                       value=0),
                                        html.Br(),
                                        html.H6('Choose the maximum # of guests allowed',
                                                className='my-class'),
                                        dcc.Slider(id='accommodates-slider',
                                                   min=0,
                                                   max=6,
                                                   step=1,
                                                   value=2,
                                                   marks={
                                                       0: {'label': '0', 'style': {'color': '#77b0b1'}},
                                                       1: {'label': '1'},
                                                       2: {'label': '2'},
                                                       3: {'label': '3'},
                                                       4: {'label': '4'},
                                                       5: {'label': '5'},
                                                       6: {'label': '6'}},
                                                   ),
                                        html.Br(),
                                        html.H6('Are you a local host (living in Tokyo)?',
                                                className='my-class'),
                                        dbc.RadioItems(id='local-button',
                                                       options=[
                                                           {'label': 'Yes', 'value': 1},
                                                           {'label': 'No', 'value': 0}],
                                                       value=0),
                                        html.Br(),
                                        html.H6('Is there a hottub?', className='my-class'),
                                        dbc.RadioItems(id='hottub-button',
                                                       options=[
                                                           {'label': 'Yes', 'value': 1},
                                                           {'label': 'No', 'value': 0}],
                                                       value=0),
                                        html.Br(),
                                        html.Br(),
                                    ])
                                    ),
                                    dcc.Tab(label='Background', value='background', children=html.Div(children=[
                                        html.Br(),
                                        html.H4(children='Background:'),
                                        html.P("Tokyo AirBnb data was gathered from the InsideAirBnB website. The dataset has information on AirBnB listings in 23 neighborhoods in and around Tokyo. After exploratory data analysis and cleaning, the data had 11,612 Airbnb listings. After feature engineering (including almost 70 amenities), each Airbnb listing has 97 features such as number of guests allowed, number of beds, etc. But how can we glean insights from this?"),
                                        html.P(
                                            "Because of the high dimensionality of the data (97 features, and thus 97 dimensions), I decided to reduce the dimensions in order to visualize the similarity of different listings to each other."),
                                        html.P("In order to reduce dimensions, I first standardized this data. This centers each feature around 0, which is important when we have widely different variances (e.g. a price range of 0-1000, and range of number of beds of 0-10). Then, I applied a dimensionality reduction technique known as Principal Components Analysis, which took the data from all 97 features, and extracted 50 principal variables (or components) that represent the data. I was able to explain the maximum amount of variance that I wanted (60%, accounted for in 50 features) while retaining as much information as possible in a lower-dimensional setting."),
                                        html.P("Next, I wanted to visualize the similarity of each listing to each other in a visual way. While there are many interesting ways to do this (k-Nearest Neighbors clustering being one of them), t-Distributed Stochastic Neighbor Embedding (t-SNE) can visualize complex polynomial relationships between features and is good at visualizing high dimensional data. It measures the similarities of the inputs and the similarities of the low-dimensional points in embedding and seeks to minimize the divergence between the two. This is visualized in the graph to the right."),
                                    ])),

                                ]),
                            ]),
                        ]),
                    ]),
                dbc.Col(
                    [
                        html.Div(children=[
                            dcc.Graph(id='3d-scatter-plot'),
                        ]
                        ),

                    ]
                ),
            ]
        ),
    ]
)

#

app.layout = html.Div([navbar, body])


@app.callback(
    Output('3d-scatter-plot', 'figure'),
    [Input('dropdown', 'value'),
     Input('beds-slider', 'value'),
     Input('superhost-radio', 'value'),
     Input('accommodates-slider', 'value'),
     Input('local-button', 'value'),
     Input('hottub-button', 'value')])
def update_function(dropdown_input_value, slider_price, s, slider_acc, local, hottub):
    # filter the dataframe
    df = data_wrangling(dropdown_input_value, slider_price, s, slider_acc, local, hottub)
    # use that dataframe in the figure
    fig = px.scatter_3d(df, x='TSNE1', y='TSNE2', z='TSNE3', color='profit_category',
                        hover_name='name', hover_data=['price_per_night_in_USD', 'estimated_monthly_income_in_USD', 'minimum_nights'],
                        template='plotly_dark', opacity=0.4, title='AirBnb Listings in Feature Space',
                        labels={'TSNE1': 'X', 'TSNE2': 'Y', 'TSNE3': 'Z'})
    fig.update_layout(legend_orientation='h')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
