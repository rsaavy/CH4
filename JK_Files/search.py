from flask import Flask, request, render_template, redirect, url_for, session, abort, Response
from TouchTunes import TouchTunes
import numpy as np
import pandas as pd

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.embed import components

#Map imports
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import EventFinder

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Map API Key
API_KEY = "AIzaSyDpmIgC3TIm-h2sbkLvDNUHbn5e0ql0YG8"
# you can set key as config
app.config['GOOGLEMAPS_KEY'] = API_KEY
GoogleMaps(app)

# Map display functions
def getSongAmt(touchtunes_events_pnda):
    indices = []
    for i in range(0, len(touchtunes_events_pnda)):
        # TouchTune data - only get once
        if i == 0 or touchtunes_events_pnda["latitude"][i-1] != touchtunes_events_pnda["latitude"][i]:
            indices.append(i);
    return indices

def genMarkerData(touchtunes_events_pnda):

    indices = getSongAmt(touchtunes_events_pnda)
    j = 0

    markers = []

    for i in range(0, len(touchtunes_events_pnda)):

        if i == indices[0] or i == indices[1] or i == indices[2] or i == indices[3]:
            markers.append(
                  {
                    'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                    'lat': touchtunes_events_pnda["latitude"][i],
                    'lng': touchtunes_events_pnda["longitude"][i],
                    'infobox': "<h3>TouchTunes Jukebox <br><br/>Last Played Song: %s by %s on %s </h3>" % (touchtunes_events_pnda["songName"][i], touchtunes_events_pnda["artistName"][i], touchtunes_events_pnda["playDate"][i])
                  }
            )
        markers.append({
            'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            'lat': touchtunes_events_pnda["location"][i][1],
            'lng': touchtunes_events_pnda["location"][i][0],
            'infobox': "<h3>Event Featuring: %s</h3><p>Description: %s</p>" % (touchtunes_events_pnda["title"][i], touchtunes_events_pnda["description"][i])
        })
    return markers
#######

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

    plot = visualize_counts(tt_df)
    div,script = components(plot)

    # Map cosas
    touchtunes_pnda = tt_df.drop_duplicates().reset_index()
    touchtunes_events_pnda = EventFinder.mergeEvent(touchtunes_pnda)
    data = genMarkerData(touchtunes_events_pnda)
    indices = getSongAmt(touchtunes_events_pnda)

    sndmap0 = Map(
            identifier="sndmap0",
            lat=data[indices[0]]['lat'],
            lng=data[indices[0]]['lng'],
            style="height:700px;width:700px;margin:0;",
            markers=genMarkerData(touchtunes_events_pnda)[0:indices[1]]
            )
    sndmap1 = Map(
            identifier="sndmap1",
            lat=data[indices[1]+1]['lat'],
            lng=data[indices[1]+1]['lng'],
            style="height:700px;width:700px;margin:0;",
            markers=genMarkerData(touchtunes_events_pnda)[indices[1]:indices[2]]
            )
    sndmap2 = Map(
            identifier="sndmap2",
            lat=data[indices[2]+1]['lat'],
            lng=data[indices[2]+1]['lng'],
            style="height:700px;width:700px;margin:0;",
            markers=genMarkerData(touchtunes_events_pnda)[indices[2]:indices[3]]
            )
    sndmap3 = Map(
            identifier="sndmap3",
            lat=data[indices[3]+1]['lat'],
            lng=data[indices[3]+1]['lng'],
            style="height:700px;width:700px;margin:0;",
            markers=genMarkerData(touchtunes_events_pnda)[indices[3]:]
            )
        ########


    return render_template('results.html',  table=tt_df.to_html(), plot_script=script, plot_div=div, sndmap0=sndmap0, sndmap1=sndmap1, sndmap2=sndmap2, sndmap3=sndmap3)
    abort(404)
    abort(Response('Hello'))
    #return render_template('results.html',  tables=[tt_df.to_html(classes='data')], titles=tt_df.columns.values)
    #return render_template("results.html")

# VIZ Code
'''
# Basic visualizations!
# Count State
state = tt_df["state"].value_counts()
# Count Style
style = tt_df["style"].value_counts()
# Count Artist
artist_name = tt_df["artistName"].value_counts()
'''

def plot_state_count(df):
    state = df["state"].value_counts()
    plot = figure(x_range=list(state.index),plot_height=300,title="State Count")
    plot.vbar(x=list(state.index), top=list(state), width=0.9)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    return(plot)

def plot_artist_count(df):
    artist_name = df["artistName"].value_counts()
    plot = figure(x_range=list(artist_name.index),plot_height=300,title="Artist Count")
    plot.vbar(x=list(artist_name.index), top=list(artist_name), width=0.9)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    return(plot)

def plot_style_count(df):
    style = df["style"].value_counts()
    plot = figure(x_range=list(style.index),plot_height=300,title="Style Count")
    plot.vbar(x=list(style.index), top=list(style), width=0.9)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0
    return(plot)

def visualize_counts(df):

    state = plot_state_count(df)
    artist = plot_artist_count(df)
    style = plot_style_count(df)

    p = row(state,artist,style)
    return(p)


if __name__ == '__main__':
    app.run()
