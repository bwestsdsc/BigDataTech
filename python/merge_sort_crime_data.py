#!/usr/bin/python

import sys
import time
import re
    
def main(argv):
    
        total_start = time.clock()
        sort_key = sys.argv[7]
        print('The sort key is: ' + sort_key)
        header = joinFiles(argv)
        sortFile(header, sort_key)
        
        total_elapsed = (time.clock() - total_start)
        
        print("Total duration: " + str(total_elapsed))
        
def joinFiles(input_tables):
    
        header = ''
    
        merge_start = time.clock()
        
        merged_output = open('merged_crime.csv', 'w')
        
        for line in input_tables[1:6]:     
            annual_file = open(line, 'r')
            for annual_line in annual_file:
                if re.search("activityType,AGENCY,activityDate,LEGEND,Charge_Description,BLOCK_ADDRESS,City_Name,ZipCode", annual_line) and header == '':
                    header = annual_line
                elif re.search("activityType,AGENCY,activityDate,LEGEND,Charge_Description,BLOCK_ADDRESS,City_Name,ZipCode", annual_line) and header != '':
                    pass
                elif annual_line == '':
                    pass
                elif re.match(",,,,,,,", annual_line):
                    pass
                else:
                    merged_output.write(annual_line)
        
        merged_output.close()
                
                
        merge_elapsed = (time.clock() - merge_start)
        print("File merging duration: " + str(merge_elapsed))
        return header
        
        
def sortFile(header, sort_key):
    
    sort_order = {'activityType' : 0, 'AGENCY' : 1, 'activityDate' : 2, 'LEGEND' : 3, 'Charge_Description' : 4, 'BLOCK_ADDRESS' : 5, 'City_Name' : 6, 'ZipCode' : 7}
    sort_by = sort_order[sort_key]
    sort_start = time.clock()
    
    field_list = []
    
    merged_output = open('merged_crime.csv', 'r')
    
    for line in merged_output:
        fields = line.split(',')
        field_list.append(fields)   
        
    sorted_output = open('sorted_output.csv', 'w')
    sorted_list = sorted(field_list, key=lambda x: x[sort_order[sort_key]])
    sorted_output.write(header)
    for record in sorted_list:
        sorted_output.write(',' .join(record))
    
    sorted_output.close()
    merged_output.close()
     
    sort_elapsed = (time.clock() - sort_start)
    
    print("Sort file duration: " + str(sort_elapsed))
           
if __name__ == "__main__":
    main(sys.argv[1:])


        
    
        
