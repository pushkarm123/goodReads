import urllib2
import csv
import time
import sys
import xml.etree.ElementTree as ET
import os
import random
from AmazonCrawler import getAmazonDetails

def getval(root, element):
    try:
        ret = root.find(element).text
        if ret is None:
            return ""
        else:
            return ret.encode("utf8")
    except:
        return ""
    

with open('csv_files/amazon_book_ratings.csv', 'w') as csvfile_ratings, open('csv_files/amazon_book_reviews.csv', 'w') as csvfile_reviews:
    ##Create file headers and writer
    ratings_fieldnames = ['book_isbn', 'avg_rating', 'five_rating', 'four_rating', 'three_rating', 'two_rating', 'one_rating' ]
    writer = csv.DictWriter(csvfile_ratings, delimiter=',', lineterminator='\n', fieldnames=ratings_fieldnames)
    writer.writeheader()
         
    reviews_fieldnames = ['book_isbn', 'review']            
    writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
    writer_book.writeheader()

with open('csv_files/user_data.csv', 'w') as csvfile, open('csv_files/book_data.csv', 'w') as csvfile_book, open('csv_files/book_author.csv', 'w') as csvfile_author:
    fieldnames = ['id', 'name','user_name', 'profile_url','image_url', 'about', 'age', 'gender', 
                  'location','joined','last_active' ]
    writer = csv.DictWriter(csvfile, delimiter = ',', lineterminator = '\n', fieldnames=fieldnames)
    writer.writeheader()
    book_fieldnames = [
                        'user_id',
                        'b_id',
                        'shelf',
                        'isbn', 
                        'isbn13',
                        'text_reviews_count',
                        'title',
                        'image_url',
                        'link',
                        'num_pages',
                        'b_format',
                        'publisher',
                        'publication_day', 
                        'publication_year', 
                        'publication_month',
                        'average_rating', 
                        'ratings_count', 
                        'description', 
                        'published'  ]
                
    writer_book = csv.DictWriter(csvfile_book, delimiter = ',', lineterminator = '\n', fieldnames=book_fieldnames)
    writer_book.writeheader()
    author_fieldnames = [
                        'u_id',
                        'b_id',
                        'a_id',
                        'name',
                        'average_rating',
                        'ratings_count',
                        'text_reviews_count']
    writer_author = csv.DictWriter(csvfile_author, delimiter = ',', lineterminator = '\n', fieldnames = author_fieldnames)
    writer_author.writeheader()

    lst = []
    i = 0
    
    while i < 10:   
        try:     
            
            time.sleep(1)
            c = random.randint(1, 1000000)
            print "random number: " + str(c)    

            if (c not in lst):
                print "getting information for user id:"+ str(c)
                lst.append(c)
                url = 'https://www.goodreads.com/user/show/'+ str(c) +'.xml?key=i3Zsl7r13oHEQCjv1vXw'
                response = urllib2.urlopen(url)
                user_data_xml = response.read()
                #write xml to file
                i = i + 1
                f = open("xml_docs/user"+ str(c) +".xml", "w")
                try:
                    f.write(user_data_xml)
                finally:
                    f.close()
            
                #root = ET.fromstring()
                root = ET.parse("xml_docs/user"+ str(c) +".xml").getroot()
                os.remove("xml_docs/user"+ str(c) +".xml")
                user_element = root.find('user')
                id = getval(user_element,'id')
                name = getval(user_element,'name')
                user_name = getval(user_element,'user_name')
                profile_url = getval(user_element,'link')
                image_url = getval(user_element,'image_url')
                about = getval(user_element,'about')
                age = getval(user_element,'age')
                gender = getval(user_element,'gender')
                location = getval(user_element,'location')
                joined = getval(user_element,'joined')
                last_active = getval(user_element,'last_active')
                writer.writerow({'id': id, 'name' : name,'user_name' : user_name,
                                  'profile_url' : profile_url,'image_url' : image_url,
                                 'about' : about, 'age': age, 'gender' : gender, 
                                 'location' : location, 'joined' : joined, 'last_active': last_active})
                print "Saved user data for user id:" + str(c)
            
            
                # get list of user shelves
            
                user_shelves_root =  user_element.find('user_shelves')
            
                user_shelf_list = []
            
                for user_shelf in user_shelves_root.findall("user_shelf"):
                    shelf = getval(user_shelf,"name")
                    #Books on Shelf
                    print "Checking for books in shelf: " + shelf + " for user id:" + str(c)
                    
                    shelf_url = "https://www.goodreads.com/review/list/"+ str(c) +".xml?key=i3Zsl7r13oHEQCjv1vXw&v=2&shelf=" + shelf
                    time.sleep(1)
                    print shelf_url
                    response = urllib2.urlopen(shelf_url)
                    shelf_data_xml = response.read()
                    # write xml to file
                    f = open("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml", "w")
                    try:
                        f.write(shelf_data_xml)
                    finally:
                        f.close()
                    
                    shelf_root = ET.parse("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml").getroot()
                    
                    os.remove("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml")
                    reviews = shelf_root.find("reviews")
                    for review in reviews.findall("review"):
                        for book in review.findall("book"):
                            b_id = getval(book,"id")
                            isbn = getval(book,"isbn")
                            print "Fetching data for book with isbn:" + str(isbn) + " and id:" + str(id)
                            isbn13 = getval(book,"isbn13")
                            text_reviews_count = getval(book,"text_reviews_count")
                            title = getval(book,"title")
                            image_url = getval(book,"image_url")
                            link = getval(book,"link")
                            num_pages = getval(book,"num_pages")
                            b_format = getval(book,"format")
                            publisher = getval(book,"publisher")
                            publication_day = getval(book,"publication_day")
                            publication_year = getval(book, "publication_year") 
                            publication_month = getval(book,"publication_month")
                            average_rating = getval(book,"average_rating")
                            ratings_count = getval(book,"rating_count")
                            description = getval(book,"description")
                            published = getval(book,"published")
                            getAmazonDetails(isbn)
                            print "Fetched review data from Amazon for book :" + title
                            writer_book.writerow({
                                'user_id': id,
                                'b_id' : b_id ,
                                'shelf' : shelf,
                                'isbn' : isbn, 
                                'isbn13': isbn13,
                                'text_reviews_count' : text_reviews_count,
                                'title' : title,
                                'image_url' : image_url,
                                'link' : link,
                                'num_pages' : num_pages,
                                'b_format' : b_format,
                                'publisher' : publisher,
                                'publication_day' : publication_day, 
                                'publication_year' : publication_year, 
                                'publication_month' : publication_month,
                                'average_rating' : average_rating, 
                                'ratings_count' : ratings_count, 
                                'description' : description })

                            print "Data written on csv for book:" + title

                            authors = book.find("authors")
                            for author in authors.findall("author"):
                                a_id = getval(author,"id")
                                name = getval(author,"name")
                                average_rating = getval(author,"average_rating")
                                ratings_count = getval(author,"ratings_count")
                                text_reviews_count = getval(author,"text_reviews_count")
                                writer_author.writerow({'u_id': id,
                                                        'b_id' : b_id,
                                                        'a_id' : a_id,
                                                        'name' : name,
                                                        'average_rating' : average_rating,
                                                        'ratings_count' : ratings_count,
                                                        'text_reviews_count' : text_reviews_count})
        except:
            time.sleep(1)
            print "Exception!!"
    print "End of Program"