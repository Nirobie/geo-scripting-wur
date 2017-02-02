from twython import Twython

## Function to get twitter's placeID, requires pair of coordinates and twitter
## api credentials:'APP_KEY','APP_SECRET','OAUTH_TOKEN','OAUTH_TOKEN_SECRET'
## stores the result in a csv file.

def get_city_id(latitude, longitude, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    
    # Initializes Twython object
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    # Calls the API and stores the results in a variable
    search_results = twitter.reverse_geocode(lat=latitude, long=longitude, granularity="city")
    # Name of the output file
    output_file = 'places.csv'
    # Declares empty list to store existing cities
    existing_cities = []
    ## If exists, retrieves name of cities in output file
    try:
        with open("data/" + output_file, 'r') as existing_file:
            for city in existing_file:
                attr = city.split(";")
                existing_cities.append(attr[0])
            existing_file.close()
    except:
        print "Creating file data/" + output_file
    ## Opens ouput file to append new results
    target = open("data/" + output_file, 'a')
    ## Saves new results in output file
    for result in search_results['result']['places']:
            # Evaluates and writes in file if the place is a city and it is not
            # in the existing cities' list.
            if result['place_type'] == "city" and result['full_name'] not in existing_cities:
                city = result['full_name']
                place_id = result['id']
                lat_c = result['centroid'][0]
                long_c = result['centroid'][1]
                print "Saving " + city + " placeID into file"
                target.write(city + ';' + place_id + ';' + str(lat_c) + ';' + str(long_c))
                target.write('\n')   
    target.close()