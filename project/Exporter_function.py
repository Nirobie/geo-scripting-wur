# -*- coding: utf-8 -*-

import got,datetime,codecs

def tweets(placeid, query, since = "2017-01-30", until = "2017-01-31", maxtweets = 1):
	tweetCriteria = got.manager.TweetCriteria()
	
	tweetCriteria.placeid = placeid
	tweetCriteria.querySearch = query
	tweetCriteria.maxTweets = int(maxtweets)
	tweetCriteria.since = since
	tweetCriteria.until = until
	
	filename = placeid + query + ".csv"
	outputFile = codecs.open("data/" + filename, "w+", "utf-8")
		
	outputFile.write('place;username;date;text;permalink')

	def receiveBuffer(tweets):
		for t in tweets:
			outputFile.write(('\n%s;%s;%s;"%s";%s' % (tweetCriteria.placeid, t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.text, t.permalink)))
		outputFile.flush();
		print 'More than %d saved on file...\n' % len(tweets)

	got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	outputFile.close()
	print 'Done. Output file generated.'