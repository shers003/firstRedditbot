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
    @property
    def keyWords(self):
        file = open('keyWords.txt', 'r')
        keywords = []
        word = ''
        count = 0
        while True:
            count += 1
            word = file.readline()
            word = word.strip('\n')
            if word == '':
                break
            else:
                keywords.append(word)
        file.close()
        
        return keywords
    
    @keyWords.setter
    def new_keyWord(self, word):
        file = open('keyWords.txt', 'a')
        file.write(word+'\n')
        file.close()

    @property
    def replied_to(self):
        ''' Property returns list of comments ids '''
        file = open('replied_to.txt', 'r')
        replied_to = []
        name = ' '
        count = 0
        while True:
            count += 1
            name = file.readline()
            name = name.strip('\n')
            if name == '':
                break
            else:    
                replied_to.append(name)
                
        file.close()

        return replied_to
    
    @replied_to.setter
    def new_replied_to(self, newId):
        file = open('replied_to.txt', 'a')
        file.write(newId+'\n')
        file.close()

    @property
    def my_comment_ids(self):
        ''' Property returns list of comments ids '''
        
        file = open('my_comment_ids.txt', 'r')
        replied_to = []
        name = ' '
        count = 0
        while True:
            count += 1
            name = file.readline()
            name = name.strip('\n')
            if name == '':
                break
            else:    
                replied_to.append(name)
                
        file.close()

        return replied_to
    
    @replied_to.setter
    def new_my_comment_id(self, newId):
        file = open('my_comment_ids.txt', 'a')
        file.write(newId+'\n')
        file.close()
                       
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
        
        try:
            subreddit.id
        except:
            print('Invalid subreddit')
            return []
        
        for submit in subreddit.hot(limit = numPost):
            print('New post:\n')
            print('Title:',submit.title,'\n')
            
            comments = submit.comments
            matches = []
            keywords = self.keyWords
                        
            for word in keywords:
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

        for match in matches:
            try:
                comId = match[0]
                comAuthor = str(match[1])
                matchedWord = str(match[2])
            except IndexError:
                print('Was an index error with: ',end='')
                print(match)
                continue
            except Exception as e:
                print(e,':',match)
                continue
            
            if comId in self.replied_to:
                print('already replied to',comId)
                continue
            
            elif matchedWord == '420':
                reply = '420 nice'
                
            elif matchedWord == '69':
                reply = '69 nice'
                
            else:
                
                reply = 'Yo ' + comAuthor + ' I noticed you said ' + matchedWord
                reply += '. I know the chances are slim but if by any chance'
                reply += ' you\'re from London, I just want to take this opertunity to say:'
                reply += ' hope you have a great day, much love my g!!'
                reply += '\n\nThis is a bot btw'
                
            #added this try to combat rate error
            try:
                self.new_replied_to = comId
                comment = self.comment(comId)
                comment.reply(reply)
                comment.upvote()
                self.new_my_comment_id = comment.id
                
                print('replied to user:',comAuthor,comId)

            except:
                print('Error occured with comment:',comId)
                
    def listenForReplise(self):
       
            for comId in self.my_comment_ids:
                comment = self.comment(comId)
                print(len(comment.replies))
                
                if len(comment.replies) != 0:
                    if comment.replies[0].id in self.my_comment_ids:
                        reply = 'I am just a freindly reddit bot'
                        comment.replies[0].reply(reply)
                        print('Replied to:',comId)
                    else:
                        print('Already replied to:',comId)

                else:
                    print('no reply for:',comId)

def main(bot):
    print('\t\tWelcome to my reddit bot\n\n')
    userInput = None
    while userInput != '0':
        print('''\nHere are your options:
0.Exit
1.Scan a subreddit and comment
2.Check for replies
3.See keywords
4.Add keyword
''')
        userInput = input('Enter choice: ')
        
        if userInput == '1':

            sub = input('Which reddit: ')
            matches = bot.lookForKeyWords(sub)

                
            print('\n\nNumber of matches',str(len(matches)))
            for match in matches:
                print(match)
            bot.sendComments(matches)
            
        elif userInput == '2':
            bot.listenForReplise()

        elif userInput == '3':
            for word in bot.keyWords:
                print(word,end=' ')
            
        elif userInput == '4':
            keyword = input('Enter new word: ')
            bot.new_keyWord = keyword
            print('Keyword added')
            
        elif userInput == '0':
            print('Bye')
            
#initalsing instance of Reddit class
bot = Bot(
    client_id = os.getenv("client_id"),
    client_secret = os.getenv("client_secret"),
    user_agent = os.getenv("user_agent"),
    username = os.getenv("redditUsername"),
    password = os.getenv("redditPassword"))

main(bot)

input('Enter to exit')
