#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_viz.py
Created on Sat Jan 26 15:23:38 2019

@author: johnkim
"""
from TouchTunes import TouchTunes
#import matplotlib.pyplot as plt
import pandas as pd
#from bokeh.io import show, output_file
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response
from flask_table import Table, Col

#Data set 
'''
If we ever want to call
tt = TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
tt = tt.consolidate()'''

# Use local file instead
tt_df = pd.read_csv("../data/export.csv")
# Basic visualizations! 
# Count State 
state = tt_df["state"].value_counts()
# Count Style
style = tt_df["style"].value_counts()
# Count Artist 
artist_name = tt_df["artistName"].value_counts()
# Count Song Name
song_name = tt_df["songName"].value_counts()

def plot_state_count(): 
    plot = figure(x_range=list(state.index),plot_height=300,title="State Count")
    plot.vbar(x=list(state.index), top=list(state), width=0.9)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0 
    return(plot)

def plot_artist_count():
    plot = figure(x_range=list(artist_name.index),plot_height=300,title="Artist Count")
    plot.vbar(x=list(artist_name.index), top=list(artist_name), width=0.9)
    plot.xgrid.grid_line_color = None
    plot.y_range.start = 0 
    return(plot)

app = Flask(__name__)

@app.route('/')

def visualize():
    
    state = plot_state_count()
    artist = plot_artist_count()
    p = row(state,artist)
    div,script = components(p)
    
    kwargs = {'plot_script': script, 'plot_div': div}
    
    if request.method == 'GET':
        return render_template('main.html', **kwargs)
    
    abort(404)
    abort(Response('Hello'))

if __name__ == '__main__':
    app.run(debug=True)
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')
    
items = tt_df.query.all()

# Populate the table
table = ItemTable(items)


'''
# Count Style
style = tt_df["style"].value_counts()
# Count Artist 
artist_name = tt_df["artistName"].value_counts()
# Count Song Name
song_name = tt_df["songName"].value_counts()
'''
'''
output_file("states.html")
p = figure(x_range=list(state.index),plot_height=300,title="State Count",toolbar_location=None, tools="")
p.vbar(x=list(state.index), top=list(state), width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)
'''