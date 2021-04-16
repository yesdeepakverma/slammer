"""
This file serves as a common url controller
"""
from views import Login, Register, AddSlam, ListSlam, Dashboard


def add_route(app):
    api_version = 0.1

    app.add_url_rule('/', view_func=Dashboard.as_view('root'))
    app.add_url_rule('/login', view_func=Login.as_view('login'))
    app.add_url_rule('/register', view_func=Register.as_view('register'))
    app.add_url_rule('/dashboard', view_func=Dashboard.as_view('dashboard'))
    app.add_url_rule('/add_slam', view_func=AddSlam.as_view('add_slam'))
    app.add_url_rule('/list_slam', view_func=ListSlam.as_view('list_slam'))
