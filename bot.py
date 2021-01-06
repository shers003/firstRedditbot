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

    #only enter lower case
    keyWords = ['london', 'g', 'fam', 'inabit', 'sn',
                'lewisham', 'safe', '420', 'wag1',
                'wagwan']
    
    def __init__(self,
                 client_id,
                 client_secret,
                 user_agent,
                 username = None,
                 password = None
                 ):
        ''' this is the bots constructor '''
        try:
            super(Bot, self).__init__(
                    client_id = client_id,
                    client_secret = client_secret,
                    user_agent = user_agent,
                    username = username,
                    password = password
                    )
        except:
            print('Failed to authenticate')
            print('/*************\\ \n')

        else:
            print('Signed in as:',self.user.me())
            print('read_only:',self.read_only)
            print('/*************\\ \n')
            
    
    def lookForKeyWords(self, name, numPost = 10, numCom = 10):
        ''' This method returns a list of
            comments that had the keyword '''

        print('\n\n\t\tSearching',name,'\n\n')
        
        subreddit = self.subreddit(name)

        for submit in subreddit.hot(limit = numPost):
            print('New post:\n')
            print('Title:',submit.title,'\n')
            
            comments = submit.comments
            matches = []
            commentRange = numCom

            
            for word in Bot.keyWords:
                for i in range(commentRange):
                    try:
                        if word in comments[i].body.lower():
                            print('Matched comment')
                            comment = comments[i]
                            info = [comment.id, comment.author, word]
                            matches.append(info)
                    
                    except IndexError as e:
                        print(e)
                        break
                                          
                         
        return matches

    def sendComments(matches):
        ''' will send a comment to the matches ''' 


#initalsing instance of Reddit class
bot = Bot(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent"),
    username = os.getenv("redditUsername"),
    password = os.getenv("redditPassword"))

matches = bot.lookForKeyWords('coding', numPost = 10, numCom = 20)
matches.append(bot.lookForKeyWords('learnProgramming', numPost = 10, numCom = 20))
matches.append(bot.lookForKeyWords('python', numPost = 10, numCom = 20))
matches.append(bot.lookForKeyWords('developer', numPost = 10, numCom = 20))

print('\n\nNumber of matches',str(len(matches)))

input('Enter to exit')
