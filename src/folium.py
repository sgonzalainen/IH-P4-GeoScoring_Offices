import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap
import pandas as pd
from geopy import distance
from folium import IFrame

def create_map(lat, lon, zoom_start = 10):

    my_map = folium.Map(location = [lat,lon], zoom_start = 15)

    return my_map


def add_marker_icon(map, lat, lon, color, type_icon, icon_text, icon_color, tooltip, add, add_distance = False, dist = ''):

    if type_icon == 'fa':
    
        icon = Icon(color = color,
                prefix = "fa",
                icon = icon_text,
                icon_color = icon_color,
                
                )
    elif type_icon == 'custom':
        #https://ocefpaf.github.io/python4oceanographers/blog/2015/11/02/icons/

        icon = folium.features.CustomIcon(icon_text,
                                          icon_size=(50, 50))

    else:
        pass



                                
    loc = [lat, lon]

    if add_distance:
        tooltip = f'{tooltip}\n {dist} km'
    else:
        pass


    marker = Marker(location = loc, icon = icon, tooltip = tooltip)

    

    if add:

        marker.add_to(map)

    else:
        return marker


def add_map_matches(mymap, winner_data, aux_col, distance, field, color, type_icon, icon_text, facolor, add):
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
        
        marker  = add_marker_icon(mymap, lat, lon, color, type_icon , icon_text,facolor,name, add)
        marker.add_to(tmp_group)


    tmp_group.add_to(mymap)

    
    

def add_heat_map(collection, mymap, field):

    df = pd.DataFrame(collection.find({'type':field},{'name':1, 'location.coordinates':1,'_id':0}))
    df['lon']= df.location.apply(lambda x: x['coordinates'][0])
    df['lat']= df.location.apply(lambda x: x['coordinates'][1])

    tmp_group = folium.FeatureGroup(name = field)
    HeatMap(data = df[["lat","lon"]], radius = 15).add_to(tmp_group)

    tmp_group.add_to(mymap)


def add_closest(mymap, ref_data, aux_col, field, color, type_icon,icon_text, facolor, add ):

    ref_coordinates = (ref_data['location']['coordinates'][1],ref_data['location']['coordinates'][0])

    df_a = pd.DataFrame(aux_col.find({'type':field},{'name':1, 'location.coordinates':1,'_id':0}))
    df_a['lon']= df_a.location.apply(lambda x: x['coordinates'][0])
    df_a['lat']= df_a.location.apply(lambda x: x['coordinates'][1])

    df_a['distance'] = df_a.apply(lambda x: (distance.distance(ref_coordinates,(x['lat'],x['lon'])).km), axis = 1)

    closest = df_a.sort_values('distance').head(1)

    clos_lat = closest.lat.values[0]
    clos_lon = closest.lon.values[0]
    clos_dis = round(closest.distance.values[0],2)


    name = closest.name.values[0]

    tmp_group = folium.FeatureGroup(name = f'closest {field}')

    marker  = add_marker_icon(mymap, clos_lat, clos_lon, color, type_icon , icon_text,facolor,name, add, True, clos_dis)

    marker.tooltip = f'{name}: {clos_dis} km'

    marker.add_to(tmp_group)

    tmp_group.add_to(mymap)

def add_pop_up(text, mymap, lat, lon, width = 200, height = 100, max_width = 500):


    iframe = folium.IFrame(text, width=width, height=height)
    popup = folium.Popup(iframe, max_width=max_width)

    Text = folium.Marker(location=[lat,lon], popup=popup,
                        icon=folium.Icon(icon_color='green'))

    mymap.add_child(Text)

def locate_competitor(mymap, aux_col, competitor, lat, lon, ):


    
    competitor_dict = list(aux_col.find({'name': competitor}))[0]
    competitor_lat = competitor_dict['location']['coordinates'][1]
    competitor_lon = competitor_dict['location']['coordinates'][0]

    comp_coor = (competitor_lat, competitor_lon)
    win_coor = (lat, lon)
    dist = round(distance.distance(comp_coor, win_coor).km,2)

    add_marker_icon(mymap, competitor_lat, competitor_lon, 'red','custom','src/img/supercell.png','white',competitor, True, add_distance = True, dist = dist)







































    


