import sys
import json
import re
from watson_developer_cloud import ToneAnalyzerV3
from prawcore import NotFound
import plotly
import plotly.graph_objs as go

redditList = []

tone_analyzer = ToneAnalyzerV3(
	version='2017-09-21',
	iam_apikey='SgwSyRomsfn-o6-hO4OSwfwQDI5SiT_22cBcPjHemOBu',
	url='https://gateway.watsonplatform.net/tone-analyzer/api'
)
class RedditParser(object):
    def __init__(self, sbreddit):
        self.sbreddit = sbreddit
    @classmethod
    def sub_exists(cls,sub):
        import praw
        reddit = praw.Reddit(client_id='AuC3ZsQDIwDKWQ',
                            client_secret='-jtdciDnmP_B_QrGiaqLD7F7L-Q',
                            user_agent='Emotion Analysis 1.0 for cuHacking2019')
        exists = True
        try:
            reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
            print(json.dumps({}))
        return exists
    def run(self):
        import praw
        global redditList
        POSTS = 3 #How many submissions in a subreddit to analyze
        #a_dict = {'subreddit' : {'name': str(self.sbreddit), 'submission': {'title': None, 'description': None, 'comments': []}}}
        if (RedditParser.sub_exists(self.sbreddit)):
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
            redditList = b_dict['subreddit']['text']
            b_dict['subreddit']['text'] = "\n".join(b_dict['subreddit']['text'])
            return b_dict
        else:
            return None

# If no arguments
if len(sys.argv) == 1:
    print (json.dumps({}))
    exit(1)
args = sys.argv[1]
runner = RedditParser(args)
longstr = runner.run()
if longstr:
    if longstr['subreddit']['text'][:30000]:
        tones = {}
        tone_analysis = tone_analyzer.tone(
            {'text': longstr['subreddit']['text'][:30000]},
            'application/json'
        ).get_result()

        redditSentences = json.loads(json.dumps(tone_analysis, indent=2)).get("sentences_tone")
        for sentence in redditSentences:
            for tone in sentence.get("tones"):
                tone = tone.get("tone_id")
                tones[tone] = tones.get(tone, 0) + 1
        data = [go.Bar(
		x=list(tones.keys()),
		y=list(tones.values())
        )]
        plotly.offline.plot(data, filename='public/reddit-graph.html', auto_open=False)
        #f = open("public/reddit-graph.html", "r")
        #html = f.read();
        #html = html.split("</body>")[0].split("<body>")[1]
        #html = html.replace("'", '"')

        returnDic = {}

        for i in range(len(redditList)):
            redditList[i] = redditList[i].replace("'", "KNIJOU(*HIBJNKHUY&T^FYGVHBGUYTR%")

  #      for i in range(len(redditList)):
   #         redditList[i] = redditList[i].replace('"', "JISDFOHD*S(HFINKJ@#(")

        # returnDic["html"] = html
        returnDic["tweetList"] = redditList
        print(json.dumps(returnDic))

        sys.stdout.flush()
    else:
        print (json.dumps({})) #no contents
        sys.stdout.flush()
