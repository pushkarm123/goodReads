'''
Created on Mar 18, 2016

@author: pushkar
'''


from bs4 import BeautifulSoup
import urllib2


req = urllib2.Request('http://www.amazon.com//product-reviews/1455536342/?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber=2', headers={ 'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11', 'Cache-Control':'max-age=0' })
html = urllib2.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')
count = BeautifulSoup(soup.findAll("div", { "class" : "a-section review"}),'html.parser')
print soup.findAll("div", { "class" : "a-section review"})