
import src.query as query
import src.stakeholders as sh

def read_foursquare_response(data, type):

    places = data['response']['groups'][0]['items']

    temp_list = []

    for place in places:
    
        temp_dict = {}
        temp_dict['type'] = type
        temp_dict['name'] = place['venue']['name']
        lat = place['venue']['location']['lat']
        lon = place['venue']['location']['lng']

        temp_dict['location'] = {'coordinates': [lon, lat], 'type':'Point'}


        
        temp_list.append(temp_dict)

    return temp_list



def find_matches_points(offices, aux_col, distance, field):


    generator = offices.find({})
    count = 0

    while True:
        
        try:
            place = next(generator)
            location = place['location']
            
            
            
            _id = place['_id']
            
            matches = aux_col.find(
                {'$and':[
                    {'location':{
                    '$nearSphere':{
                    '$geometry': location,
                    '$maxDistance': distance 
                }
            }},{'type': field}
            
            ]}
            ,{'name':1, 'location':1, '_id':0})
            
            offices.update_one({'_id': _id}, {'$set': {field: len(list(matches))}})

            count += 1

            if count > 200: #for safety
                break
            
 
        except StopIteration:
            break

def find_all_google_places(offices, text, distance, google_api):

    generator = offices.find({})
    count = 0

    
    temp_list = []
    temp_list_ids = []

    while True:

        try:
            temp_dict = {}
            place = next(generator)

            lat = place['location']['coordinates'][1]
            lng = place['location']['coordinates'][0]

            _id = place['_id']

            res = query.google_places(text, google_api, distance,lat, lng)

            place_id = res['candidates'][0]['place_id']

            

            if place_id not in temp_list_ids:
                temp_list_ids.append(place_id)

                temp_dict['place_id'] = place_id
                temp_dict['type'] = text
                temp_dict['name'] = res['candidates'][0]['name']
                lon_ = res['candidates'][0]['geometry']['location']['lng']
                lat_ = res['candidates'][0]['geometry']['location']['lat']
                temp_dict['location'] = {'coordinates': [lon_, lat_], 'type':'Point'}

                temp_list.append(temp_dict)

            else:
                pass
        
            count += 1
            if count > 200: #for safety
                break

        except StopIteration:
            break

    return temp_list


def get_travel_time(offices, des_lat, des_lon, google_api, time):

    generator = offices.find({})
    count = 0

    while True:

        try:
            temp_dict = {}
            place = next(generator)

            lat = place['location']['coordinates'][1]
            lng = place['location']['coordinates'][0]

            _id = place['_id']

            data = query.google_maps_travel(google_api, lat, lng, des_lat, des_lon, 'driving', time)

            minutes = query.extract_duration_travel(data)

            offices.update_one({'_id': _id}, {'$set': {'driving': minutes}})

            data = query.google_maps_travel(google_api, lat, lng, des_lat, des_lon, 'transit', time)

            minutes = query.extract_duration_travel(data)

            offices.update_one({'_id': _id}, {'$set': {'transit': minutes}})

            count += 1
            if count > 200: #for safety
                break

        except StopIteration:
            break



def score_travel(row, ideal_car, ideal_transport, red, stakeholders):

    '''



    '''

    
    car_time = row['driving']
    transport_time = row['transit']
    
    score_total = sh.get_score(stakeholders, 'airport')
    
    penalty = 0
    
    if car_time > ideal_car:
        penalty += (car_time - ideal_car) * red
   
    else:
        pass
    
    if transport_time > ideal_transport:
        penalty += (transport_time - ideal_transport) * red
 
    else:
        pass

    

    score = score_total * (1- penalty)
    
    
    
    return score









            
            



            



            
            

            

            









