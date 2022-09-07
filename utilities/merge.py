import csv
import argparse
from fileinput import lineno

def domain_merge(src_file, dest_file, ignore_headers):

    print('DEBUG in domain_merge')
    print('DEBUG src_file: ', src_file)
    print('DEBUG dest_file: ', dest_file)


    # create CSV reader and CSV writer
    src_csv = open(src_file, 'r')
    src_reader = csv.reader(src_csv)
    if ignore_headers:
        next(src_reader, None)

    dest_csv = open(dest_file, 'a')
    dest_writer = csv.writer(dest_csv)

    for line in src_reader:
        try:
            dest_writer.writerow(line)
        except Exception as err:
            print('Failed to add row to destination CSV. {}'.format(err))

    src_csv.close()
    dest_csv.close()


def get_args():
    parser = argparse.ArgumentParser(description="A utility to merge new output files into the primary lookup file")
    parser.add_argument('-s','--src-file', dest="src_file", required=True)
    parser.add_argument('-d','--dest-file', dest="dest_file", required=True)
    parser.add_argument('-t', '--ioc-type', dest="ioc_type", choices=['domain'], required=True)
    parser.add_argument('--ignore-headers', dest="ignore_headers", required=False, action='store_true')
    #parser.add_argument('-o','--output-name', dest="output_name", default="", required=False)
    #parser.add_argument('--pass', dest="user_pass", required=True)
    #parser.add_argument('-replicate')
    #parser.add_argument('--t', '--test', dest="test_conn", required=False)

    return parser.parse_args()

def main():
    print("hello world")
    
     # get args 
    args = get_args()

    print('DEBUG headers: ', args.ignore_headers)

    if args.ioc_type == "domain":
        domain_merge(args.src_file, args.dest_file, args.ignore_headers)

    print('INFO: CSV merge has been completed')

if __name__ == '__main__':
    main()