'''
Created on Mar 27, 2016

@author: Meera
'''

from textblob import TextBlob
import csv
import re
#open('Amazon_Reviews_Test.csv') as csvfile,
with  open('csv_files/Amazon_Reviews_Sentiment.csv', 'w') as csvfile_reviews:
    reviews_fieldnames = ['book_isbn', 'review','sentimentScore']            
    writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
    writer_book.writeheader()

with open('amazon_book_reviews.csv','rb') as csvfile, open('csv_files/Amazon_Reviews_Sentiment.csv', 'a') as csvfile_reviews:
    reader = csv.reader(csvfile)
    
    for row in reader:
        try:
            #print(row['book_isbn'], row['review'])
            text = row[1].decode("utf-8")
            #text = re.sub("[^A-Za-z]*", " ", text)
            isbn = row[0]

            blob = TextBlob(text)
            #print blob
            blob.tags           
            blob.noun_phrases
        
            try:
                blob.translate(to="en")
                print blob
            except:
                print"No translation needed for English text"
            
            sentimentScore = blob.sentiment.polarity
            print(blob.sentiment.polarity)
        
            reviews_fieldnames = ['book_isbn', 'review','sentimentScore']            
            writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
            #writer_book.writeheader()
            writer_book.writerow({'book_isbn': isbn, 'review': text.encode("utf-8"), 'sentimentScore':sentimentScore})
        except:
            print "Exception!!"