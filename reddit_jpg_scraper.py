import praw  #reddit api wrapper
import requests       
import os
import shutil
import json 

number_of_posts=int(input("enter the number of photos you want"))

try:
    os.chdir(os.getcwd()+"\\Downloaded_Pictures")
except:
    os.mkdir(os.getcwd()+"\\Downloaded_Pictures")
    print("Downloaded_Pictures||file Created!")
    os.chdir(os.getcwd()+"\\Downloaded_Pictures")

try:
    with open("reddit_credentials.json") as f:
        creds = json.load(f)
        print(creds)
except:
    print("First time setup!")
    cerds={"client_id":input("Enter client_id"),"client_secret":input("Enter client_secret")}
    with open("reddit_credentials.json","w")as f:
        json.dump(cerds,f)
    with open("reddit_credentials.json") as f:
        creds = json.load(f)

uclient_id = creds.get("client_id")
uclient_secret = creds.get("client_secret")

print("logging in")
reddit = praw.Reddit(
    client_id = uclient_id,       
    client_secret = uclient_secret,
    user_agent = "bot 0.1",
)
print("done")

try:
    os.mkdir(os.getcwd()+"\\png")
except:
    pass
try:
    os.mkdir(os.getcwd()+"\\jpg")
except:
    pass
print(os.listdir())
subs =['meme','dankmeme'] #add any ammount 
i = 0
for sub in subs:
    for submission in reddit.subreddit(sub).hot(limit = number_of_posts ): 
        try:
            url = submission.url
            response = requests.get(url)
            ext = url[-3:]
            print(ext)
            supported_types = ["png","jpg"]
            if ext in supported_types:
                i += 1 
                file_name= "{}.{}.{}".format(i,str(submission.id),ext)
                if file_name not in os.listdir(os.getcwd()+"\\{}".format(ext)): 
                    with open(file_name.lower().strip(" "),"wb")as f:
                        f.write(response.content)
                    with open("titles_with_numbers.txt","a")as f:
                        f.write(str(i) + submission.title+" ID = "+submission.id+"\n")
                    shutil.move(file_name,os.getcwd()+"\\{}".format(ext))
        except:
            pass
os.chdir(ogpath)
