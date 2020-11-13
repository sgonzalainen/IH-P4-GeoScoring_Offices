import folium
from folium import Choropleth, Circle, Marker, Icon, Map

def create_map(lat, lon, zoom_start = 10):

    my_map = folium.Map(location = [lat,lon], zoom_start = 15)

    return my_map


def add_marker_icon(map, lat, lon, color, icon, icon_color, tooltip):

    icon = Icon(color = color,
             prefix = "fa",
             icon = icon,
             icon_color = icon_color,
             
             )
                                
    loc = [lat, lon]


    marker = Marker(location = loc, icon = icon, tooltip = tooltip)


    marker.add_to(map)
