#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
from watson_developer_cloud import ToneAnalyzerV3
import sys

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='SgwSyRomsfn-o6-hO4OSwfwQDI5SiT_22cBcPjHemOBu',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

# RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

# def strip_emoji(text):
#     return RE_EMOJI.sub(r'', text)

#Variables that contains the user credentials to access Twitter API 
access_token = "2237159415-kEiwPGBZJWUsTYhmUdkUiS1hX0GiiwVEhPseC1F"
access_token_secret = "9J5ylgtPuhkSKKh10jGylS8CmSKsFZP5mLJcsbFBlw74k"
consumer_key = "nqXHh0t7oJpGbdeGhp2PGmP81"
consumer_secret = "bXcaZmYR1kqaWXNHLDKBBH6ngNkGkkAA3WhYTXJEaeRo8HMnmP"

tweetString = ""

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

	def __init__(self):
		super().__init__()
		self.counter=0
		self.limit=5

	def on_data(self, data):
		global tweetString
		tweet = json.loads(data).get('text')
		if ('RT @' in tweet):
			tweet = tweet.split(": ", 1)[1]

		tweetString += tweet
		self.counter += 1
		if (self.counter < self.limit):
			return True
		stream.disconnect()

	def on_error(self, status):
		print (status)


if __name__ == '__main__':
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
	if (len(sys.argv) > 1):
		stream.filter(track=[sys.argv[1]])
	else:
		stream.filter(track=['#maga'])


	tones = {}
	# for text in tweetList:
	tone_analysis = tone_analyzer.tone(
		{'text': tweetString},
		'application/json'
	).get_result()

	tweetSentences = json.loads(json.dumps(tone_analysis, indent=2)).get("sentences_tone")

	for sentence in tweetSentences:
		for tone in sentence.get("tones"):
			tone = tone.get("tone_id")
			tones[tone] = tones.get(tone, 0) + 1
	
	print(tones)