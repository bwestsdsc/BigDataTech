#!/usr/bin/env python

from collections import OrderedDict
import collections

class ABSMapper(object):
    
    def sorter (self, chunk):
        
        license_dict = collections.defaultdict(lambda : collections.defaultdict(dict))
        try:
            for line in chunk:
                license_dict[line[5]]['company'] = line[10]
                license_dict[line[5]]['address'] = line[11]
                license_dict[line[5]]['lon'] = line[13]
                license_dict[line[5]]['lat'] = line[14]
        except TypeError:
            pass
        
        sorted_license = OrderedDict(sorted(license_dict.items(),key = lambda x: (x[1]['lon'], x[1]['lat']),reverse = True))
        augmented_license = self.calcDist(sorted_license)
            
        #return sorted_license
    
    def calcDist(self, sorted_license):
        
        for k in sorted_license.keys():
            print('Lon: ' + sorted_license[k]['lon'] +' Lat: ' + sorted_license[k]['lat'])
            
      