import Exporter
from get_places_by_state import *
from transform_shapefile import *
from analyze_sentiment import *
from map_results import *

## Twitter API codes
APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

## States of interest
states = ['Texas','California']

if __name__ == '__main__':
    
    
    # Get the list of placeIDs of cities in Texas and California
    places_by_state(states, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    # Scrape tweets in the cities in Texas and California that contain @HillaryClinton and
    # @realDonaldTrump, before and after US presidential election
    Exporter.tweets("places.csv", "@HillaryClinton", "2016-10-31", "2016-11-07", "before")
    Exporter.tweets("places.csv", "@realDonaldTrump", "2016-10-31", "2016-11-07", "before")
    Exporter.tweets("places.csv", "@realDonaldTrump", "2016-11-08", "2016-11-15", "after")
    Exporter.tweets("places.csv", "@HillaryClinton", "2016-11-08", "2016-11-15", "after")
    
    # Analize sentiment of tweets
    sent_before = sentiment('places.csv', 'before')
    sent_after = sentiment('places.csv', 'after')
    
    # Create before and after election visualizations of tweet sentiment in
    # Texas and California
    create_map(sent_before, 'places.csv', states, 'before')
    create_map(sent_after, 'places.csv', states, 'after')
    
    
