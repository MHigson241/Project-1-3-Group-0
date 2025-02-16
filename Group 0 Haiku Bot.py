#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 14:25:44 2025

@authors: Maddy, Quincy, Kadir
"""

import praw
import syllapy
import re
import requests
import json

#discord webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1340337023432654958/mfKWYA4_xljoUAmiXELXRi14CXJZpuyf6ohn3msJArLjahNi96xrxuNfammRUqnaxFQG"


reddit = praw.Reddit (
    user_agent = True,
    client_id = "Ilolf9Y-L115BLwW6HES6g",
    client_secret = "tG4orvN7paw0WyD004NI4UhOac7MjA",
    )

username ='CPTHaikuBot'
password ='Project1-3Group0'

                   # Send to Discord
def send_to_discord(haiku):
        # Prepare the payload for the Discord webhook
        payload = {
            "content": haiku
        }
        

        # Send the POST request to the Discord webhook
        response = requests.post(WEBHOOK_URL, json=payload)

        # Check the response status
        if response.status_code == 204:
            print("Successfully posted message to Discord!")
        else:
            print(f"Failed to post message: {response.status_code}, {response.text}")

for submission in reddit.subreddit("maine").hot(limit = 100):
    text = submission.title
    
    #Init Dictionary
    syllableCounts = []
    
    #Strip non-alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    #Make list of words with syllable counts
    words = (text.split())
    totalCount = 0
    for word in words:
        totalCount += syllapy.count(word)
        syllables = syllapy.count(word)
        syllableCounts.append({word:syllables})

    #Line building function
    def buildLine(lineNum): 

        #Init variables
        line = "  >"
        lineCount = 0
        global syllableCounts

        #Assign syllable target
        if lineNum == 1 or lineNum == 3:
            syllTarget = 5
        elif lineNum == 2:
            syllTarget = 7
        
        #Main loop    
        while lineCount < syllTarget:
                    
            #Get Current word and syllable count, and add to line
            currentDict = syllableCounts.pop(0)
            for key, value in currentDict.items():
                line += key
                line += " "
                lineCount += value
                        
            #Check line for completion/error
            if lineCount == syllTarget:
                return line
                break
            elif lineCount > syllTarget:
                return "ERROR"


    #Check length
    if totalCount == 17:
        
        #Build lines
        line1 = buildLine(1)
        if line1 != "ERROR":
            line2 = buildLine(2)
            if line2 != "ERROR":
                line3 = buildLine(3)
                if line3 != "ERROR":

                    #Print final haiku
                    print("Haiku Detected")
                    print(line1)
                    print(line2)
                    print(line3)
                    print("")

                    #Joins line item/list into def of Haiku
                    haiku = [line1 , line2 , line3]

                    #Joins Haiku list ito a paragraph that has line item breaks
                    haiku_message = "\n".join(haiku)

                    #call the function to send the haiku
                    send_to_discord(haiku_message)
                    #to stop the program from re-running and finding same Haiku
                    