import urllib2
from bs4 import BeautifulSoup
from textblob import TextBlob
import csv
import time
import re
import urllib2
import csv
import time
import sys
import xml.etree.ElementTree as ET
import os
import random
import traceback
#from GetLocation import getLocation
#from IPython.display import clear_output

def createUserDict(user_element):
    id = getval(user_element,'id')
    name = getval(user_element,'name')
    user_name = getval(user_element,'user_name')
    profile_url = getval(user_element,'link')
    image_url = getval(user_element,'image_url')
    about = getval(user_element,'about')
    age = getval(user_element,'age')
    gender = getval(user_element,'gender')
    location = getval(user_element,'location')
    lat_text, lng_text = getLocation(location)
    joined = getval(user_element,'joined')
    last_active = getval(user_element,'last_active')
    lat_text, lng_text = getLocation(location)
    userDict = dict ([('user_id', id), ('name', name) , ('user_name' , user_name),
    ('profile_url', profile_url), ('image_url', image_url),
    ('about', about), ('age', age), ('gender', gender), 
    ('location', location) , ('latitude', lat_text), ('longitude', lng_text), 
    ('joined', joined), ('last_active', last_active)])
    return userDict

def writeToCSV(writer, mydict):
    writer.writerow(mydict)

def getLocation(address):
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/xml?&address=' + urllib2.quote(address)
        response = urllib2.urlopen(url)
        location_data_xml = response.read()
        
        #f = open("xml_docs/location.xml", "w")
        #try:
        #    f.write(location_data_xml)
        #finally:
        #    f.close()
        
        root = ET.fromstring(location_data_xml) #parse("xml_docs/location.xml").getroot()
        #os.remove("xml_docs/location.xml")
        
        result_element = root.find('result')
        geometry_element = result_element.find('geometry')
        location_element = geometry_element.find('location')
        
        lat_text = getval(location_element,"lat")
        lng_text = getval(location_element,"lng")
        
        return lat_text, lng_text
    except Exception, e:
        traceback.print_exc()
        print "Exception! Address - " + address
        return '', ''

def getSentimentScore (text):
    blob = TextBlob(text)
    blob.tags           
    blob.noun_phrases
    try:
        blob.translate(to="en")
        print blob
    except:
        print"No translation needed for English text"
    sentimentScore = blob.sentiment.polarity
    return sentimentScore

