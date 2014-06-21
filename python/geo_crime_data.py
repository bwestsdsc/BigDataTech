#!/usr/bin/python

import sys
import time
import csv
import multiprocessing
from itertools import *
import urllib.request
from urllib.parse import urlparse
      

def main(argv):
    
    incidents_list = []
   
    sorted_crime_file = open('sorted_output.csv', 'r')
    sorted_fields = csv.reader(sorted_crime_file, delimiter=',', quotechar='"')
    mpp = multiprocessing.Pool(4)
    
    for chunk in grouper(100000, sorted_fields):
        results = mpp.map(processChunk, chunk)
        #for r in results:
            #print(r[5] + ', ' + r[6]) 
    
def grouper(n, iterable, padvalue=None):
    
    if iterable != '':
        return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def processChunk(chunk):

    update_chunk  = []
    for line in chunk:
        print(chunk[5] + ' - ' + chunk[6])
       # getLongLat(chunk[5], chunk[6])
        #chunk[5] + chunk[6])
        #json parsing step goes here
        #update_chunk.append(lat)
        #update_chunk.append(long)
        
    return chunk

def getLongLat(str_address, city):
    
    data = {}
    data['address'] = str_address + ', '  + city
    url_values = urllib.parse.urlencode(data)
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    full_url = url + '?' + url_values
    response = urllib.request.urlopen(full_url)
    
    print(response.read().decode('utf-8'))
    
    
if __name__ == "__main__":
     main(sys.argv[1:])

