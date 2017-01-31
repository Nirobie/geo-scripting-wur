import zipfile, urllib2, shapefile, datetime
from twython import Twython
from json import dumps

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
    target = open(output_file, 'a')

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

## Download required files and unpack them to the data folder

response = urllib2.urlopen('http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_ua10_500k.zip')
zipcontent= response.read()
with open("cb_2015_us_ua10_500k.zip", 'w') as f:
    f.write(zipcontent)

zip_ref = zipfile.ZipFile("cb_2015_us_ua10_500k.zip", 'r')
zip_ref.extractall("data/us_cities")
zip_ref.close()

response = urllib2.urlopen('http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_state_500k.zip')
zipcontent= response.read()
with open("cb_2015_us_state_500k.zip", 'w') as f:
    f.write(zipcontent)

zip_ref = zipfile.ZipFile("cb_2015_us_state_500k.zip", 'r')
zip_ref.extractall("data/us_states")
zip_ref.close()


## Read shapefile and transform to GeoJSON

# read the shapefile (urban areas)
reader = shapefile.Reader("data/us_cities/cb_2015_us_ua10_500k.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
places = open('places.csv', 'r')
for line in places:
    attr = line.split(";")
    city = attr[0]
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        if atr['NAME10'] == city:
            buffer.append(dict(type="Feature",
                           geometry=geom, properties=atr)) 
places.close()   

# write the GeoJSON file (urban areas)

geojson = open("data/us_cities/us_cities.json", "w")
geojson.write(dumps({"type": "FeatureCollection",
                     "features": buffer}, indent=2) + "\n")
geojson.close()

# read the shapefile (states)

reader = shapefile.Reader("data/us_states/cb_2015_us_state_500k.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    if atr['NAME'] == 'Texas':
        buffer.append(dict(type="Feature",
                           geometry=geom, properties=atr)) 
   
# write the GeoJSON file

geojson = open("data/us_states/us_states.json", "w")
geojson.write(dumps({"type": "FeatureCollection",
                     "features": buffer}, indent=2) + "\n")
geojson.close()