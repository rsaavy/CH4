from flask import Flask, request, render_template, redirect, url_for, session
from TouchTunes import TouchTunes
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods=["GET","POST"])
def main_page():

    if request.method == "POST":

        if request.form['search_button'] == "search":
            start_date = request.args.get("start-date")
            end_date = request.args.get("end-date")
            start_date = request.form["start-date"]
            end_date = request.form["end-date"]
            session["start_date"] = start_date
            session["end_date"] = end_date

            return redirect(url_for('results'))

    return render_template("search.html")

@app.route('/results')
def results():
    tt_df = TouchTunes(session.get("start_date"),"00:00:00",session.get("end_date"),"23:59:59",0).consolidate()
    return render_template('results.html',  table=tt_df.to_html())
    #return render_template('results.html',  tables=[tt_df.to_html(classes='data')], titles=tt_df.columns.values)
    #return render_template("results.html")


if __name__ == '__main__':
    app.run()
