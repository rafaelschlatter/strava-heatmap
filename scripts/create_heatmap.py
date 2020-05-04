import folium
from flask import url_for
from branca.element import Template, MacroElement


m = folium.Map(
    name="Strava Heatmap",
    tiles="cartodbpositron",
    location=[61.91, 10.76],
    zoom_start=5.3,
    control_scale=True,
)

template = """
{% macro html(this, kwargs) %}
<!doctype html>
<html lang="en">
<body>
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:0px solid grey;; background-color:rgba(255, 255, 255, 0.5);
     border-radius:6px; padding: 0px; font-size:7px; left: 50px; top: 11px;'>
     
<div class='legend-title'><a href="http://heatmap.westeurope.azurecontainer.io/" class="btn btn-outline-dark">Back to home</a></div>
</div>
</body>
</html>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)

m.get_root().add_child(macro)

m.save("app/templates/heatmap.html")
