#My first attempt at making a reddit bot
#04-01-2021
#I'm well excited

#praw 
import praw as pw

#dotenv
from dotenv import load_dotenv
import os
load_dotenv()


reddit = pw.Reddit(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent"),
    username = os.getenv("username"),
    password = os.getenv("password"))


reddit.read_only = True
print('read_only: ',reddit.read_only)

learnP = reddit.subreddit('learnProgramming')
print(learnP.title)

