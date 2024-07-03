from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    users = [
        {
            "name": "Lisa",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Anna",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Annie",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Benjamin",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Connor",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Jeff",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Joelle",
            "colour": "#0000FFA0"
        },
        {
            "name": "Nabla",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Sigh",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Sophy",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Felisha",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Cherry",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Ericknash",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Freyah",
            "colour": "#FF8EBAA0"
        },
        {
            "name": "Hailee",
            "colour": "#FF8EBAA0"
        }
    ]
    return render_template("index.html", title="Sign In", users=users)