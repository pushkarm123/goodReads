'''
Created on Mar 28, 2016

@author: pushkar
'''
import csv
import os
from textblob import TextBlob

with open('csv_files/amazon_book_reviews.csv', 'rb') as f:
    reader = csv.reader(f)
    next(reader, None)
    i = 0
    for row in reader:
        text = row[1].decode("UTF-8")
        blob = TextBlob(text)
        try:
            blob.translate(to="en")
        except:
            print "No translation needed"
        blob.tags           
        blob.noun_phrases
            #blob.translate(to="en")
            #print blob
        print blob
        sentimentScore = blob.sentiment.polarity
        print(blob.sentiment.polarity)
        