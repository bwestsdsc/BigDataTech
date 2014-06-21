#!/usr/bin/python

import sys
import time
import csv
import multiprocessing

def main(argv):
    
    header_fields = {'activityType' : 0, 'AGENCY' : 1, 'activityDate' : 2, 'LEGEND' : 3, 'Charge_Description' : 4, 'BLOCK_ADDRESS' : 5, 'City_Name' : 6, 'ZipCode' : 7}
    word_list = {}
    jobs = []
    
    categories = []
    for field in argv:
        categories.append(field)
               
    for field_value in categories:
        print(field_value)
        try:
            p = multiprocessing.Process(target=groupCount, args=(field_value,))
            jobs.append(p)
            p.start()
        except Exception as e:
            print("Unable to start thread" + e)
        
def groupCount(field):
    
    word_count = {}
     
    header_index = {'activityType' : 0, 'AGENCY' : 1, 'activityDate' : 2, 'LEGEND' : 3, 'Charge_Description' : 4, 'BLOCK_ADDRESS' : 5, 'City_Name' : 6, 'ZipCode' : 7}
 
    try:
        crime_file = open('merged_crime.csv', 'r')
    except:
        print("Cannot open file")
        
    record_fields = csv.reader(crime_file, delimiter=',', quotechar='"')
     
          
    for column_value in record_fields:
        word_key = header_index[field]
        word_count.setdefault(column_value[word_key], 0)
        word_count[column_value[word_key]] += 1
          
    for k, v in word_count.items():
        result = "Term: " + k + " Count: " + str(v)
        print(result) 
    
    crime_file.close()
           
    total_elapsed = (time.clock() - total_start)
    print("Time: " + str(total_elapsed))


total_start = time.clock()   
    
if __name__ == "__main__":
     main(sys.argv[1:])
    
    
    
        
  
