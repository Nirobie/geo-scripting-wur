from twython import Twython

from get_city_id import *
import Exporter
from transform_shapefile import *
from analyze_sentiment import *
from map_results import *


if __name__ == '__main__':
    #get_city_id(29.8384948, -95.4708095532)
    #get_city_id(29.4770355, -98.6710862865)
    #get_city_id(32.8198585, -96.7301749064)
    #get_city_id(30.3233457, -97.716309926)
    #Exporter.tweets("places.csv", "@HillaryClinton", "2016-10-31", "2016-11-07", "before")
    #Exporter.tweets("places.csv", "@realDonaldTrump", "2016-10-31", "2016-11-07", "before")
    #Exporter.tweets("places.csv", "@realDonaldTrump", "2016-11-08", "2016-11-15", "after")
    #Exporter.tweets("places.csv", "@HillaryClinton", "2016-11-08", "2016-11-15", "after")
    
    sent_before = sentiment('places.csv', 'before')
    sent_after = sentiment('places.csv', 'after')
    
    create_map(sent_before, 'places.csv', 'Texas', 'before')
    create_map(sent_after, 'places.csv', 'Texas', 'after')
    

