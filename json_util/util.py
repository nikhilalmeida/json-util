__author__ = 'nikhilalmeida'

from argparse import ArgumentParser
import json
import sys
import codecs

ARGS = {}
parser = ArgumentParser(description='JSON utilities.')
parser.add_argument("command", help='The command to be performed. List of commands are:\n1. intersect. \n2. unique')


def intersect():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("file_2", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(args.file_2, "rb") as file_2, codecs.open(
            "output/intersection_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1], args.key), "wb") as output_file:
        cache = {}
        print "Loading file {} into memory.".format(args.file_1)
        for line in file_1:
            data = json.loads(line)
            cache[data[args.key]] = data
        print "Finding intersection".format(args.file_1)
        count = 0
        found = 0
        for line in file_2:
            count += 1
            if count % 100000 == 0:
                print "Finished processing {} lines.\nMatched {} lines".format(count, found)
            data = json.loads(line)
            if data[args.key] in cache:
                found += 1
                out = dict(data.items() + cache[data[args.key]].items())
                output_file.write("%s\n" % json.dumps(out))
    print "Finished generating the intersection"


def subtract():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("file_2", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    print "coming in here",args
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(args.file_2, "rb") as file_2, codecs.open(
            "output/subtraction_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1], args.key), "wb") as output_file:
        cache = {}
        print "Loading file {} into memory.".format(args.file_2)
        for line in file_2:
            data = json.loads(line)
            cache[data[args.key]] = data
        count = 0
        found = 0
        for line in file_1:
            count +=1
            if count % 100000 == 0:
                print "Finished processing {} lines.\nUnMatched {} lines".format(count, found)
            data = json.loads(line)
            if data[args.key] not in cache:
                found += 1
                output_file.write(line)
    print "Finished generating the subtraction"


def union():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("file_2", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(args.file_2, "rb") as file_2, codecs.open(
            "output/union_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1], args.key), "wb") as output_file:
        cache = {}
        print "Loading file {} into memory.".format(args.file_1)
        for line in file_1:
            data = json.loads(line)
            cache[data[args.key]] = data
        print "Finding common section".format(args.file_1)
        count = 0
        found = 0
        for line in file_2:
            count += 1
            if count % 100000 == 0:
                print "Finished processing {} lines.\nMatched {} lines".format(count, found)
            data = json.loads(line)
            if data[args.key] in cache:
                found += 1
                out = dict(data.items() + cache[data[args.key]].items())
                output_file.write("%s\n" % json.dumps(out))
                cache[data[args.key]] = "used"
            else:
                output_file.write("%s\n" % json.dumps(data))
        print "found {} title in common".format(found)
        print "Adding titles in {} that were not present in {}".format(args.file_1, args.file_2)
        for key, value in cache.items():
            if value!="used":
                output_file.write("%s\n" % json.dumps(value))

    print "Finished generating the union"




if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print "please pass the command as the first argument"
        exit(0)
    print sys.argv
    if sys.argv[1] == 'intersect':
        intersect()
    elif sys.argv[1] == 'subtract':
        subtract()
    elif sys.argv[1] == 'union':
        union()
    print "done"
