'''
Created on Apr 3, 2016

@author: pushkar
'''

import urllib2
import xml.etree.ElementTree as ET
import os
import traceback


def getval(root, element):
    try:
        ret = root.find(element).text
        if ret is None:
            return ""
        else:
            return ret.encode("utf8")
    except:
        return ""
    

def getLocation(address):
    try:
        url = 'https://maps.googleapis.com/maps/api/geocode/xml?&address=' + urllib2.quote(address)
        response = urllib2.urlopen(url)
        location_data_xml = response.read()
        
        f = open("xml_docs/location.xml", "w")
        try:
            f.write(location_data_xml)
        finally:
            f.close()
        
        root = ET.parse("xml_docs/location.xml").getroot()
        os.remove("xml_docs/location.xml")
        
        result_element = root.find('result')
        geometry_element = result_element.find('geometry')
        location_element = geometry_element.find('location')
        
        lat_text = getval(location_element,"lat")
        lng_text = getval(location_element,"lng")
        
        return lat_text, lng_text
    except Exception, e:
        traceback.print_exc()
        print "Exception! Address - " + address