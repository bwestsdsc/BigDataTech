#!/usr/bin/python

import sys
import time
import csv
import multiprocessing
from itertools import *
import urllib.request
from urllib.parse import urlparse
import re
      

def main(argv):
    
    incidents_list = []
   
    sorted_crime_file = open('sorted_output_tiny.csv', 'r')
    sorted_fields = csv.reader(sorted_crime_file, delimiter=',', quotechar='"')
    mpp = multiprocessing.Pool(4)
    
    for chunk in grouper(1, sorted_fields):
        results = mpp.map(processChunk, chunk)
        
def grouper(n, iterable, padvalue=None):
    
    if iterable != '':
        return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def processChunk(chunk):

    update_chunk  = []
    for line in chunk[1:5]:
        getLongLat(chunk[5], chunk[6])

        #json parsing step goes here
        #update_chunk.append(lat)
        #update_chunk.append(long)
        
    return chunk

def getLongLat(str_address, city):
    
    data = {}
    data['address'] = str_address + ', '  + city
    #restful webservice call here send the address and get the longitude and latitiude
    url_values = urllib.parse.urlencode(data)
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    full_url = url + '?' + url_values
    response = urllib.request.urlopen(full_url)
    decode_response = ((response.read().decode('utf-8')))
    
    pprint.pprint(decode_response)


if __name__ == "__main__":
     main(sys.argv[1:])

