import folium
from folium import Choropleth, Circle, Marker, Icon, Map

def create_map(lat, lon, zoom_start = 10):

    my_map = folium.Map(location = [lat,lon], zoom_start = 15)

    return my_map


def add_marker_icon(map, lat, lon, color, type_icon, icon_text, icon_color, tooltip, add):

    if type_icon == 'fa':
    
        icon = Icon(color = color,
                prefix = "fa",
                icon = icon_text,
                icon_color = icon_color,
                
                )
    elif type_icon == 'custom':

        icon = folium.features.CustomIcon(icon_text,
                                          icon_size=(50, 50))

    else:
        pass



                                
    loc = [lat, lon]


    marker = Marker(location = loc, icon = icon, tooltip = tooltip)

    

    if add:

        marker.add_to(map)

    else:
        return marker


def add_map_matches(map, winner_data, aux_col, distance, field, color, type_icon, icon_text, facolor, add):
    '''


    '''


    matches = list(aux_col.find(
                {'$and':[
                    {'location':{
                    '$nearSphere':{
                    '$geometry': winner_data['location'],
                    '$maxDistance': distance 
                }
            }},{'type': field}]}))

    
    tmp_group = folium.FeatureGroup(name = field)

    for match in matches:
        lat = match['location']['coordinates'][1]
        lon = match['location']['coordinates'][0]
        name = match['name']
        
        marker  = add_marker_icon(map, lat, lon, color, type_icon , icon_text,facolor,name, add)
        marker.add_to(tmp_group)


    tmp_group.add_to(map)

    



    return map
    


