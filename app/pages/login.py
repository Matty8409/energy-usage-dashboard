import dash
from dash import html, dcc

dash.register_page(__name__, path="/login")

layout = html.Div(id='theme-wrapper', children=[
        html.H2("Login", style={'textAlign': 'center'}),
        dcc.Input(id='username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Login', id='login-button', n_clicks=0),
        html.Button('Go to Register', id='go-to-register', n_clicks=0, style={'marginTop': '10px'}),
        html.Div(id='login-message', style={'color': 'red', 'marginTop': '10px'}),
        # Hidden registration elements
        dcc.Input(id='register-username', type='text', placeholder='Enter Username', style={'display': 'none'}),
        dcc.Input(id='register-password', type='password', placeholder='Enter Password', style={'display': 'none'}),
        html.Button('Register', id='register-button', n_clicks=0, style={'display': 'none'}),
        html.Button('Go to Login', id='go-to-login', n_clicks=0, style={'display': 'none'}),
        html.Div(id='register-message', style={'display': 'none'})
    ])

def get_login_layout():
    return layout