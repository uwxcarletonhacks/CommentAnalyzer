import sys
import json
import re
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='SgwSyRomsfn-o6-hO4OSwfwQDI5SiT_22cBcPjHemOBu',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)
class RedditParser(object):
    def __init__(self, sbreddit):
        self.sbreddit = sbreddit
    def run(self):
        import praw
        import pprint
        import json
        POSTS = 3 #How many submissions in a subreddit to analyze
        #a_dict = {'subreddit' : {'name': str(self.sbreddit), 'submission': {'title': None, 'description': None, 'comments': []}}}
        b_dict = {'subreddit' : {'name': str(self.sbreddit), 'text': []}}
        reddit = praw.Reddit(client_id='AuC3ZsQDIwDKWQ',
                            client_secret='-jtdciDnmP_B_QrGiaqLD7F7L-Q',
                            user_agent='Emotion Analysis 1.0 for cuHacking2019')
        for submission in reddit.subreddit(self.sbreddit).hot(limit = POSTS):
            submission.comments.replace_more(limit = 0)
            b_dict['subreddit']['text'].append(submission.title)
            #a_dict['subreddit']['submission']['title'] = submission.title
            #a_dict['subreddit']['submission']['description'] = submission.description
            for allcomment in submission.comments.list():
                #a_dict['subreddit']['submission']['comments'].append(allcomment.body)
                b_dict['subreddit']['text'].append(allcomment.body)
        b_dict['subreddit']['text'] = "\n".join(b_dict['subreddit']['text'])
        print (b_dict['subreddit']['text'])
        return b_dict


# If no arguments
if len(sys.argv) == 1:
    exit(1)
args = sys.argv[1]
runner = RedditParser(args)
longstr = runner.run()

tones = {}
tone_analysis = tone_analyzer.tone(
	{'text': longstr['subreddit']['text']},
	'application/json'
).get_result()

tweetSentences = json.loads(json.dumps(tone_analysis, indent=2)).get("sentences_tone")
for sentence in tweetSentences:
	for tone in sentence.get("tones"):
		tone = tone.get("tone_id")
		tones[tone] = tones.get(tone, 0) + 1
print(tones)
sys.stdout.flush()