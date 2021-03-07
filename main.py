import requests
import json
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.secret_key = "dontsayanybodykey"
Bootstrap(app)

API = "https://api.openbrewerydb.org/breweries?by_city="


class SearchForm(FlaskForm):
    search = StringField("Enter city name")
    submit = SubmitField("Search")
    clear = SubmitField("Clear", render_kw={'formnovalidate': True})

@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    data = {}
    if form.validate_on_submit():
        search_word = form.search.data
        response = requests.get(f"{API}{search_word}")
        response.raise_for_status()
        data = response.json()
    if form.clear.data:
        return redirect(url_for("home"))    
    return render_template("index.html", form=form, data=data)

if __name__ == "__main__":
    app.run(debug=True)
