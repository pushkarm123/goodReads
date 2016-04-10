import mysql.connector
import traceback
import csv

conn = mysql.connector.connect(host= "localhost",
                  user="root",
                  passwd="Password11!!",
                  db="my_db")

cursor = conn.cursor()

try:
   	with open('/Users/pushkar/Documents/workspace/DataSet/Iteration_6/book_data.csv','rb') as csvfile:
   		reader = csv.reader(csvfile)
		next(reader, None)
		i=2
   		for row in reader:
   			user_id = row[0].decode("utf-8")
   			book_id = row[1].decode("utf-8")
   			isbn = row[3].decode("utf-8")
   			text_reviews_count = row[5].decode("utf-8")
   			title = row[6].decode("utf-8")
   			num_pages = row[9].decode("utf-8")
   			format = row[10].decode("utf-8")
   			publication_year = row[13].decode("utf-8")
   			avg_rating = row[15].decode("utf-8")
   			fiction = row[19].decode("utf-8")[:11]
   			fantasy = row[20].decode("utf-8")[:11]
   			classics = row[21].decode("utf-8")[:11]
   			young_adults = row[22].decode("utf-8")[:11]
   			romance = row[23].decode("utf-8")[:11]
   			non_fiction = row[24].decode("utf-8")[:11]
   			historical_fiction = row[25].decode("utf-8")[:11]
   			science_fiction = row[26].decode("utf-8")[:11]
   			dystopian = row[27].decode("utf-8")[:11]
   			horror = row[28].decode("utf-8")[:11]
   			paranormal = row[29].decode("utf-8")[:11]
   			contemporary = row[30].decode("utf-8")[:11]
   			childrens = row[31].decode("utf-8")[:11]
   			adult = row[32].decode("utf-8")[:11]
   			adventure = row[33].decode("utf-8")[:11]
   			mystery = row[34].decode("utf-8")[:11]
   			urban_fantasy = row[35].decode("utf-8")[:11]
   			history = row[36].decode("utf-8")[:11]
   			chick_lit = row[37].decode("utf-8")[:11]
   			thriller = row[38].decode("utf-8")[:11]
   			audio_book = row[39].decode("utf-8")[:11]
   			drama = row[40].decode("utf-8")[:11]
   			biography = row[41].decode("utf-8")[:11]
   			vampires = row[42].decode("utf-8")[:11]
   			plays = row[43].decode("utf-8")[:11]
   			philosophy = row[44].decode("utf-8")[:11]
   			crime = row[45].decode("utf-8")[:11]
   			poetry = row[46].decode("utf-8")[:11]
   			psychology = row[47].decode("utf-8")[:11]
   			mythology = row[48].decode("utf-8")[:11]
   			comics = row[49].decode("utf-8")[:11]

   			if(num_pages == ''):
   				num_pages = 0
   			if(publication_year == ''):
   				publication_year = 0

   			##Format and title not added

   			cursor.execute("insert into book_data (book_id, isbn, text_reviews_count, num_pages, format, publication_year, avg_rating, fiction, classics, young_adults, romance, non_fiction, historical_fiction, science_fiction, dystopian, horror, paranormal, contemporary, childrens, adult, adventure, mystery, urban_fantasy, history, chick_lit, thriller, audio_book, drama, biography, vampires, plays, philosophy, crime, poetry, psychology, mythology, comics) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (book_id, isbn, text_reviews_count, num_pages, format, publication_year, avg_rating, fiction, classics, young_adults, romance, non_fiction, historical_fiction, science_fiction, dystopian, horror, paranormal, contemporary, childrens, adult, adventure, mystery, urban_fantasy, history, chick_lit, thriller, audio_book, drama, biography, vampires, plays, philosophy, crime, poetry, psychology, mythology, comics))


   			cursor.execute("insert into user_book (user_id, book_id) values (%s, %s)", (user_id, book_id))


	conn.commit()
	cursor.close()
except Exception, e:
	traceback.print_exc()
	conn.rollback()

conn.close()