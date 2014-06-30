#!/usr/bin/env python

from collections import OrderedDict
import collections
import random
import csv
import math
import os.path
import sys
import pprint
import re

CENTROIDS = collections.defaultdict(lambda : collections.defaultdict(dict))

class ABSMapper(object):
    
    def main (self):
        
        license_data = []
        centroids = collections.defaultdict(dict)
        license_dict = collections.defaultdict(dict)
        file_inputs = csv.reader(sys.stdin, delimiter=',', quotechar='"')
        record = ''
        cent_list = []
        cent_rec = ''
        
        for line in file_inputs:
            if len(line) == 3:
                for element in line:
                    key = line[0].strip()
                    centroids[key]['lon'] = line[1]
                    centroids[key]['lat'] = line[2]
            else:
                license_data.append(line)
       
        license_dict = self.createLicenseDict(license_data)
        self.calcCentroids(license_dict, centroids)     
        cluster_dict = self.assignCluster(license_dict)

        for key in cluster_dict.keys():
             for sub_key in cluster_dict[key].keys(): 
                 try:
                      record += (str(key) + ', ' + str(sub_key) + ', ' + '"' + license_dict[sub_key]['address'] + '"' +
                             ', ' + '"' + license_dict[sub_key]['company'] + '"' + ', ' + str(cluster_dict[key][sub_key]['distance']) + 
                             ', ' + str(license_dict[sub_key]['lon']) + ', ' + str(license_dict[sub_key]['lat']) + 
                             ', ' + str(CENTROIDS[key]['lon']) +
                             ', ' + str(CENTROIDS[key]['lat']) + '\n')
      
                 except KeyError:
                     pass
                 
        sys.stdout.write(record)
 
  
    def createLicenseDict (self, abs_list):
        
        license_dict = collections.defaultdict(lambda : collections.defaultdict(dict))
        n = 0
        try:
            for line in abs_list:
                if line[0] != 'last_date':
                    company = re.sub(',', '', line[10])
                    address = re.sub(',', '', line[11])
                    license_dict[n]['company'] = company
                    license_dict[n]['address'] = address
                    license_dict[n]['lon'] = float(line[13])
                    license_dict[n]['lat'] = float(line[14])
                    n += 1
        except:
            print('Error at:' + line[0])
      
        return license_dict
    
    def calcCentroids(self, license_dict, centroids):
            
        if len(centroids.values())  > 0:
            # iteratve runs if the centroid file was already created
            centroids_file = open('centroids.csv', 'w')

            for line in centroids.keys():
                CENTROIDS[line]['lon'] = centroids[line]['lon']
                CENTROIDS[line]['lat'] = centroids[line]['lat']
                centroids_file.write(str(line) + ', ' + str(centroids[line]['lon']) + ', ' + str(centroids[line]['lat']) +'\n') 
        else:
            # initial run
            centroids_file = open('centroids.csv', 'w')
            j = 0
            for key in random.sample(license_dict.keys(), 20):
                CENTROIDS[key]['lon'] = license_dict[key]['lon']
                CENTROIDS[key]['lat'] = license_dict[key]['lat']
                centroids_file.write(str(key) + ', ' + str(license_dict[key]['lon']) + ', ' + str(license_dict[key]['lat']) + '\n')                    
 
        centroids_file.close()
        return centroids
               
        
    def assignCluster(self, license_dict):
        
        #assign license location to the nearest cluster
        cluster_dict = collections.defaultdict(lambda : collections.defaultdict(dict))
        
        for k in license_dict.keys():
            if k:
                retval = self.calcDist(license_dict[k]['lon'], license_dict[k]['lat'])
                dist_to_cent = retval[0]
                cluster_key = retval[1]
                print("Distance :" + str(dist_to_cent) + " for Cluster " + str(cluster_key))
                try: 
                    cluster_dict[cluster_key][k]['distance'] = dist_to_cent
                except KeyError:
                    pass
                
            else:
                pass
    
        return cluster_dict
            
    def calcDist(self, lon, lat):
        
        # calculation of euclidean distance over a sphere
        earth_radius = 6371 # Radius of the earth in km
        min_distance = 0
        min_key = ''
        retval = collections.namedtuple('retval', ['x', 'y'])
        distance_dict = collections.defaultdict(dict)
        try:
            for key in CENTROIDS.keys():
                print(key)
                lat2 = float(CENTROIDS[key]['lat'])
                lon2 = float(CENTROIDS[key]['lon'])
                dlon = math.radians(float(lon))-math.radians(lon2)
                dlat = math.radians(float(lat))-math.radians(lat2)
                a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(float(lat))) * math.cos(math.radians(float(lat2))) * math.sin(dlon/2) * math.sin(dlon/2)
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
                distance_dict[key] = earth_radius * c # Distance in km
            
            min_distance = min(distance_dict.values())
            for k, v in distance_dict.items():
                    if min_distance == v:
                        min_key = k
           
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        
        return retval(min_distance, min_key)
       
absMap = ABSMapper()
record = absMap.main()

            
           
            
      