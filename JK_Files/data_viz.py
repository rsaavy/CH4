#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_viz.py
Created on Sat Jan 26 15:23:38 2019

@author: johnkim
"""
#from TouchTunes import TouchTunes
#import matplotlib.pyplot as plt
import pandas as pd
#from bokeh.io import show, output_file

from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, request, render_template, abort, Response

tt = pd.read_csv("/Users/johnkim/Documents/GitHub/CH4/JK_Files/export.csv")
# Basic visualizations! 
# Count State 
state = tt["state"].value_counts()

app = Flask(__name__)

@app.route('/')

def hello():
    '''
    plot = figure(x_range=list(state.index),plot_height=300,title="State Count",toolbar_location=None, tools="")
    
    script, div = components(plot)
    '''
    
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend="Temp.", line_width=2)

    div, script = components(p)    
    
    kwargs = {'plot_script': script, 'plot_div': div}
    
    if request.method == 'GET':
        return render_template('main.html', **kwargs)
    
    abort(404)
    abort(Response('Hello'))

if __name__ == '__main__':
    app.run(debug=True)

'''
If we ever want to call 
#tt = TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
#x = tt.consolidate()
'''


'''
# Count Style
style = tt["style"].value_counts()
# Count Artist 
artist_name = tt["artistName"].value_counts()
# Count Song Name
song_name = tt["songName"].value_counts()
'''
'''
output_file("states.html")
p = figure(x_range=list(state.index),plot_height=300,title="State Count",toolbar_location=None, tools="")
p.vbar(x=list(state.index), top=list(state), width=0.9)
p.xgrid.grid_line_color = None
p.y_range.start = 0
show(p)
'''