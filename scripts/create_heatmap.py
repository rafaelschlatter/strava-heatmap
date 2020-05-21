import os
import requests
import logging
import json
import folium
import time
from stravaio import StravaIO
from stravaio import strava_oauth2
from branca.element import Template, MacroElement

if time.time() > int(os.environ["STRAVA_TOKEN_EXPIRES_AT"]):
    logging.critical("Access token expired. Need to refresh token.")
    
    payload = {
        "client_id": os.environ["STRAVA_CLIENT_ID"],
        "client_secret": os.environ["STRAVA_CLIENT_SECRET"],
        "grant_type": "refresh_token",
        "refresh_token": os.environ["STRAVA_REFRESH_TOKEN"]
    }

    response = requests.request("POST", "https://www.strava.com/api/v3/oauth/token", data=payload)
    response_dict = json.loads(response.text)
    
    os.environ["STRAVA_ACCESS_TOKEN"] = str(response_dict["access_token"]) 
    os.environ["STRAVA_REFRESH_TOKEN"] = str(response_dict["refresh_token"]) 
    os.environ["STRAVA_TOKEN_EXPIRES_AT"] = str(response_dict["expires_at"]) 
else:
    logging.critical("Access token still valid. Can use existing token.")

client = StravaIO(access_token=os.environ["STRAVA_ACCESS_TOKEN"])
athlete = client.get_logged_in_athlete()
activities = client.get_logged_in_athlete_activities(after=20170101)

m = folium.Map(
    name="Strava Heatmap",
    tiles='cartodbdark_matter',
    location=[59.925,10.728123],
    zoom_start=11.5,
    control_scale=True
)

template = """
{% macro html(this, kwargs) %}
<!doctype html>
<html lang="en">
<body>
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:0px solid grey;; background-color:rgba(255, 255, 255, 0.9);
     border-radius:6px; padding: 0px; left: 50px; top: 11px;'>
     
<div class='home-button'><a href="https://my-heatmap.azurewebsites.net/" class="btn btn-outline-dark">Back to home</a></div>
</div>

<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:1px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:15px; right: 13px; top: 11px;'>
     
<div class='legend-title'>Activity type</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:#00ffff;opacity:0.7;'></span>Ski</li>
    <li><span style='background:#ff9933;opacity:0.7;'></span>Run</li>
    <li><span style='background:#ff3399;opacity:0.7;'></span>Ride</li>
    <li><span style='background:#cc00ff;opacity:0.7;'></span>Other</li>
  </ul>
</div>
</div>

</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)

for a in activities:
    if a.type == "Workout":
        continue
    streams = client.get_activity_streams(a.id, athlete.id)
    try:
        points = list(zip(streams.lat, streams.lng))
        if a.type == "Run":
            folium.PolyLine(locations=points,color="#ff9933", opacity=1/2, weight=1).add_to(m)
        elif a.type == "Ride":
            folium.PolyLine(locations=points,color="#ff3399", opacity=1/2, weight=1).add_to(m)
        elif a.type == "NordicSki":
            folium.PolyLine(locations=points,color="#00ffff", opacity=1/2, weight=1).add_to(m)
        else:
            folium.PolyLine(locations=points,color="#cc00ff", opacity=1/2, weight=1).add_to(m)
        print(a.id)
    except:
        pass

m.save("app/templates/heatmap.html")
