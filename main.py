import praw
import os
import config
import random
from datetime import datetime
import time

#Config
reddit = praw.Reddit(client_id = config.clientID,
                    client_secret = config.clientSecret,
                    username = config.redditID,
                    password = config.redditPassword,
                    user_agent = config.userAgent,)

#Posts the submisson
def postSubmisson():

    #Picks DisneyVacation or NotDisneyVacation sub
    subName = random.choice(["DisneyVacation", "NotDisneyVacation"])
    print(subName)

    #Searches the new for a suitable post
    for submission in reddit.subreddit(subName).new(limit=50):
        if not submission.stickied and not submission.is_self and not submission.saved and submission.score > 5:
            print(submission.title)
            print(submission.url)
            submission.save()
            #Adds nsfw tag if needed
            if submission.over_18 :
                posted = reddit.subreddit("disneydilemma").submit(submission.title, url=submission.url, nsfw=True)
            else :
                posted = reddit.subreddit("disneydilemma").submit(submission.title, url=submission.url)
            print(posted.permalink)
            #Comments the real subreddit and the link
            posted.reply("Crossposted from r/" + ">!" + subName + " " + submission.shortlink + "!<")
            break
        else:
            print("No Suitable Post Left")

#Runs the code every 15 minutes
while True:
    print("Update data:", datetime.now())
    sleep = 15 - datetime.now().minute % 15
    if sleep == 15:
        postSubmisson()
        time.sleep(sleep * 60)
    else:
        time.sleep(sleep * 60)