from flask import render_template, redirect, url_for
from app import app

users = [
    {
        "name": "Lisa",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Anna",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Annie",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Benjamin",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Connor",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Jeff",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Joelle",
        "color": "#0000FFA0"
    },
    {
        "name": "Nabla",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Sigh",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Sophy",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Felisha",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Cherry",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Ericknash",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Freyah",
        "color": "#FF8EBAA0"
    },
    {
        "name": "Hailee",
        "color": "#FF8EBAA0"
    }
]

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for("select_user"))

@app.route('/select_user')
def select_user():
    return render_template("select_user.html", title="Select User", users=users)

@app.route('/sign_in/<username>')
def sign_in(username):
    joelle = {
        "name": "Joelle",
        "color": "#0000FFA0"
    }
    return render_template("sign_in.html", title="Sign In", user=joelle)