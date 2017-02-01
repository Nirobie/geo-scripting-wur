from twython import Twython

### Local Variables

##codes to access twitter API. 

APP_KEY = "9jlDDVPYsigPe8Ao9UbnqjQ7Q"
APP_SECRET = "jVHAOFrKHfpBOaJzH2K0F0ZRgB3bz5rVdlqoGQAup5tXaaspGT"
OAUTH_TOKEN = "102152165-Sdv2opvPufyotWasY7U2C5G1ofxrckFvDtKKvTpx"
OAUTH_TOKEN_SECRET = "FoBl3PW21BZoUeYi4WDbcUHuMC4YTAL5ZOvctMVB3eAsl"

##initiating Twython object

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### Code

## Get twitter place id 

def get_city_id(latitude, longitude):
    search_results = twitter.reverse_geocode(lat=latitude, long=longitude, granularity="city")
    
    output_file = 'places.csv' 
    target = open("data/" + output_file, 'a')

    for result in search_results['result']['places']:
            place_type = result['place_type']
            if place_type == "city":
                city = result['full_name']
                place_id = result['id']
                lat_c = result['centroid'][0]
                long_c = result['centroid'][1]
                target.write(city + ';' + place_id + ';' + str(lat_c) + ';' + str(long_c))
                target.write('\n')
        
    target.close()