def getAmazonDetails(isbn):
    with open('csv_files/amazon_book_ratings.csv', 'a') as csvfile_ratings, open('csv_files/amazon_book_reviews.csv', 'a') as csvfile_reviews:
        #Create writer for ratings file
        ratings_fieldnames = ['book_isbn', 'avg_rating', 'five_rating', 'four_rating', 'three_rating', 'two_rating', 'one_rating' ]
        writer_ratings = csv.DictWriter(csvfile_ratings, delimiter=',', lineterminator='\n', fieldnames=ratings_fieldnames)
        #writer.writeheader()
        
        ##Create writer for reviews file 
        reviews_fieldnames = ['book_isbn', 'amazonScore']            
        writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
        ##writer_book.writeheader()

        print 'http://www.amazon.com/product-reviews/' + isbn + '?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=1'

        ##Get Overall details of the book    
        req = urllib2.Request('http://www.amazon.com/product-reviews/' + isbn + '?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=1', headers={ 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
    
        avgRatingTemp = soup.find_all('div',{'class':"a-row averageStarRatingNumerical"})[0].get_text()
        avgRating = re.findall('\d+\.\d+', avgRatingTemp)[0]
    
        try:
            fiveStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 5star histogram-review-count"})[0].get_text()
            fiveStarRating = fiveStarRatingTemp.strip('%')
        except:
            fiveStarRating = 0

        try:
            fourStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 4star histogram-review-count"})[0].get_text()
            fourStarRating = fourStarRatingTemp.strip('%')
        except:
            fourStarRating = 0

        try:
            threeStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 3star histogram-review-count"})[0].get_text()
            threeStarRating = threeStarRatingTemp.strip('%')
        except:
            threeStarRating = 0

        try:
            twoStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 2star histogram-review-count"})[0].get_text()
            twoStarRating = twoStarRatingTemp.strip('%')
        except:
            twoStarRating = 0

        try:
            oneStarRatingTemp = soup.find_all('a',{'class':"a-size-small a-link-normal 1star histogram-review-count"})[0].get_text()
            oneStarRating = oneStarRatingTemp.strip('%')
        except:
            oneStarRating = 0

        writer_ratings.writerow({'book_isbn': isbn, 'avg_rating': avgRating, 'five_rating': fiveStarRating, 
                         'four_rating': fourStarRating, 'three_rating': threeStarRating, 'two_rating': twoStarRating,
                         'one_rating': oneStarRating})
    
        ##Get top 20 helpful review of book
        for pagenumber in range(1,3):
            req = urllib2.Request('http://www.amazon.com/product-reviews/' + isbn + '?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber='+ str(pagenumber), headers={ 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11' })
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')    
            for i in range(0,10):
                try:
                    review = soup.find_all('div',{'class':"a-section review"})[i].contents[3].get_text().encode('UTF-8')
                    print "Amazon review is: " + review
                    
                    amazonScore = getSentimentScore(review)
                    print "Sentiment score for the book is: " + str(amazonScore)

                    writer_book.writerow({'book_isbn': isbn, 'amazonScore': amazonScore})
                except:
                    print "No Reviews ISBN - " + isbn
                
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
    writer_ratings = csv.DictWriter(csvfile_ratings, delimiter=',', lineterminator='\n', fieldnames=ratings_fieldnames)
    writer_ratings.writeheader()
         
    reviews_fieldnames = ['book_isbn', 'amazonScore']            
    writer_book = csv.DictWriter(csvfile_reviews, delimiter=',', lineterminator='\n', fieldnames=reviews_fieldnames)
    writer_book.writeheader()


with open('csv_files/user_data.csv', 'w') as csvfile, open('csv_files/book_data.csv', 'w') as csvfile_book, open('csv_files/book_author.csv', 'w') as csvfile_author, open('csv_files/goodreads_user_reviews_ratings.csv', 'w') as gdrds_rr:
    fieldnames = ['user_id', 'name','user_name', 'profile_url','image_url', 'about', 'age', 'gender', 
                  'location', 'latitude', 'longitude', 'joined','last_active' ]
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
                        'published',
                        'fiction'   ,
                        'fantasy'   ,
                        'classics'  ,
                        'young_adult'   ,
                        'romance'   ,
                        'non_fiction'   ,
                        'historical_fiction'    ,
                        'science_fiction'   ,
                        'dystopian' ,
                        'horror'    ,
                        'paranormal'    ,
                        'contemporary'  ,
                        'childrens' ,
                        'adult' ,
                        'adventure' ,
                        'mystery'    ,
                        'urban_fantasy' ,
                        'history'   ,
                        'chick_lit' ,
                        'thriller'  ,
                        'audiobook' ,
                        'drama' ,
                        'biography' ,
                        'vampires' ,
                        'plays' ,
                        'philosophy' ,
                        'crime' ,
                        'poetry' ,
                        'psychology' ,
                        'mythology' ,
                        'comics'   ]
                
    writer_book = csv.DictWriter(csvfile_book, delimiter = ',', lineterminator = '\n', fieldnames=book_fieldnames)
    writer_book.writeheader()
    
    goodreads_ratings_fieldnames = ['user_id', 'b_id', 'rating', 'sentimentScore' ]
    rr_writer = csv.DictWriter(gdrds_rr, delimiter=',', lineterminator='\n', fieldnames=goodreads_ratings_fieldnames)
    rr_writer.writeheader()

    author_fieldnames = ['u_id', 'b_id', 'a_id', 'name', 'average_rating', 'ratings_count', 'text_reviews_count']
    writer_author = csv.DictWriter(csvfile_author, delimiter = ',', lineterminator = '\n', fieldnames = author_fieldnames)
    writer_author.writeheader()

    lst = []
    i = 0    
    while i < 12500:   
        try:  
            #time.sleep(1)
            #clear_output()
            c = random.randint(7500001, 8000000)
            #c = 2469697
            print "random number: " + str(c)    

            if (c not in lst):
                print "getting information for user id:"+ str(c)
                lst.append(c)
                url = 'https://www.goodreads.com/user/show/'+ str(c) +'.xml?key=i3Zsl7r13oHEQCjv1vXw'
                response = urllib2.urlopen(url)
                user_data_xml = response.read()
                
                #write xml to file
                #f = open("xml_docs/user"+ str(c) +".xml", "w")
                #try:
                #    f.write(user_data_xml)
                #finally:
                #    f.close()
            
                #root = ET.fromstring()

                root = ET.fromstring(user_data_xml) #parse("xml_docs/user"+ str(c) +".xml").getroot()
                #os.remove("xml_docs/user"+ str(c) +".xml")
                user_element = root.find('user')
                user_shelf_to_count = user_element.find('user_shelves')
                b_count = 0
                for user_shelf in user_shelf_to_count.findall('user_shelf'):
                    b_count = b_count + int(getval(user_shelf,'book_count'))
                
                print 'Book count is ' + str(b_count)
                if(b_count > 10):


                    print 'Collecting data for user ' + str(c)           
                    '''id = getval(user_element,'id')
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
                    '''

                    userDict = createUserDict(user_element)    

                    id = userDict['user_id']
                    #writer.writerow({'id': id, 'name' : name,'user_name' : user_name,
                    #                  'profile_url' : profile_url,'image_url' : image_url,
                    #                 'about' : about, 'age': age, 'gender' : gender, 
                    #                 'location' : location, 'joined' : joined, 'last_active': last_active})
                    
                    writeToCSV(writer,userDict)

                    print "Saved user data for user id:" + str(c)
 
                    # get list of user shelves
                    user_shelves_root =  user_element.find('user_shelves')
                    user_shelf_list = []
                    for user_shelf in user_shelves_root.findall("user_shelf"):
                        shelf = getval(user_shelf,"name")
                        #Books on Shelf
                        print "Checking for books in shelf: " + shelf + " for user id:" + str(c)
                         
                        shelf_url = "https://www.goodreads.com/review/list/"+ str(c) +".xml?key=i3Zsl7r13oHEQCjv1vXw&v=2&per_page=200&shelf=" + shelf
                        #time.sleep(1)
                        print shelf_url
                        response = urllib2.urlopen(shelf_url)
                        shelf_data_xml = response.read()
                        # write xml to file
                        #f = open("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml", "w")
                        #try:
                        #    f.write(shelf_data_xml)
                        #finally:
                        #    f.close()
                         
                        shelf_root = ET.fromstring(shelf_data_xml) #parse("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml").getroot()
                         
                        #os.remove("xml_docs/user_shelf_" + shelf + "_"+ str(c) + ".xml")
                        try:
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
                                    
                                    #Get Amazon book details
                                    #getAmazonDetails(isbn)
 
 
                                    print "Fetched review data from Amazon for book :" + title
 
                                    #get number of books on each type of shelf
                                    book_url = 'https://www.goodreads.com/book/show/'+str(b_id)+'.xml?key=i3Zsl7r13oHEQCjv1vXw'
                                    response = urllib2.urlopen(book_url)
                                    book_data_xml = response.read()
                                    # write xml to file
                                    #f = open("xml_docs/book_data_" + str(b_id) + ".xml", "w")
                                    #try:
                                    #    f.write(book_data_xml)
                                    #finally:
                                    #    f.close()
                             
                                    book_root = ET.fromstring(book_data_xml) #parse("xml_docs/book_data_" + str(b_id) + ".xml").getroot()
                                    #os.remove("xml_docs/book_data_" + str(b_id) + ".xml")
                                    print "checking count in shelf for book_id:" + str(b_id) 
                                    book_root = book_root.find("book")
                                    book_shelves = book_root.find("popular_shelves")
                                     
                                    fiction = 0
                                    fantasy = 0
                                    classics = 0
                                    young_adult = 0
                                    romance = 0
                                    non_fiction = 0
                                    historical_fiction = 0
                                    science_fiction = 0
                                    dystopian = 0
                                    horror = 0
                                    paranormal = 0
                                    contemporary = 0
                                    childrens = 0
                                    adult = 0
                                    adventure = 0
                                    mystery = 0
                                    urban_fantasy = 0
                                    history = 0
                                    chick_lit = 0
                                    thriller = 0
                                    audiobook = 0
                                    drama = 0
                                    biography = 0
                                    vampires = 0
                                    plays = 0
                                    philosophy = 0
                                    crime = 0
                                    poetry = 0
                                    psychology = 0
                                    mythology = 0
                                    comics = 0
                                    cnt = 0.0
                                     
                                    for shelf_type in book_shelves.findall("shelf"):
                                        attributes = shelf_type.attrib
                                        name = attributes['name']
                                        count = float(attributes['count'])
                                        #print name + ":" + count
                                         
                                        if ( name == 'fiction'):
                                            fiction = count
                                            cnt = cnt + count
                                        if ( name == 'fantasy'):
                                            fantasy = count
                                            cnt = cnt + count
                                        if ( name == 'classics' or name == 'classic'):
                                            classics = count
                                            cnt = cnt + count
                                        if ( name == 'young-adult'):
                                            young_adult = count
                                            cnt = cnt + count
                                        if ( name == 'romance' or name == 'romantic'):
                                            romance = count
                                            cnt = cnt + count
                                        if ( name == 'non-fiction' or name == 'nonfiction'):
                                            non_fiction = count
                                            cnt = cnt + count
                                        if ( name == 'historical-fiction'):
                                            historical_fiction = count
                                            cnt = cnt + count
                                        if ( name == 'science-fiction' or name == 'sci-fi fantasy' or name == 'scifi' or name == 'fantasy-sci-fi' or name == 'sci-fi'):
                                            science_fiction = count
                                            cnt = cnt + count
                                        if ( name == 'dystopian' or name == 'dystopia'):
                                            dystopian = count
                                            cnt = cnt + count
                                        if ( name == 'horror'):
                                            horror = count
                                            cnt = cnt + count
                                        if ( name == 'paranormal' or name == 'ghost'):
                                            paranormal = count
                                            cnt = cnt + count
                                        if ( name == 'contemporary' or name == 'contemporary-fiction'):
                                            contemporary = count
                                            cnt = cnt + count
                                        if ( name == 'childrens' or name == 'children' or name == 'kids' or name =='children-s-books'):
                                            childrens = count
                                            cnt = cnt + count
                                        if ( name == 'adult'):
                                            adult = count
                                            cnt = cnt + count
                                        if ( name == 'adventure'):
                                            adventure = count
                                            cnt = cnt + count
                                        if ( name == 'mystery'):
                                            mystery = count
                                            cnt = cnt + count
                                        if ( name == 'urban-fantasy'):
                                            urban_fantasy = count
                                            cnt = cnt + count
                                        if ( name == 'history' or name == 'historical'):
                                            history = count
                                            cnt = cnt + count
                                        if ( name == 'chick-lit'):
                                            chick_lit = count
                                            cnt = cnt + count
                                        if ( name == 'thriller'):
                                            thriller = count
                                            cnt = cnt + count
                                        if ( name == 'audiobook' or name == "audio"):
                                            audiobook = count
                                            cnt = cnt + count
                                        if ( name == 'drama' or name == 'dramatic'):
                                            drama = count
                                            cnt = cnt + count
                                        if ( name == 'biography' or name == 'memoirs'):
                                            biography = count
                                            cnt = cnt + count
                                        if ( name == 'vampires' or name == 'vampire'):
                                            vampires = count
                                            cnt = cnt + count
                                        if ( name == 'plays' or name == 'play' or name == 'theater' or name == 'theatrical'):
                                            plays = count
                                            cnt = cnt + count
                                        if ( name == 'philosophy' or name == 'philosophical'):
                                            philosophy = count
                                            cnt = cnt + count
                                        if ( name == 'crime' or name == 'criminal'):
                                            crime = count
                                            cnt = cnt + count
                                        if ( name == 'poetry'or name == 'poem' or name == 'poems'):
                                            poetry = count
                                            cnt = cnt + count
                                        if ( name == 'psychology'or name == 'psychological'):
                                            psychology = count
                                            cnt = cnt + count
                                        if ( name == 'mythology' or name == 'mythological'):
                                            mythology = count
                                            cnt = cnt + count
                                        if ( name == 'comics' or name == 'comic'):
                                            comics = count
                                            cnt = cnt + count
 
                                    fiction = fiction/cnt
                                    fantasy = fantasy/cnt
                                    classics = classics/cnt
                                    young_adult = young_adult/cnt
                                    romance = romance/cnt
                                    non_fiction = non_fiction/cnt
                                    historical_fiction = historical_fiction/cnt
                                    science_fiction = science_fiction/cnt
                                    dystopian = dystopian/cnt
                                    horror = horror/cnt
                                    paranormal = paranormal/cnt
                                    contemporary = contemporary/cnt
                                    childrens = childrens/cnt
                                    adult = adult/cnt
                                    adventure = adventure/cnt
                                    mystery = mystery/cnt
                                    urban_fantasy = urban_fantasy/cnt
                                    history = history/cnt
                                    chick_lit = chick_lit/cnt
                                    thriller = thriller/cnt
                                    audiobook = audiobook/cnt
                                    drama = drama/cnt
                                    biography = biography/cnt
                                    vampires = vampires/cnt
                                    plays = plays/cnt
                                    philosophy = philosophy/cnt
                                    crime = crime/cnt
                                    poetry = poetry/cnt
                                    psychology = psychology/cnt
                                    mythology = mythology/cnt
                                    comics = comics/cnt
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
                                        'description' : description, 
                                         
                                        'fiction' : fiction , 
                                        'fantasy' : fantasy ,
                                        'classics' : classics   ,
                                        'young_adult' : young_adult ,
                                        'romance' : romance ,
                                        'non_fiction' : non_fiction ,
                                        'historical_fiction' : historical_fiction   ,
                                        'science_fiction' : science_fiction ,
                                        'dystopian' : dystopian ,
                                        'horror' : horror   ,
                                        'paranormal' : paranormal   ,
                                        'contemporary' : contemporary   ,
                                        'childrens' : childrens ,
                                        'adult' : adult ,
                                        'adventure' : adventure ,
                                        'mystery' : mystery   ,
                                        'urban_fantasy' : urban_fantasy ,
                                        'history' : history ,
                                        'chick_lit' : chick_lit ,
                                        'thriller' : thriller   ,
                                        'audiobook' : audiobook ,
                                        'drama' : drama ,
                                        'biography' : biography ,
                                        'vampires' : vampires ,
                                        'plays' : plays ,
                                        'philosophy' : philosophy ,
                                        'crime' : crime ,
                                        'poetry' : poetry ,
                                        'psychology' : psychology , 
                                        'mythology' : mythology ,
                                        'comics' : comics   })
 
 
                                    #bookDict = createBookDict(book)    
 
                                    print "Data written on csv for book:" + title
 
                                    print "Getting reviews details from user: " + str(id) + " and book_id: " + str(b_id)
                                    review_url = "https://www.goodreads.com/review/show_by_user_and_book.xml?book_id=" +str(b_id)+ "&key=i3Zsl7r13oHEQCjv1vXw&user_id=" + str(id)
                                    review_response = urllib2.urlopen(review_url)
                                    review_response_xml = review_response.read()
                                    review_root = ET.fromstring(review_response_xml)
                                    user_rr = review_root.find("review")
                                     
                                    user_r_rating = getval(user_rr, "rating")
                                    print "Got user review rating: " + user_r_rating
 
                                    user_r_review = getval(user_rr, "body")
                                    user_r_review = user_r_review.replace('\n', '')
                                    print "User review is: " + user_r_review
 
                                    score = getSentimentScore(user_r_review)
                                    print "Sentiment score is " + str(score)
 
                                    rr_writer.writerow({
                                        'user_id': id,
                                        'b_id' : b_id ,
                                        'rating' : user_r_rating,
                                        'sentimentScore' : score })
 
 
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
                        except Exception, e:
                            traceback.print_exc()
#                         
                    i = i + 1
        except:
            #time.sleep(1)
            print "Exception!!"
            traceback.print_exc()
    print "End of Program"