import dash_bootstrap_components as dbc
from dash import html, dcc

def get_login_layout():
    login_layout = dbc.Container([
        html.H2("Login", className="text-center my-4"),
        dbc.Input(id='username', type='text', placeholder='Enter Username', className='mb-3 login-input'),
        dbc.Input(id='password', type='password', placeholder='Enter Password', className='mb-3 login-input'),
        html.Div([
            dbc.Button('Login', id='login-button', color='primary', className='btn-primary login-button')
        ], className='login-button-group'),
        html.Div(id='login-message', className='text-danger mt-3')
    ], id='theme-wrapper', className='p-4')
    return login_layout