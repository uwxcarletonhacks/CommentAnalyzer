from tweepy import OAuthHandler
from tweepy import API
import json
import re
from watson_developer_cloud import ToneAnalyzerV3
import sys
import plotly
import plotly.graph_objs as go

TWEET_COUNT = 100
PAGE_COUNT = 3

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='SgwSyRomsfn-o6-hO4OSwfwQDI5SiT_22cBcPjHemOBu',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

#Variables that contains the user credentials to access Twitter API
access_token = "2237159415-kEiwPGBZJWUsTYhmUdkUiS1hX0GiiwVEhPseC1F"
access_token_secret = "9J5ylgtPuhkSKKh10jGylS8CmSKsFZP5mLJcsbFBlw74k"
consumer_key = "nqXHh0t7oJpGbdeGhp2PGmP81"
consumer_secret = "bXcaZmYR1kqaWXNHLDKBBH6ngNkGkkAA3WhYTXJEaeRo8HMnmP"

tweetString = ""
tweetList = []
tones = {}

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

if (len(sys.argv) > 1):
	search = "#" + sys.argv[1]
else:
	search = "#python"

idList = []
search_results = api.search(q=search, count=TWEET_COUNT, result_type='recent', lang="en")
for j in range (PAGE_COUNT):
	for i in range(len(search_results)):
		idValue = json.loads(json.dumps(search_results[i]._json)).get('id')
		tweet = json.loads(json.dumps(search_results[i]._json)).get('text')
		if ('RT @' in tweet):
			tweet = tweet.split(": ", 1)[1]

		tweet = tweet.replace("'", "KNIJOU(*HIBJNKHUY&T^FYGVHBGUYTR%")
		if (idValue not in idList):
			idList.append(idValue)
			tweetList.append(tweet)
			tweetString += tweet
	idList.sort()
	if (len(idList) > 0 and j < 2):
		search_results = api.search(q=search, max_id=idList[1]-1, count=TWEET_COUNT, result_type='recent', lang="en")

# # for text in tweetList:
if (len(search_results) > 0):
	tone_analysis = tone_analyzer.tone(
		{'text': tweetString},
		'application/json'
	).get_result()

	tweetSentences = json.loads(json.dumps(tone_analysis, indent=2)).get("sentences_tone")

	for sentence in tweetSentences:
		for tone in sentence.get("tones"):
			tone = tone.get("tone_id")
			tones[tone] = tones.get(tone, 0) + 1

	data = [go.Bar(
			x=list(tones.keys()),
			y=list(tones.values())
	)]

	plotly.offline.plot(data, filename='public/twitter-graph.html', auto_open=False)

	# f = open("public/twitter-graph.html", "r")
	# html = f.read();
	# html = html.split("</body>")[0].split("<body>")[1]
	# html = html.replace("'", '"')

	returnDic = {}

	# returnDic["html"] = html;
	returnDic["tweetList"] = tweetList
	print(json.dumps(returnDic))
	sys.stdout.flush()
else:
	print(json.dumps({}))
	sys.stdout.flush()

	# Removed html from bottom
# idList = []
# search_results = api.search(q=search, count=TWEET_COUNT, result_type='recent', lang="en")

# TWEET_COUNT = 100
# PAGE_COUNT = 3

# for j in range (PAGE_COUNT):
# 	for i in range(len(search_results)): NO
# 		idValue = json.loads(json.dumps(search_results[i]._json)).get('id')
# 		tweet = json.loads(json.dumps(search_results[i]._json)).get('text') NO
# 		if ('RT @' in tweet): NO
# 			tweet = tweet.split(": ", 1)[1] NO

# 		tweet = tweet.replace("'", "^G*M)FE#C%B&!X$BKN") NO
# 		if (idValue not in idList):
# 			idList.append(idValue)
# 			tweetList.append(tweet)
# 			tweetString += tweet
# 	idList.sort()
# 	if (len(idList) > 0 and j < 2):
# 		search_results = api.search(q=search, max_id=idList[1]-1, count=TWEET_COUNT, result_type='recent', lang="en")