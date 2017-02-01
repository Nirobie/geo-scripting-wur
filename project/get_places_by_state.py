import pandas as pd
from get_city_id import * 

def places_by_state(state):
    city_coord = pd.read_csv('data/coordinates.csv')
    xs = city_coord.loc[city_coord['State']==state].iloc[:11,3]
    ys = city_coord.loc[city_coord['State']==state].iloc[:11,4]
    
    i=0
    while i < len(xs.index):
        if i < 10:
            x = xs.iloc[i,]
            y = ys.iloc[i,]
            #Call the get places function with x and y
            get_city_id(y,x)
        i+=1