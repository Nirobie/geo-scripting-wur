import zipfile, urllib2, shapefile, datetime
from json import dumps
from download_files import *


## Functions to read cities and states shapefiles
## and transform features of interest to GeoJSON

## Function to transform cities urban areas polygons
## Requires the the csv file resulting from get_city_ids
## function, containing the cities' names.

def transformCities(places):
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_ua10_500k.zip"
    foldername = "us_cities"
    # Call function to download shapefiles
    downloadData(url, foldername)
    # Read the cities shapefile
    reader = shapefile.Reader("data/" + foldername + "/cb_2015_us_ua10_500k.shp")
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    # Declare list to store selected shapefile features    
    buffer = []
    # Read and loop over the csv file with cities names
    placesfile = open("data/" + places, "r")
    for line in placesfile:
        attr = line.split(";")
        city_name = attr[0]
        city2 = city_name.split(", ")
        # Store the city name in variable
        city = city2[0]
        # Store the state two letter code in variable
        state = city2[1]
        ## Loop over features in shapefile
        for sr in reader.shapeRecords():
            atr = dict(zip(field_names, sr.record))
            geom = sr.shape.__geo_interface__
            ## Include in 'buffer' list if the city name and state
            ## code are in the shapefile feature name, updating the
            ## city's name to csv file format.
            if city in atr['NAME10'] and state in atr['NAME10']:
                print 'Storing ' + city_name + ' in GeoJSON file'                
                atr['NAME10'] = city_name               
                buffer.append(dict(type="Feature", 
                                   geometry=geom, properties=atr)) 
    placesfile.close()
    
    ## Write a GeoJSON file with the 'buffer' list with selected features
    geojson = open("data/" + foldername + "/us_cities.json", "w")
    geojson.write(dumps({"type": "FeatureCollection", 
    "features": buffer}, indent=2) + "\n")
    geojson.close()

## Function for states with same structure, using list with states'
## names to evaluate the inclusion of the feature in file

def transformStates(statename):
    url = "http://www2.census.gov/geo/tiger/GENZ2015/shp/cb_2015_us_state_500k.zip"
    foldername = "us_states"
    ## Call function to download shapefiles
    downloadData(url, foldername)
    ## Read the states shapefile
    reader = shapefile.Reader("data/" + foldername + "/cb_2015_us_state_500k.shp")
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        if atr['NAME'] in statename:
            buffer.append(dict(type="Feature", 
                               geometry=geom, properties=atr)) 
    ## Write the GeoJSON file
    geojson = open("data/" + foldername + "/us_states.json", "w")
    geojson.write(dumps({"type": "FeatureCollection",
    "features": buffer}, indent=2) + "\n")
    geojson.close()

