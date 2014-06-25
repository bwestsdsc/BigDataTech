#!/usr/bin/env python

import csv
import collections
import pprint
import sys

class ABSReducer(object):
    
    def getData(self):
        
        mapped_results = open('mapped_results.csv', 'r')
        record_fields = csv.reader(mapped_results, delimiter=',', quotechar='"')
        new_centers = self.recalcCenter(record_fields)
        mapped_results = open('mapped_results.csv', 'r')
        record_fields = csv.reader(mapped_results, delimiter=',', quotechar='"')
        conv_test = self.testCenters(record_fields, new_centers)
        print(conv_test)
        self.reportFindings()
            
    def recalcCenter(self, record_fields):   
        # open centroids file for creating cnetroid lat/lon records in case convergence test fails
        new_centers = collections.defaultdict(dict)
        new_center_file = open('centroids.csv', 'w')
        
        # extract records from centroids file and use as basis for recount
        for record in record_fields:
            try:
                # sum up each record's lat/lon within cluster 
                new_centers[record[0]]['lon'] += float(record[5])
                new_centers[record[0]]['lat'] += float(record[6])
                new_centers[record[0]]['count'] += 1
            except KeyError:
                # needed to initialize firt record
                new_centers[record[0]]['lon'] = float(record[5])
                new_centers[record[0]]['lat'] = float(record[6])
                new_centers[record[0]]['count'] = 1
         
        # compute average from summed records   
        for k in new_centers.keys():
            try:
                new_centers[k]['avg_lon'] = new_centers[k]['lon'] / new_centers[k]['count']
                new_centers[k]['avg_lat'] = new_centers[k]['lat'] / new_centers[k]['count']
            except KeyError:
                pass
            new_center_file.write(k + ', ' + str(new_centers[k]['avg_lon']) + ', ' + str(new_centers[k]['avg_lat']) + '\n')
  
        return new_centers
                
    def testCenters(self, record_fields, new_centers):
        
        test = 1
        #compute the delta between old positions and new
        for record in record_fields:
            lon_delta = round(float(new_centers[record[0]]['avg_lon']) - float(record[5]), 4)
            lat_delta = round(float(new_centers[record[0]]['avg_lat']) - float(record[6]), 4)
            # if greater than 1 second, the convergence threshold has not been met
            # need to iterate the mapper with new centers
            if lon_delta >= .1 or lat_delta >= .1:
                test = 0
                return test
                break
            else:
                test = 1
        return test
    
    def reportFindings(self):
        
        mapped_results = open('mapped_results.csv', 'r')
        record_fields = csv.reader(mapped_results, delimiter=',', quotechar='"')
        for record in record_fields:
            pprint.pprint(record)
        
        
                       
reducer = ABSReducer()
reducer.getData()
        
        
