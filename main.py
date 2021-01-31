import praw
import os
import config
import random

reddit = praw.Reddit(client_id = config.clientID,
                    client_secret = config.clientSecret,
                    username = config.redditID,
                    password = config.redditPassword,
                    user_agent = config.userAgent,)

subName = random.choice(["disneyvacation", "notdisneyvacation"])
print(subName)

for submission in reddit.subreddit(subName).new(limit=20):
    if not submission.stickied and not submission.is_self and not submission.saved and submission.score > 5:
        print(submission.title)
        print(submission.url)
        submission.save()
        posted = reddit.subreddit("disneydilemma").submit(submission.title, url=submission.url)
        print(posted.permalink)
        posted.reply("Crossposted from r/" + ">!" + subName + " " + submission.shortlink + "!<")
        break
    else:
        print("No Suitable Post Left")