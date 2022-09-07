#!/usr/bin/env python3

''' IMPORTS '''
import argparse
from concurrent.futures import process
from email.utils import formataddr
from venv import create
import vt
from datetime import datetime 
import csv
from vt_meeseeks import domain_functions, hash_functions
from datetime import datetime

def create_output_file(ioc_type, output_name):
    if not output_name:
        now = datetime.now()
        formatted_date = now.strftime("%Y%m%d")
        output_filename = formatted_date + "_" + ioc_type + ".csv"
    
    FOUT = open(output_filename, 'w')

    # create csv writer
    writer = csv.writer(FOUT)
    return writer

def get_args():
    parser = argparse.ArgumentParser(description="Various tools leveraging the VirusTotal API")
    parser.add_argument('-a','--apikey', dest="apikey", required=True)
    parser.add_argument('-i','--input-file', dest="input_file", required=True)
    parser.add_argument('-t', '--ioc-type', dest="ioc_type", choices=['hash', 'domain'], required=True)
    parser.add_argument('-o','--output-name', dest="output_name", default="", required=False)
    #parser.add_argument('--pass', dest="user_pass", required=True)
    #parser.add_argument('-replicate')
    #parser.add_argument('--t', '--test', dest="test_conn", required=False)

    return parser.parse_args()

def main():
    print("hello world")
    
     # get args 
    args = get_args()

    # print("DEBUG:")
    # print(args)



    # create vt client
    try:
        vt_client = vt.Client(args.apikey)
        print('INFO: VT client created')
    except Exception as err: 
        print("ERROR: Failed to create VT client. {}".format(err))

    # create output file
    try:
        csv_obj = create_output_file(args.ioc_type, args.output_name)
    except Exception as err: 
        print("ERROR: Failed to create output file. {}".format(err))

    # open primary lookup for comparison 
    #LOOKUP = open("primary_lookups/{}_lookup_primary.csv".format(args.ioc_type), 'r')

    if args.ioc_type == "domain":
        domain_functions.add_column_headers(csv_obj)
        
        with open(args.input_file, 'r') as FIN:
            with  open("primary_lookups/{}_lookup_primary.csv".format(args.ioc_type), 'r') as LOOKUP:
                lookup_reader = csv.reader(LOOKUP, delimiter=",")
                for domain in FIN:
                    domain = domain.strip("\n")
                    print("DEBUG domain: ", repr(domain)) 
                    for row in lookup_reader:
                        #int("DEBUG row: ", row)
                        print("DEBUG row[1]: ", repr(row[1]))
                        if domain == row[1]:
                            print('INFO: match found in lookup for {}. Checking next domain in input list.'.format(domain))
                            break
                        else:
                            continue
                    else:
                        print("INFO: No match found for {}".format(domain))
                        domain = domain.strip('\n') # remove new line 
                        domain_result = domain_functions.get_domain_info(vt_client, domain)
                        domain_functions.write_to_output(csv_obj, domain_result)
                
                
    '''ADD CODE FOR HASH HEADERS'''
    
    
            

if __name__ == '__main__':
    main()