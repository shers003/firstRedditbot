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
                'wagwan', 'catford', 'ladywell',
                'brockley', 'croften', '69', 'bruv',
                'brudda']
    
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
                        
            for word in Bot.keyWords:
                for i in range(numCom):
                    try:
                        if word in comments[i].body.lower():
                            comment = comments[i]
                            info = [comment.id, comment.author, word]
                            matches.append(info)
                            print('Matched comment')
                        else:
                            print('Comment not matched')
                            
                    except IndexError as e:
                        print(e)
                        break
                                          
                         
        return matches

    def sendComments(self, matches):
        ''' will send a comment to the matches '''

        #make this a file that gets read chapter 7
        replied_to = []

        for match in matches:
            comId = match[0]
            comAuthor = str(match[1])
            matchedWord = str(match[2])

            if comId in replied_to:
                continue
            
            elif matchedWord == '420':
                reply = '420 nice'
                
            elif matchedWord == '69':
                reply = '69 nice'
                
            else:    
                reply = 'Yo ' + comAuthor + ' I noticed you said ' + matchedWord
                reply += '. I know the chances are slim but if by any chance'
                reply += ' you\'re from SE London, I just want to take this opertunity to say:'
                reply += ' hope you have a great day, much love my g!!'
                reply += '\n\nThis is a bot btw'

            comment = self.comment(comId)
            comment.reply(reply)
            comment.upvote()
            replied_to.append(comId)
         
#initalsing instance of Reddit class
bot = Bot(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent"),
    username = os.getenv("redditUsername"),
    password = os.getenv("redditPassword"))

matches = bot.lookForKeyWords('coding', numPost = 5, numCom = 10)
#matches.append(bot.lookForKeyWords('learnProgramming', numPost = 10, numCom = 20))
#matches.append(bot.lookForKeyWords('python', numPost = 10, numCom = 20))
#matches.append(bot.lookForKeyWords('developer', numPost = 10, numCom = 20))

print('\n\nNumber of matches',str(len(matches)))
for match in matches:
    print(match)

bot.sendComments(matches)

input('Enter to exit')
