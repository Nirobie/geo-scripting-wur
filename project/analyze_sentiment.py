from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import pandas as pd

### Sentiment function gets the cities file with the Twitter placeIDs
### and returns a dictionary with pandas DataFrames with daily results
### and the cities' placeIDs as keys. 

def sentiment(cities, time):
    
    # Define a list of queries that have the file names
    q_list = ["@realDonaldTrump", "@HillaryClinton"]    
    
    ## From the cities csv file, gets a list of placeids
    ## of the cities to analyse.
    citieslist = []    
    places = open("data/" + cities, 'r')
    for line in places:
        attr = line.split(";")
        citieslist.append(attr[1])
    places.close()
    
    # Inicialize the sentiment intensity analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Defines a dictionary to store the DataFrame for each city    
    city_results = {}    
    
    ## Loops over the placeID list to analize every tweet file
    for placeid in citieslist:
    # Defines a pandas DataFrame to store the results by city
        df = pd.DataFrame({'date': []})
        i=0
        ## Loops over tweets' files for each city
        for query in q_list:
            with open('data/'+placeid+query+time+'.csv', 'r') as infile:
                reader = csv.DictReader(infile, delimiter=';')
                ## Loops over tweets for each tweets' file
                for tweet in reader:
                    # Perform the sentiment analysis of the tweet text
                    vs = analyzer.polarity_scores(tweet['text'])
                    # Store the sentiment result and tweet date in DataFrame
                    df.loc[i, query] = vs['compound']
                    df.loc[i, 'date'] = tweet['date']
                    i+=1
            infile.close()
        # Makes the date column a date time index for the DataFrame
        df = df.set_index(pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M'))
        df = df.drop(['date'], axis=1)
        # Store the results in dictionary city_results under placeID key
        print 'Saving ' + placeid + ' results'
        city_results[placeid] = df.resample('D').sum()
    return city_results