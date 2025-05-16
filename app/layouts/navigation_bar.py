import dash_bootstrap_components as dbc
from dash import html, dcc

def get_navigation_bar(active_page):
    nav_items = [
        {'label': 'Dashboard', 'href': '/dashboard', 'color': 'info'},
        {'label': 'Statistics', 'href': '/statistics', 'color': 'success'},
        {'label': 'Collections', 'href': '/save-data-collection', 'color': 'primary'},
        {'label': 'Costs and Carbon', 'href': '/costs-and-carbon', 'color': 'warning'}
    ]
    return dbc.Navbar(
        dbc.Container([
            dbc.Nav(
                [
                    dbc.NavItem(
                        dcc.Link(
                            html.Div(
                                item['label'],
                                className=f"nav-link {'active' if active_page == item['href'] else ''}"
                            ),
                            href=item['href'],
                            style={'textDecoration': 'none'}
                        )
                    ) for item in nav_items
                ],
                className='d-flex justify-content-center'
            )
        ]),
        color="white",
        dark=False,
        className="mt-4 navbar-light-mode"
    )