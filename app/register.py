# app/register.py
import dash
from dash import Input, Output, State, html
from flask import session
from app.auth import register_user  # Handles user registration
from app.layouts import get_register_layout, get_login_layout

def register_register_callbacks(app):
    @app.callback(
        [Output('theme-wrapper', 'children'),  # Update the page content
         Output('register-message', 'children')],  # Display registration feedback
        [Input('register-button', 'n_clicks')],
        [State('register-username', 'value'),
         State('register-password', 'value')]
    )
    def handle_register(n_register_clicks, username, password):
        if dash.callback_context.triggered_id == 'register-button' and n_register_clicks:
            if not username or not password:
                return get_register_layout(), html.Div("Username and password are required.", style={'color': 'red'})

            # Call the registration logic
            response, status_code = register_user(username, password)
            if status_code == 201:  # Registration successful
                session['registered'] = True
                return get_login_layout(), html.Div("Registration successful. Please log in.", style={'color': 'green'})
            else:  # Registration failed
                return get_register_layout(), html.Div(response.get('error', 'Registration failed.'), style={'color': 'red'})

        return get_register_layout(), ""

    @app.callback(
        Output('theme-wrapper', 'children'),  # Update the target to 'theme-wrapper'
        [Input('go-to-login', 'n_clicks')]
    )
    def go_to_login(n_clicks):
        if dash.callback_context.triggered_id == 'go-to-login' and n_clicks:
            return get_login_layout()
        return dash.no_update
