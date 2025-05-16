from dash import html, dcc

def get_register_layout():
    register_layout = html.Div(id='theme-wrapper', children=[
        html.H2("Register", style={'textAlign': 'center'}),
        dcc.Input(id='register-username', type='text', placeholder='Enter Username', style={'margin': '10px'}),
        dcc.Input(id='register-password', type='password', placeholder='Enter Password', style={'margin': '10px'}),
        html.Button('Register', id='register-button', n_clicks=0),
        html.Button('Go to Login', id='go-to-login', n_clicks=0, className='me-1 mt-1 btn btn-primary', style={'marginTop': '10px'}),
        html.Div(id='register-message', className='register-message'),
        # Hidden login elements
        dcc.Input(id='register-username', value='', type='text', style={'display': 'none'}),
        dcc.Input(id='register-password', value='', type='password', style={'display': 'none'}),
        html.Button('Login', id='login-button', n_clicks=0, className='me-1 mt-1 btn btn-primary' ,style={'display': 'none'}),
        html.Div(id='login-message')
    ])
    return register_layout