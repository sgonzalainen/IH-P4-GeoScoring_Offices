
import requests




def foursquare_query(lat, lon, cat, radius, client_id, client_secret, limit = 100):


    foursquare_cat_ids = {'vegan_rest': '4bf58dd8d48988d1d3941735',
             'tech_startup': '4bf58dd8d48988d125941735',
             'coworking_space': '4bf58dd8d48988d174941735',
             'design_studio': '4bf58dd8d48988d1f4941735',
             'pub': '4bf58dd8d48988d11b941735',
             'karaoke_bar': '4bf58dd8d48988d120941735',
             'night_club': '4bf58dd8d48988d11f941735',
             'basketball_stadium': '4bf58dd8d48988d18b941735',
             'starbucks': '556f676fbd6a75a99038d8ec'}

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


def read_foursquare_response(data):

    places = data['response']['groups'][0]['items']

    temp_list = []

    for place in places:
    
        temp_dict = {}
        temp_dict['name'] = place['venue']['name']
        lat = place['venue']['location']['lat']
        lon = place['venue']['location']['lng']

        temp_dict['location'] = {'coordinates': [lon, lat], 'type':'Point'}


        
        temp_list.append(temp_dict)

    return temp_list

def find_matches_points(offices, aux_col, distance, field):


    generator = offices.find({})
    while True:
        
        try:
            place = next(generator)
            location = place['location']
            
            
            name = place['name']
            _id = place['_id']
            
            matches = aux_col.find(
            {'location':{
                '$nearSphere':{
                    '$geometry': location,
                    '$maxDistance': distance * 1000
                }
            }},{'name':1, 'location':1, '_id':0})
            
            offices.update_one({'_id': _id}, {'$set': {field: len(list(matches))}})
            
 
        except StopIteration:
            break

def google_places(text, key, radius, lat, lon):

    endpoint = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'


    params = { "key" : key,
          "input" : text,
          "inputtype" : "textquery",
          'locationbias': f'circle:{radius}@{lat},{lon}',
          'fields': 'name,geometry'
    
            }


    resp = requests.get (endpoint, params = params)

    try:
        return resp.json()
    except:
        return resp











    


    

