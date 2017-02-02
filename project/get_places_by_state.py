import pandas as pd
from get_city_id import * 

## The function gets a states lists as parameter and retrieves
## the placeID of the cities, using get_city_id function. Requires
## a csv file with US cities coordinates by state ordered by population.

def places_by_state(states, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    # Loops over states in states list
    for state in states:
        ## Reads the coordinates of the cities in the state
        # Reads the cities data in a panda DataFrame
        city_coord = pd.read_csv('data/coordinates.csv')
        xs = city_coord.loc[city_coord['State']==state].iloc[:11,3]
        ys = city_coord.loc[city_coord['State']==state].iloc[:11,4]
        # Loops over pairs of coordinates to get up to seven of the most
        # populated cities in the state contained in the cities file
        i=0
        while i < len(xs.index):
            if i < 7:
                x = xs.iloc[i,]
                y = ys.iloc[i,]
                #Calls get_city_id using the city's coordinates
                get_city_id(y,x, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
            i+=1