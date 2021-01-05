#My first attempt at making a reddit bot
#04-01-2021
#I'm well excited

#praw 
import praw as pw

#dotenv
from dotenv import load_dotenv
import os
load_dotenv()


#sub class of prasws Reddit class
class Bot(pw.Reddit):
    ''' A reddit bot class '''

    def __init__(self,
                 client_id,
                 client_secret,
                 user_agent,
                 username = None,
                 password = None
                 ):
        ''' this is the bots constructor '''
        super(Bot, self).__init__(
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent,
                username = username,
                password = password
                )

        print(self.user.me())
        self.read_only = True
        print('read_only: ',self.read_only)
        

        subreddit = self.subreddit('learnProgramming')

        for submit in subreddit.top(limit = 1):
            print('New post:\n')
            print(submit.title)
            print()


#initalsing instance of Reddit class
bot = Bot(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent"),
    username = os.getenv("redditUsername"),
    password = os.getenv("redditPassword"))

print(os.getenv("username"))
