import sys
import os
import argparse
import re
import logging

from massage_mei import massage_mei

def massage_file(args, file, in_dir, out_dir):
    try:
        logging.info("Massage file: " + os.path.join(in_dir, file))
        massage_mei(os.path.join(in_dir, file), os.path.join(out_dir, file + "_msg.mei"))
        logging.info("DONE.")
    except Exception as ex:
        logging.critical(ex)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MEI-Massage all matching files in the input directory.')
    parser.add_argument('in_dir')
    parser.add_argument('--out', dest='out_dir')
    parser.add_argument('--filter', dest='filter')
    parser.add_argument('-R', dest='recursive', action='store_true')
    parser.add_argument('--ignore', dest='filter_ignore')
    set_logging(parser)
    args = parser.parse_args()

    if not args.out_dir:
        args.out_dir = args.in_dir

    if args.filter:
        prog = re.compile(args.filter)

    if args.filter_ignore:
        prog_ignore = re.compile(args.filter_ignore)
        
    if args.recursive:
        for root, dirs, files in os.walk(args.in_dir):
            for file in files:
                if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                    massage_file(args, file, root, root)
    else:
        for file in os.listdir(args.in_dir):
            if (not args.filter or prog.match(file)) and (not args.filter_ignore or not prog_ignore.match(file)):
                massage_file(args, file, args.in_dir, args.out_dir)
