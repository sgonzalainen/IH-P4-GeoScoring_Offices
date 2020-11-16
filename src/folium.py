import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap
import pandas as pd
from geopy import distance
from folium import IFrame

def create_map(lat, lon, zoom_start = 10):

    '''
    Creates a map in Folium
    Args:
        lat(float): Latitude
        lon(float): Longitude
        zoom_start(int): zoom start of map, by default 10

    Returns:
        my_map(folium map)

    '''

    my_map = folium.Map(location = [lat,lon], zoom_start = 15)

    return my_map


def add_marker_icon(mymap, lat, lon, color, type_icon, icon_text, icon_color, tooltip, add, add_distance = False, dist = ''):
    '''
    Adds or returns a  marker based on some parameters
    Args:
        mymap(Folium map)
        lat(float): Latitude for marker
        lon(float): Longitude for marker
        color(str): color code for marker (used in case type_icon is 'fa')
        type_icon(str): 'fa' to used fontawesome, 'custom' to used a picture.
        icon_text(str): type of fontawesome or location for picture
        icon_color(str): color of symbol in marker if type_icon is 'fa'.
        tooltip(str): text to add to marker
        add(boolean): True if marker directly added to map. False just to return marker (for later group adding)
        add_distance(boolean): by default False, meaning no distance added to tooltip. True means distance is added to tooltip
        dist(float): distance to be added to tooltip if add_distance is True

    Returns:
        marker(Folium Marker): if add is False

    '''

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
        marker.add_to(mymap)
    else:
        return marker


def add_map_matches(mymap, winner_data, aux_col, distance, field, color, type_icon, icon_text, facolor, add):
    '''
    Find matches in a collection, groups them and adds them to map
    Args:
        mymap(Folium map)
        winner_data(dict): information of winner location
        aux_col (Mongo collection): collection with location points to find matches within
        distance(int): distance in meters to find matches
        field(str): type of venues to filter in aux_col
        color(str): color code for marker (used in case type_icon is 'fa')
        type_icon(str): 'fa' to used fontawesome, 'custom' to used a picture.
        icon_text(str): type of fontawesome or location for picture
        facolor(str): color of symbol in marker if type_icon is 'fa'.
        add(boolean): True if marker directly added to map. False just to return marker (for later group adding)
    
    Returns:

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
    '''
    Creates a heat map in a group and adds it to a map
    Args:
        collection(Mongo collection): collection with location points to find matches within
        mymap(Folium map)
        field(str): type of venues to filter in collection
    
    Returns:
    
    '''

    df = pd.DataFrame(collection.find({'type':field},{'name':1, 'location.coordinates':1,'_id':0}))
    df['lon']= df.location.apply(lambda x: x['coordinates'][0])
    df['lat']= df.location.apply(lambda x: x['coordinates'][1])

    tmp_group = folium.FeatureGroup(name = field)
    HeatMap(data = df[["lat","lon"]], radius = 15).add_to(tmp_group)

    tmp_group.add_to(mymap)


def add_closest(mymap, ref_data, aux_col, field, color, type_icon,icon_text, facolor, add ):
    '''
    For a ref collection, finds closest match in a auxiliary collection, and adds to map in a different layer
    Args:
        mymap(Folium map)
        ref_data(Mongo collection): principal collection with location points to find matches within)
        aux_col (Mongo collection): secondary collection with location points to find closest match within
        field(str): type of venues to filter in aux_col
        color(str): color code for marker (used in case type_icon is 'fa')
        type_icon(str): 'fa' to used fontawesome, 'custom' to used a picture.
        icon_text(str): type of fontawesome or location for picture
        facolor(str): color of symbol in marker if type_icon is 'fa'.
        add(boolean): True if marker directly added to map. False just to return marker (for later group adding)
    
    Returns:

    '''

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
    '''
    Adds a popup frame with text
    Returns:
        text(str): text to show in popup
        mymap(Folium map)
        lat(float): Latitude for marker
        lon(float): Longitude for marker
        width(int): width of pop_up
        height(int): height of pop_up
        max_width(int): max width of pop_up
    
    Returns:
    
    '''


    iframe = folium.IFrame(text, width=width, height=height)
    popup = folium.Popup(iframe, max_width=max_width)

    Text = folium.Marker(location=[lat,lon], popup=popup,
                        icon=folium.Icon(icon_color='green'))

    mymap.add_child(Text)

def locate_competitor(mymap, aux_col, competitor, lat, lon, ):

    '''
    Given a name, finds in a collection and adds it to map.
    Args:
        mymap(Folium map)
        aux_col (Mongo collection): collection with location points to find competitor
        competitor(str): name of competitior
        lat(float): Latitude of our office
        lon(float): Longitude of our office

    Returns:
    
    '''
    
    competitor_dict = list(aux_col.find({'name': competitor}))[0]
    competitor_lat = competitor_dict['location']['coordinates'][1]
    competitor_lon = competitor_dict['location']['coordinates'][0]

    comp_coor = (competitor_lat, competitor_lon)
    win_coor = (lat, lon)
    dist = round(distance.distance(comp_coor, win_coor).km,2)

    add_marker_icon(mymap, competitor_lat, competitor_lon, 'red','custom','src/img/supercell.png','white',competitor, True, add_distance = True, dist = dist)







































    


