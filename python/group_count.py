#!/usr/bin/python

import sys
import time
import csv

def main(argv):
    
        total_start = time.clock()
        header_fields = {'activityType' : 0, 'AGENCY' : 1, 'activityDate' : 2, 'LEGEND' : 3, 'Charge_Description' : 4, 'BLOCK_ADDRESS' : 5, 'City_Name' : 6, 'ZipCode' : 7}
        
        word_list = {}
        
        n = 0
        for field_values in argv:
            groupCount(argv[n])
            n += 1
        
        total_elapsed = (time.clock() - total_start)
        print("Time: " + str(total_elapsed))
        
def groupCount(field):
    
    word_count = {}
    
    header_index = {'activityType' : 0, 'AGENCY' : 1, 'activityDate' : 2, 'LEGEND' : 3, 'Charge_Description' : 4, 'BLOCK_ADDRESS' : 5, 'City_Name' : 6, 'ZipCode' : 7}

    crime_file = open('merged_crime.csv', 'r')
    record_fields = csv.reader(crime_file, delimiter=',', quotechar='"')
         
    for column_value in record_fields:
        word_key = header_index[field]
        # print (field + " - " + word_key)
        word_count.setdefault(column_value[word_key], 0)
        word_count[column_value[word_key]] += 1
        
    for k, v in word_count.items():
        print("Term: " + k + " Count: " + str(v))        

if __name__ == "__main__":
    main(sys.argv[1:])
