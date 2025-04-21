import html
from dash import Output, Input, State
from app.layouts import get_register_layout


def register_register_callbacks(app):
    @app.callback(
        Output('theme-wrapper', 'children'),
        [Input('register-button', 'n_clicks')],
        [State('register-username', 'value'), State('register-password', 'value')]
    )
    def handle_registration(n_clicks, username, password):
        if n_clicks:
            from app.auth import register_user
            response, status_code = register_user(username, password)
            if status_code == 201:  # Registration successful
                return html.Div([
                    html.H2("Registration Successful!", style={'textAlign': 'center'}),
                    html.Button('Go to Login', id='go-to-login', n_clicks=0)
                ])
            else:  # Registration failed
                return html.Div([
                    get_register_layout(),
                    html.Div(response['error'], style={'color': 'red', 'marginTop': '10px'})
                ])
        return get_register_layout()