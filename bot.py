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
    
    ####### Bot Properties ####### 
    ##############################
    
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
		
    @property
    def commentTxt(self):
        file = open('commentTxt.txt', 'r')
        txt = file.read()
        file.close()
        return txt
     
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

    ## Bot Properties setters #### 
    ##############################
    
    @commentTxt.setter
    def commentTxt(self, txt):
        file = open('commentTxt.txt', 'w')
        txt = file.write(txt)
        file.close()
            
    @keyWords.setter
    def new_keyWord(self, word):
        if word == None:
            return 'Not valid'
        elif word == '':
            return 'Not valid'
        else:
            file = open('keyWords.txt', 'a')
            file.write(word+'\n')
            file.close()
            
    @replied_to.setter
    def new_replied_to(self, newId):
        if newId == None:
            return 'Not valid'
        elif newId == '':
            return 'Not valid'
        else:
            file = open('replied_to.txt', 'a')
            file.write(newId+'\n')
            file.close()
    
    @replied_to.setter
    def new_my_comment_id(self, newId):
        if newId == None:
            return 'Not valid'
        elif newId == '':
            return 'Not valid'
        else:
            file = open('my_comment_ids.txt', 'a')
            file.write(newId+'\n')
            file.close()

    ####### Bot Methods ########## 
    ##############################
                       
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
            return matches

        matches = []
        keywords = self.keyWords
        
        for submit in subreddit.hot(limit = numPost):
            print('New post:\n')
            print('Title:',submit.title,'\n')
            
            comments = submit.comments
                                    
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
                            
            else:
                reply = self.commentTxt
                
            #added this try to combat rate error
            try:  
                comment = self.comment(comId)
                self.new_replied_to = comId
                comment.reply(reply)
                comment.upvote()
                self.new_my_comment_id = comment.id
                
                print('replied to user:',comAuthor,comId)

            except Exception as e:
                print('Error occured with comment:',comId,'\n',e)
                
    def replyToReplies(self, rep):
       
            for comId in self.my_comment_ids:
                comment = self.comment(comId)
                print(len(comment.replies))
                
                if len(comment.replies) != 0:
                    if comment.replies[0].id in self.my_comment_ids:
                        reply = rep
                        comment.replies[0].reply(reply)
                        print('Replied to:',comId)
                    else:
                        print('Already replied to:',comId)

                else:
                    print('no reply for:',comId)

def main(bot):
    ''' Main code for console '''
    print('\t\tWelcome to my reddit bot\n\n')
    userInput = None
    while userInput != '0':
        print('''\nHere are your options:
0.Exit
1.Scan a subreddit and comment
2.Check for replies
3.See keywords
4.Add keyword
5.view comment
6.change comment
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
            msg = input('Enter a Reply for the replies')
            if msg == None:
                msg = 'I am just a freindly reddit bot'
            bot.replyToReplies(msg)

        elif userInput == '3':
            for word in bot.keyWords:
                print(word,end=' ')
            
        elif userInput == '4':
            keyword = input('Enter new word: ')
            bot.new_keyWord = keyword
            print('Keyword added')

        elif userInput == '5':
            print(bot.commentTxt)
            
        elif userInput == '6':
            newTxt = input('Enter new comment: ')
            if newTxt != '':
                bot.commentTxt = newTxt
                print('Commented changed to:',newTxt)
            
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

##############################################
############# GUI CODE #######################
##############################################
'''
from tkinter import *

class App(Frame):

    def __init__(self, master, bot):
        
        super(App, self).__init__(master)
        self.bot = bot
        self.grid()
        self.setupGui()

    def setupGui(self):
        
        #Title    
        Label(self, text = os.getenv("redditUsername")
              ).grid(row = 0, column = 1, sticky = W)
        #see comment text button
        Button(self,
                text = 'See Comment',
                command = self.getComment
               ).grid(row = 1, column = 0, sticky = W)

        #set comment text button
        Button(self,
                text = 'Set Comment',
                command = self.setComment
               ).grid(row = 2, column = 0, sticky = W)

        #Comment text box
        self.commentEntry = Text(self,
                              width = 40,
                              height = 5,
                              wrap = WORD)
        self.commentEntry.grid(row = 1, column = 1, columnspan = 3, sticky = W)

        #see keywords text button
        Button(self,
               text = 'See Keywords',
               command = self.getKeywords
               ).grid(row = 3, column = 0, sticky = W)

        #Add keywords button
        Button(self,
               text = 'Add Keywords',
               command = self.AddKeywords
               ).grid(row = 4, column = 0, sticky = W)

        #Keywords textbox
        self.keyWordEntry = Text(self,
                              width = 40,
                              height = 5,
                              wrap = WORD)
        self.keyWordEntry.grid(row = 3, column = 1, columnspan = 3, sticky = W)

        self.addKeywordEntry = Entry(self,)
        self.addKeywordEntry.grid(row = 4, column = 1, sticky = W)
  
    def getComment(self):
        txt = self.bot.commentTxt
        
        self.commentEntry.delete(0.0, END)
        self.commentEntry.insert(0.0, txt)

    def setComment(self):
        newTxt = self.commentEntry.get(0.0, END)
        self.bot.commentTxt = newTxt
        
        self.commentEntry.delete(0.0, END)

    def getKeywords(self):
        self.keyWordEntry.delete(0.0, END)
        
        keywords = self.bot.keyWords
        for word in keywords:
            self.keyWordEntry.insert(END, word)
            self.keyWordEntry.insert(END, ' ')
            

    def AddKeywords(self):
        self.keyWordEntry.delete(0.0, END)
        word = self.addKeywordEntry.get()
        self.bot.new_keyWord = word
        
root = Tk()
root.title('Reddit Bot')

app = App(root, bot)

root.mainloop()
'''
