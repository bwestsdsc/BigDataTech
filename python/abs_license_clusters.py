#!/usr/bin/env python

import sys
import time
import csv
import multiprocessing
from itertools import *
from abs_mapper import ABSMapper

class ABSLicenseCluster(object):

    def splitter(self, abs_data_file):
        
        mpp = multiprocessing.Pool(6)
        
        abs_data = open(abs_data_file, 'r')
        abs_fields = csv.reader(abs_data, delimiter=',', quotechar='"')
        for chunk in self.grouper(1000, abs_fields):
            mapper = ABSMapper()
            sorted_licenses_dict = mapper.sorter(chunk)
            
        reducer = ABSReducer()
        
            
            
    def grouper(n, iterable, padvalue=None):
    
        if iterable != '':
            return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)
   
file_name = 'abs-licenses-casnd.csv'         
cluster = ABSLicenseCluster
cluster.splitter(cluster, file_name)