#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re

RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

def strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

#Variables that contains the user credentials to access Twitter API 
access_token = "2237159415-kEiwPGBZJWUsTYhmUdkUiS1hX0GiiwVEhPseC1F"
access_token_secret = "9J5ylgtPuhkSKKh10jGylS8CmSKsFZP5mLJcsbFBlw74k"
consumer_key = "nqXHh0t7oJpGbdeGhp2PGmP81"
consumer_secret = "bXcaZmYR1kqaWXNHLDKBBH6ngNkGkkAA3WhYTXJEaeRo8HMnmP"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data).get('text')
        if ('RT ' in tweet):
        	tweet = tweet.split(": ", 1)[1]

       	print()
        print(tweet)
        print("-----------")
        print(strip_emoji(tweet))
        print()
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#maga'])