import os
import requests
import logging
import json
import time
import folium
from folium.plugins import HeatMap, LocateControl
from stravaio import StravaIO
from branca.element import Template, MacroElement


def refresh_token():
    if time.time() > int(os.environ["STRAVA_TOKEN_EXPIRES_AT"]):
        logging.critical("Access token expired. Need to refresh token.")

        payload = {
            "client_id": os.environ["STRAVA_CLIENT_ID"],
            "client_secret": os.environ["STRAVA_CLIENT_SECRET"],
            "grant_type": "refresh_token",
            "refresh_token": os.environ["STRAVA_REFRESH_TOKEN"],
        }

        response = requests.request(
            "POST", "https://www.strava.com/api/v3/oauth/token", data=payload
        )
        response.raise_for_status()
        response_dict = json.loads(response.text)

        os.environ["STRAVA_ACCESS_TOKEN"] = str(response_dict["access_token"])
        os.environ["STRAVA_REFRESH_TOKEN"] = str(response_dict["refresh_token"])
        os.environ["STRAVA_TOKEN_EXPIRES_AT"] = str(response_dict["expires_at"])
    else:
        logging.critical("Access token still valid. Can use existing token.")


def add_html(m):
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
        border-radius:6px; padding: 10px; font-size:15px; right: 11px; top: 150px;'>
        
    <div class='legend-title'>Activity type</div>
    <div class='legend-scale'>
    <ul class='legend-labels'>
        <li><span style='background:#ff9933;opacity:0.7;'></span>Run</li>
        <li><span style='background:#f6ff00;opacity:0.7;'></span>Ice Skate</li>
        <li><span style='background:#00ff55;opacity:0.7;'></span>Canoe</li>
        <li><span style='background:#00ffff;opacity:0.7;'></span>Nordic Ski</li>
        <li><span style='background:#00ccff;opacity:0.7;'></span>Alpine Ski</li>
        <li><span style='background:#0066ff;opacity:0.7;'></span>Ride</li>
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

    return m


def downsample(l, n):
    """Returns every nth element from list l. Returns the
    original list if n is set to 1.
    Used to reduce the number of GPS points per activity,
    to improve performance of the website.
    """

    return l[0::n]


def download_data(activities, reduce_sample=True):
    data = []
    for a in activities:
        if a.type == "Workout":
            continue
        streams = client.get_activity_streams(a.id, athlete.id)
        time.sleep(12) # trying to circumvent Strava api limits
        try:
            points = list(zip(streams.lat, streams.lng))
            if reduce_sample:
                points = downsample(l=points, n=4)
            activity = {"id": a.id, "type": a.type, "coordinates": points}
            data.append(activity)
            logging.critical("Downloaded activity with id: {}".format(a.id))
        except Exception:
            logging.error("Failed to download activity with id: {}".format(a.id))

    return data


def create_activity_layer(activities, opacity=0.5, weight=1):
    activity_layer = folium.FeatureGroup(name="Activities", show=True, overlay=True)

    if len(activities) == 0:
        logging.info("No activities found, returning empty folium map.")
        return None

    data = []
    for a in activities:
        if a["type"] == "Workout":
            continue

        if a["type"] == "Run":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#ff9933",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        elif a["type"] == "Ride":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#0066ff",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        elif a["type"] == "NordicSki":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#00ffff",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        elif a["type"] == "AlpineSki":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#00ccff",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        elif a["type"] == "Canoeing":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#00ff55",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        elif a["type"] == "IceSkate":
            folium.PolyLine(
                locations=a["coordinates"],
                color="#f6ff00",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
        else:
            folium.PolyLine(
                locations=a["coordinates"],
                color="#cc00ff",
                opacity=opacity,
                weight=weight,
            ).add_to(activity_layer)
    logging.critical("Successfully created activity layer.")

    return activity_layer


def create_heatmap_layer(data, radius=5, blur=5):
    heatmap_layer = folium.FeatureGroup(name="Heatmap", show=False, overlay=True)
    heatmap_data = []
    for activity in data:
        heatmap_data.append(activity["coordinates"])

    flat_list = [item for sublist in heatmap_data for item in sublist]
    HeatMap(data=flat_list, radius=radius, blur=blur,).add_to(heatmap_layer)
    logging.critical("Successfully created heatmap layer.")

    return heatmap_layer


if __name__ == "__main__":
    refresh_token()
    client = StravaIO(access_token=os.environ["STRAVA_ACCESS_TOKEN"])
    athlete = client.get_logged_in_athlete()
    activities = client.get_logged_in_athlete_activities(after=20170101)

    data = download_data(activities=activities, reduce_sample=True)
    activity_layer = create_activity_layer(activities=data, opacity=0.5, weight=2)
    heatmap_layer = create_heatmap_layer(data=data, radius=5, blur=5)

    m = folium.Map(
        name="Strava Heatmap",
        tiles="cartodbpositron",
        location=[59.925, 10.728123],
        zoom_start=11.5,
        control_scale=True,
    )
    m = add_html(m)
    
    folium.TileLayer("cartodbpositron").add_to(m)
    folium.TileLayer("cartodbdark_matter").add_to(m)
    # heatmap_layer.add_to(m)
    activity_layer.add_to(m)
    LocateControl().add_to(m)
    folium.LayerControl().add_to(m)

    m.save("app/templates/heatmap.html")
