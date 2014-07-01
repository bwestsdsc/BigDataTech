#!/usr/bin/env python

import csv
import collections
import pprint
import sys
import re


class ABSReducer(object):
    
    def getData(self):
     
        license_data = []
        centroids = collections.defaultdict(dict)
        mapped_data = collections.defaultdict(lambda : collections.defaultdict(dict))
        input_str = ''
        input_list = []
        line = ''
        new_list = []
        
        input_str = csv.reader(sys.stdin, delimiter=',', quotechar='"')
     
        for line in input_str:
            if len(line) > 7:
                cluster_key = line[0].strip()
                license_key = line[1].strip()
                address = (line[2].strip())
                company = line[3].strip()
                distance = line[4].strip() 
                mapped_data[cluster_key][license_key]['address'] = address
                mapped_data[cluster_key][license_key]['company'] = company
                mapped_data[cluster_key][license_key]['distance'] = distance
                mapped_data[cluster_key][license_key]['lon'] = line[5].strip()
                mapped_data[cluster_key][license_key]['lat'] = line[6].strip()
                mapped_data[cluster_key][license_key]['key_lon'] = line[7].strip()
                mapped_data[cluster_key][license_key]['key_lat'] = line[8].strip()
    
        new_centers = self.recalcCenter(mapped_data) 
        conv_test = self.testCenters(mapped_data, new_centers)
        print("Convergence Test Result: " + str(conv_test))
        self.reportFindings(mapped_data)
            
    def recalcCenter(self, record_fields): 
        
        new_centers = collections.defaultdict(lambda : collections.defaultdict(dict))
        new_center_file = open('centroids.csv', 'w')

        for cluster_key in record_fields.keys():
            for license_key in record_fields[cluster_key].keys():
                try:
                 # sum up each record's lat/lon within cluster 
                    new_centers[cluster_key]['sum_lon'] += float(record_fields[cluster_key][license_key]['lon'])
                    new_centers[cluster_key]['sum_lat'] += float(record_fields[cluster_key][license_key]['lat'])
                    new_centers[cluster_key]['count'] += 1
                except TypeError:
                    new_centers[cluster_key]['sum_lon'] = float(record_fields[cluster_key][license_key]['lon'])
                    new_centers[cluster_key]['sum_lat'] = float(record_fields[cluster_key][license_key]['lat'])
                    new_centers[cluster_key]['count'] = 1
             
         # compute average from summed record  
        for k in new_centers.keys():
             try:
                 new_centers[k]['avg_lon'] = new_centers[k]['sum_lon'] / new_centers[k]['count']
                 new_centers[k]['avg_lat'] = new_centers[k]['sum_lat'] / new_centers[k]['count']
             except KeyError:
                 pass
             new_center_file.write(k + ', ' + str(new_centers[k]['avg_lon']) + ', ' + str(new_centers[k]['avg_lat']) + '\n')
        new_center_file.close()
        
        return new_centers
                
    def testCenters(self, record_fields, new_centers):
        
        test = 1
        #compute the delta between old positions and new
        for cluster_key in record_fields.keys():
            for license_key in record_fields[cluster_key].keys():
                lon_delta = round(float(new_centers[cluster_key]['avg_lon']) - float(record_fields[cluster_key][license_key]['lon']), 4)
                lat_delta = round(float(new_centers[cluster_key]['avg_lat']) - float(record_fields[cluster_key][license_key]['lat']), 4)
            # if greater than 1 second, the convergence threshold has not been met
            # need to iterate the mapper with new centers
                if lon_delta > .2 or lat_delta >= .097:
                    test = 0
                    return test
                    break
                else:
                    test = 1
                    
        return test
    
    def reportFindings(self, mapped_data):

        max_record = 0
        min_record = 10000
        max_key = ''
        min_key = ''
 
        for licensee in mapped_data:
            print(str(licensee) + ' ' + str(len(mapped_data[licensee].keys())))
            if max_record < len(mapped_data[licensee].keys()):
                max_record = len(mapped_data[licensee].keys())
                max_key = licensee
            elif min_record > len(mapped_data[licensee].keys()):
                min_record = len(mapped_data[licensee].keys())
                min_key = licensee
                
        print('Maximum Number Licenses/Cluster: ' + str(max_key) + ' - ' + str(max_record))
        print('Minimum Number Licenses/Cluster: ' + str(min_key) + ' - ' + str(min_record))
                                             
reducer = ABSReducer()
reducer.getData()
        
        
