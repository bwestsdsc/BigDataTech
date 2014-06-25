#!/usr/bin/env python

from collections import OrderedDict
import collections
import random
import csv
import math
import os.path
import sys



CENTROIDS = collections.defaultdict(lambda : collections.defaultdict(dict))

class ABSMapper(object):
    
    def main (self, file):
        
        abs_data = open(file, 'r')
        abs_list = csv.reader(abs_data, delimiter=',', quotechar='"')
        license_dict = self.createLicenseDict(abs_list)
        centroids = (self.calcCentroids(license_dict))
        cluster_dict = self.assignCluster(license_dict)
        reducer_file = open('mapped_results.csv', 'w', newline='')
        reducer_writer = csv.writer(reducer_file, delimiter=',', quotechar='"')
        for key in cluster_dict:
            for sub_key in cluster_dict[key].keys():
                record = [str(key), str(sub_key), str(cluster_dict[key][sub_key]['address']), str(cluster_dict[key][sub_key]['company']), str(cluster_dict[key][sub_key]['distance']), str(cluster_dict[key][sub_key]['lon']), str(cluster_dict[key][sub_key]['lat'])]
                reducer_writer.writerow(record)
        
    def createLicenseDict (self, abs_list):
        
        license_dict = collections.defaultdict(lambda : collections.defaultdict(dict))
        n = 0
        try:
            for line in abs_list:
                 license_dict[n]['company'] = line[10]
                 license_dict[n]['address'] = line[11]
                 license_dict[n]['lon'] = line[13]
                 license_dict[n]['lat'] = line[14]
                 n += 1
        except TypeError:
            pass
        
        return license_dict
    
    def calcCentroids(self, license_dict):
        
        if os.path.isfile('centroids.csv'):
            # iteratve runs if the centroid file was already created
            centroid_file = open('centroids.csv', 'r')
            for line in centroid_file:
                line_list = (line.split(','))
                CENTROIDS[line_list[0]]['lon'] = line_list[1]
                CENTROIDS[line_list[0]]['lat'] = line_list[2].strip()           
        else:
            # initial run
            centroid_file = open('centroids.csv', 'w')
            for key in random.sample(license_dict.keys(), 100):
                CENTROIDS[key]['lon'] = license_dict[key]['lon']
                CENTROIDS[key]['lat'] = license_dict[key]['lat']
                centroid_file.write(str(key) +', ' + str(CENTROIDS[key]['lon']) + ', ' + str(CENTROIDS[key]['lat'] + "\n"))
        
        
    def assignCluster(self, license_dict):
        
        #assign license location to the nearest cluster
        cluster_dict = collections.defaultdict(dict)
        for k in license_dict.keys():
            if k:
                retval = self.calcDist(license_dict[k]['lon'], license_dict[k]['lat'])
                dist_to_cent = retval[0]
                cluster_key = retval[1]
                cluster_dict[cluster_key][k] = license_dict[k]
                cluster_dict[cluster_key][k]['distance'] = dist_to_cent
            else:
                pass
    
        return cluster_dict
            
    def calcDist(self, lon, lat):
        
        # calculation of euclidean distance over a sphere
        earth_radius = 6371 # Radius of the earth in km
        min_distance = float('1000000')
        min_key = ''
        retval = collections.namedtuple('retval', ['x', 'y'])
        try:
            for key in CENTROIDS.keys():
                lat2 = float(CENTROIDS[key]['lat'])
                lon2 = float(CENTROIDS[key]['lon'])
                dlon = math.radians(float(lon))-math.radians(lon2)
                dlat = math.radians(float(lat))-math.radians(lat2)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(float(lat))) * math.cos(math.radians(float(lat2))) * math.sin(dlon/2) * math.sin(dlon/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
                distance = earth_radius * c # Distance in km
                if distance < min_distance:
                    min_distance = distance
                    min_key = key
                                
            return retval(min_distance, min_key)
        
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
       
absMap = ABSMapper()
absMap.main('abs-licenses-casnd.csv')
            
           
            
      