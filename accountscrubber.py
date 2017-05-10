#!/usr/bin/python
# -*- coding: utf-8 -*-
#Please ensure that your system's encoding is also set to UTF-8!!!
#Install Praw using "pip install praw"
import praw
import time
import sys
import os
import random
import string

#==============================
#========CONFIGURATION=========
#==============================
#Your login info
YOURACCOUNT = "username"
YOURPASSWORD = "password"
#Generate or retrieve this info at https://www.reddit.com/prefs/apps/
CLIENTID = "clientidkey"
CLIENTSECRET = "clientsecretkey"

#POST HANDLING
#Store comments and submissions in a text file so you can review them later
ARCHIVE_COMMENTS = 1
ARCHIVE_SUBMISSIONS = 0
#Scramble the body of your comments and submissions to prevent Reddit from keeping a copy in their archive
SCRAMBLE_COMMENTS = 1
SCRAMBLE_SUBMISSIONS = 0
#Delete comments and submissions
DELETE_COMMENTS = 1
DELETE_SUBMISSIONS = 0

#TIMING
#Control the amount of comments you want to manage in any given cycle.
COMMENTSPERCYCLE = 10
SUBMISSIONSPERCYCLE = 10
#The amount of time to take between actions in seconds. Don't go below 30, or this bot may get banned.
TIMEBETWEENACTIONS = 30

#VARIABLES
if not os.path.isfile("comment_archive.txt"):
    comment_archive = []
else:
    with open("comment_archive.txt", "r") as file:
        comment_archive = file.read()
        comment_archive = comment_archive.split("\n")
        comment_archive = list(filter(None, comment_archive))
        comment_archive = list(set(comment_archive))

if not os.path.isfile("submission_archive.txt"):
    submission_archive = []
else:
    with open("submission_archive.txt", "r") as file:
        submission_archive = file.read()
        submission_archive = submission_archive.split("\n")
        submission_archive = list(filter(None, submission_archive))
        submission_archive = list(set(submission_archive))

#FUNCTIONS
def randomword(length):
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 !@#$%^&*()_-+=<>,./?{}[];':") for i in range(length))

#account config
reddit = praw.Reddit(client_id=CLIENTID,
                     client_secret=CLIENTSECRET,
                     password=YOURPASSWORD,
                     user_agent='AccountScrubber 0.5 (by /u/semperverus)',
                     username=YOURACCOUNT)

                     
while True:
    for comment in reddit.redditor(YOURACCOUNT).comments.controversial('all', limit=COMMENTSPERCYCLE):
        if ARCHIVE_COMMENTS == 1:
            try:
                msg = "[id:" + comment.id + "][Score: " + str(comment.score) + "] - " + comment.body
                msg = msg.rstrip()
                print(msg)
                comment_archive.append(msg)
            except Exception as e:
                print("[\u001B[91mfail\u001B[0m][id:\u001B[97m" + comment.id + "\u001B[0m] " + str(e))
        if SCRAMBLE_COMMENTS == 1:
            comment.edit(randomword(10000))
            print("[id:" + comment.id + "] Comment scrambled")
            time.sleep(TIMEBETWEENACTIONS)
        if DELETE_COMMENTS == 1:
            comment.delete()
            print("[id:" + comment.id + "] Comment deleted")
            time.sleep(TIMEBETWEENACTIONS)
            
    with open("comment_archive.txt", "w") as file:
                    for entry in comment_archive:
                        file.write(entry + "\n")
                        
    for submission in reddit.redditor(YOURACCOUNT).submissions.controversial('all', limit=SUBMISSIONSPERCYCLE):
        if ARCHIVE_SUBMISSIONS == 1:
            if submission.is_self:
                try:
                    msg = "[id:" + comment.id + "][Score: " + str(submission.score) + "] [Title: " + submission.title + "] - " + submission.body
                    print(msg)
                except Exception as e:
                    print("[\u001B[91mfail\u001B[0m][id:\u001B[97m" + submission.id + "\u001B[0m] " + str(e))
            else:
                try:
                    msg = "[id:" + comment.id + "][Score: " + str(submission.score) + "] [Title: " + submission.title + "] - " + submission.url
                    print(msg)
                except Exception as e:
                    print("[\u001B[91mfail\u001B[0m][id:\u001B[97m" + submission.id + "\u001B[0m] " + str(e))
        if SCRAMBLE_SUBMISSIONS == 1:
            if submission.is_self:
                #submission.edit(randomword(10000))
                #time.sleep(TIMEBETWEENACTIONS)
                print("[id:" + comment.id + "] Submission scrambled")
        if DELETE_SUBMISSIONS == 1:
                #submission.delete()
                #time.sleep(TIMEBETWEENACTIONS)
                print("[id:" + comment.id + "] Submission deleted")
                
    with open("submission_archive.txt", "w") as file:
                    for entry in submission_archive:
                        file.write(entry + "\n")
