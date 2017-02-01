import zipfile, urllib2, shapefile, datetime
from json import dumps
import json
from download_files import *
from Sentiment_function import *

result = sentiment("places.csv", "before")

## Read shapefile and transform to GeoJSON

# Cities

def transformCities(places):
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_ua10_500k.zip"
    foldername = "us_cities"
    # call function to download shapefiles
    downloadData(url, foldername)
    # read the cities shapfile
    reader = shapefile.Reader("data/" + foldername + "/cb_2015_us_ua10_500k.shp")
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    placesfile = open(places, "r")
    for line in placesfile:
        attr = line.split(";")
        city = attr[0]
        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            if atr['NAME10'] == city:
                buffer.append(dict(type="Feature", 
                                   geometry=geom, properties=atr)) 
    placesfile.close()
    # Write the GeoJSON file
    geojson = open("data/" + foldername + "/us_cities.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", 
    "features": buffer}, indent=2) + "\n")
    geojson.close()
    
def add_color(places, json_file, result):
    placesfile = open(places, "r")
    with open(json_file) as cities:
        json_decoded = json.load(cities)
    for feature in json_decoded['features']:
        for line in placesfile:
            attr = line.split(";")
            if attr[0] == feature['properties']['NAME10']:
                city_id = attr[1]
                if sum(result[city_id]['@realDonaldTrump']) > sum(result[city_id]['@HillaryClinton']):
                    feature['properties']['FCOLOR'] = 'red'
                else:
                    feature['properties']['FCOLOR'] = 'blue'
                with open(json_file, 'w') as cities2:
                    json.dump(json_decoded, cities2,sort_keys=True,
                              indent=4, separators=(',', ': '))
    placesfile.close()