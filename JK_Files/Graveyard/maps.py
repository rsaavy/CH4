# API Key: AIzaSyDpmIgC3TIm-h2sbkLvDNUHbn5e0ql0YG8
import requests
import json
import EventFinder
import TouchTunes
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


# https://www.google.com/maps/embed/v1/view?key=AIzaSyDpmIgC3TIm-h2sbkLvDNUHbn5e0ql0YG8&center=44.518958,-88.020313&zoom=18

API_KEY = "AIzaSyDpmIgC3TIm-h2sbkLvDNUHbn5e0ql0YG8"

touchtunes_data = TouchTunes.TouchTunes("2018-02-19","21:00:00","2018-02-19","22:00:00",0)
touchtunes_pnda = touchtunes_data.consolidate().drop_duplicates().reset_index()
touchtunes_events_pnda = EventFinder.mergeEvent(touchtunes_pnda)


app = Flask(__name__)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDpmIgC3TIm-h2sbkLvDNUHbn5e0ql0YG8"


app = Flask(__name__, template_folder=".")
GoogleMaps(app)

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


@app.route("/")
def mapview():
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
    return render_template('map.html', sndmap0=sndmap0, sndmap1=sndmap1, sndmap2=sndmap2, sndmap3=sndmap3)

if __name__ == "__main__":
    app.run(debug=False)

data = genMarkerData(touchtunes_events_pnda)
print(data)
