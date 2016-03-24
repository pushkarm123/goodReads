'''
Created on Mar 18, 2016

@author: pushkar
'''

import urllib2
from bs4 import BeautifulSoup
import csv
import time
import re


def getAmazonDetails(isbn):
    
    with open('csv_files/amazon_book_ratings.csv', 'w') as csvfile_ratings, open('csv_files/amazon_book_reviews.csv', 'w') as csvfile_reviews:
        ##Create file headers and writer
        ratings_fieldnames = ['book_isbn', 'avg_rating', 'five_rating', 'four_rating', 'three_rating', 'two_rating', 'one_rating' ]
        writer = csv.DictWriter(csvfile_ratings, delimiter=',', lineterminator='\n', fieldnames=ratings_fieldnames)
        writer.writeheader()
         
        reviews_fieldnames = ['book_isbn', 'review']            
        writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
        writer_book.writeheader()

        ##Get Overall details of the book    
        req = urllib2.Request('http://www.amazon.com/product-reviews/' + isbn + '?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=1', headers={ 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
    
        avgRatingTemp = soup.find_all('div',{'class':"a-row averageStarRatingNumerical"})[0].get_text()
        avgRating = re.findall('\d+\.\d+', avgRatingTemp)[0]
    
        fiveStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 5star histogram-review-count"})[0].get_text()
        fiveStarRating = fiveStarRatingTemp.strip('%')
    
        fourStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 4star histogram-review-count"})[0].get_text()
        fourStarRating = fourStarRatingTemp.strip('%')
    
        threeStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 3star histogram-review-count"})[0].get_text()
        threeStarRating = threeStarRatingTemp.strip('%')
    
        twoStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 2star histogram-review-count"})[0].get_text()
        twoStarRating = twoStarRatingTemp.strip('%')
        
        oneStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 1star histogram-review-count"})[0].get_text()
        oneStarRating = oneStarRatingTemp.strip('%')

        writer.writerow({'book_isbn': isbn, 'avg_rating': avgRating, 'five_rating': fiveStarRating, 
                         'four_rating': fourStarRating, 'three_rating': threeStarRating, 'two_rating': twoStarRating,
                         'one_rating': oneStarRating})
    
        ##Get top 20 helpful review of book
        for pagenumber in range(1,3):
            req = urllib2.Request('http://www.amazon.com/product-reviews/' + isbn + '?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber='+ str(pagenumber), headers={ 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')    
            for i in range(0,10):
                review = soup.find_all('div',{'class':"a-section review"})[i].contents[3].get_text().encode('UTF-8')
                writer_book.writerow({'book_isbn': isbn, 'review': review})
            
            
getAmazonDetails('0446576433')
