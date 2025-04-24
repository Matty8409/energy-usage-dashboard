# app/register.py
import dash
from dash import Input, Output, State, html
from flask import session
from app.auth import register_user  # Assume this function handles user registration
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
        if n_register_clicks:
            if not username or not password:
                return get_register_layout(), "Username and password are required."

            # Call the registration logic
            response, status_code = register_user(username, password)
            if status_code == 201:  # Registration successful
                session['registered'] = True
                return get_login_layout(), "Registration successful. Please log in."
            else:  # Registration failed
                return get_register_layout(), response.get('error', 'Registration failed.')

        return get_register_layout(), ""

    @app.callback(
        Output('theme-wrapper', 'children'),  # Update the target to 'theme-wrapper'
        [Input('go-to-login', 'n_clicks')]
    )
    def go_to_login(n_clicks):
        if n_clicks:
            return get_login_layout()
        return dash.no_update