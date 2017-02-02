# -*- coding: utf-8 -*-

import got,datetime,codecs

def tweets(filename, query, since, until, time):
    
    def receiveBuffer(tweets):
        for t in tweets:
            outputFile.write(('\n%s;%s;%s;"%s";%s' % (tweetCriteria.placeid, t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.text, t.permalink)))
            outputFile.flush();
            print 'More than %d saved on file...\n' % len(tweets)    
        
    places = open("data/" + filename, 'r')
    for line in places:
        attr = line.split(";")
        placeid = attr[1]
        tweetCriteria = got.manager.TweetCriteria()
    
        tweetCriteria.placeid = placeid
        tweetCriteria.querySearch = query
        tweetCriteria.since = since
        tweetCriteria.until = until
    
        tweetname = placeid + query + time + ".csv"
        
        try:
            with open("data/" + tweetname) as file:
                print "File " + tweetname + " already exists"
                file.close()
        except:
            outputFile = codecs.open("data/" + tweetname, "w+", "utf-8")
            outputFile.write('place;username;date;text;permalink')
            got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
            outputFile.close()
            print 'Done. Output file %s generated.' % (tweetname)
    places.close()