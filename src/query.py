
import requests
from datetime import datetime

###################### FUNCTIONS RELATED TO QUERIES #####################


def foursquare_query(lat, lon, cat, radius, client_id, client_secret, limit = 100):
    '''
    Performs query in foursquare Places API related to a location and a category
    Args:
        lat(float): Latitude
        lon (float): Longitude
        cat(str): category code by API
        radius(int): radius for location in meters
        client_id(str): API token
        client_secret(str): API token2
        limit(int): number of returns, by defaul maximum of API, i.e. 100

    Returns:
        resp(json): request response

    '''
    #acc. to API
    foursquare_cat_ids = {'vegan_rest': '4bf58dd8d48988d1d3941735',
             'tech_startup': '4bf58dd8d48988d125941735',
             'coworking_space': '4bf58dd8d48988d174941735',
             'design_studio': '4bf58dd8d48988d1f4941735',
             'pub': '4bf58dd8d48988d11b941735',
             'night_club': '4bf58dd8d48988d11f941735',
             'basket_stadium': '4bf58dd8d48988d18b941735',
             'starbucks': '556f676fbd6a75a99038d8ec',
             'preschool': '52e81612bcbc57f1066b7a45',
             'nurseryschool': '4f4533814b9074f6e4fb0107'}

    endpoint = 'https://api.foursquare.com/v2/venues/explore'

    cat = foursquare_cat_ids[cat]

    params = { "client_id" : client_id,
          "client_secret" : client_secret,
          "v" : "20180323",
          "ll": f'{lat},{lon}',
          'radius': radius,
          "categoryId": cat,
          "limit" : limit
            }

    resp = requests.get (endpoint, params = params)

    try:
        return resp.json()
    except:
        return resp






def google_places(text, key, radius, lat, lon):
    '''
    Performs query in Google Places API related to a location and a text
    Args:
        text(str): search text
        key(str): API token
        radius(int): radius for location in meters
        lat(float): Latitude
        lon (float): Longitude

    Returns:
        resp(json): request response

    '''

    endpoint = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = { "key" : key,
          "input" : text,
          "inputtype" : "textquery",
          'locationbias': f'circle:{radius}@{lat},{lon}',
          'fields': 'place_id,name,geometry'
    
            }

    resp = requests.get (endpoint, params = params)
    try:
        return resp.json()
    except:
        return resp


def google_maps_travel(key, ori_lat, ori_lon, des_lat, des_lon, mode, time):
    '''
    Performs query in Google Routes API related to a origin and destination
    Args:
        key(str): API token
        ori_lat(float): latitude origin point
        ori_lon(float): longitude origin point
        des_lat(float): latitud destination point
        des_lon(float): longitude destination point
        mode (str): 'driving' or 'transit'
        time(int): arrival time in seconds since 1stJan 1970.

    Returns:
        resp(json): request response

    '''

    endpoint = 'https://maps.googleapis.com/maps/api/directions/json'


    params = { "key" : key,
        "origin" : f'{ori_lat},{ori_lon}',
        "destination" : f'{des_lat},{des_lon}',
        'mode': mode,
        'arrival_time': time

        }

    resp = requests.get (endpoint, params = params)

    try:
        return resp.json()
    except:
        return resp




def get_time_for_google(year, month, day, hour):
    '''
    Given a date, returns date in seconds since 1stJan 1970
    Args:
        year(int): year
        month(int): month
        day(int): day
        hour(int): hour

    Returns:
        date_sec(int): seconds since 1stJan 1970 UTM

    '''
    date = datetime.now()
    date = date.replace(minute = 0, hour = 12, second = 0, year = 2020, month = 11, day = 17)
    date_sec = int(date.timestamp())

    return date_sec


def extract_duration_travel(data):
    '''
    Given a google route json response, returns total time of travel
    Args:
        data(json): response data from API

    Returns:
        time(float): total travel time in minutes

    '''

    seconds = 0
    for route in data['routes']:
        for leg in route['legs']:
            seconds += leg['duration']['value']

    time = round(seconds/60,1)

    return time





















    


    

