class RedditParser(object):
    def __init__(self, sbreddit):
        self.sbreddit = sbreddit
    def run(self):
        import praw
        import pprint
        import json
        a_dict = {'subreddit' : {'name': str(self.sbreddit), 'submission': {'title': None, 'description': None, 'comments': []}}}
        #b_dict = {'subreddit' : {'name': str(self.sbreddit), 'text': []}}
        reddit = praw.Reddit(client_id='AuC3ZsQDIwDKWQ',
                            client_secret='-jtdciDnmP_B_QrGiaqLD7F7L-Q',
                            user_agent='Emotion Analysis 1.0 for cuHacking2019')
        for submission in reddit.subreddit(self.sbreddit).hot(limit = 1):
            submission.comments.replace_more(limit = 0)
            #b_dict['subreddit']['text'].append(submission.title)
            #b_dict['subreddit']['text'].append(submission.description)
            a_dict['subreddit']['submission']['title'] = submission.title
            a_dict['subreddit']['submission']['description'] = submission.description
            for allcomment in submission.comments.list():
                a_dict['subreddit']['submission']['comments'].append(allcomment.body)
                #b_dict['subreddit']['text'].append(allcomment.body)
        #" ".join(b_dict['subreddit']['text'])
        jform = json.dumps(a_dict)
        return jform

if __name__ == "__main__":
    import sys
    # If no arguments
    if len(sys.argv) == 1:
        exit(1)
    args = sys.argv[1]
    runner = RedditParser(args)
    runner.run()