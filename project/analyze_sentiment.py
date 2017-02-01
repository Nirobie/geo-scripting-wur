from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import pandas as pd

###sentiment function gets the cities file with the Twitter placeIDs
###and returns a dictionary with pandas DataFrames with daily results

def sentiment(cities, time):
    time = time
    #Define a list of queries that have the file names
    ## Parameter?
    q_list = ["@realDonaldTrump", "@HillaryClinton"]    
    
    ##Get a list of placeids of the cities to analyse
    citieslist = []    
    places = open("data/" + cities, 'r')
    for line in places:
        attr = line.split(";")
        citieslist.append(attr[1])
    places.close()
    ##Opens every file with tweets and runs into it
    analyzer = SentimentIntensityAnalyzer()
    #Defines a pandas DataFrame to store the results by city   
    #df = pd.DataFrame({'date': []})
    #i=0
    #Defines a dictionary to store the DataFrame for each city    
    city_results = {}
    for placeid in citieslist:
        df = pd.DataFrame({'date': []})
        i=0
        for query in q_list:
            with open('data/'+placeid+query+time+'.csv', 'r') as infile:
                reader = csv.DictReader(infile, delimiter=';')
                for tweet in reader:
                    vs = analyzer.polarity_scores(tweet['text'])
                    df.loc[i, query] = vs['compound']
                    df.loc[i, 'date'] = tweet['date']
                    i+=1
            infile.close()
        df = df.set_index(pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M'))
        df = df.drop(['date'], axis=1)
        city_results[placeid] = df.resample('D').sum()
    return city_results