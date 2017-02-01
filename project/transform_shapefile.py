import zipfile, urllib2, shapefile, datetime
from json import dumps
from download_files import *


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
    placesfile = open("data/" + places, "r")
    for line in placesfile:
        attr = line.split(";")
        city_name = attr[0]
        city2 = city_name.split(", ")
        city = city2[0]
        state = city2[1]
        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            if city in atr['NAME10'] and state in atr['NAME10']:
                atr['NAME10'] = city_name               
                buffer.append(dict(type="Feature", 
                                   geometry=geom, properties=atr)) 
    placesfile.close()
    # Write the GeoJSON file
    geojson = open("data/" + foldername + "/us_cities.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", 
    "features": buffer}, indent=2) + "\n")
    
    geojson.close()

# States

def transformStates(statename):
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_state_500k.zip"
    foldername = "us_states"
    # call function to download shapefiles
    downloadData(url, foldername)
    # read the states shapefile
    reader = shapefile.Reader("data/" + foldername + "/cb_2015_us_state_500k.shp")
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        if atr['NAME'] == statename:
            buffer.append(dict(type="Feature", 
                               geometry=geom, properties=atr)) 
    # write the GeoJSON file
    geojson = open("data/" + foldername + "/us_states.json", "w")
    geojson.write(dumps({"type": "FeatureCollection",
    "features": buffer}, indent=2) + "\n")
    geojson.close()

