#!/usr/bin/python3
# Remove braces from files

import argparse

parser = argparse.ArgumentParser(description='remove { and } in a file.')
parser.add_argument('file', metavar='file', type=str,
                    help='The file to edit it')

args = parser.parse_args()

with open(args.file, 'r') as f:
    file = list(f)

with open(args.file, 'w') as f:
    for line in file:
        line = line.replace('{','')
        line = line.replace('}', '')
        f.write(line)
