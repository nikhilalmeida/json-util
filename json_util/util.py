__author__ = 'nikhilalmeida'

from argparse import ArgumentParser
import json
import sys
import codecs
import ast
import itertools
import collections

ARGS = {}
parser = ArgumentParser(description='JSON utilities.')
parser.add_argument("command", help='The command to be performed. List of commands are:\n1. intersect. \n2. unique')


def intersect():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("file_2", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(args.file_2, "rb") as file_2, codecs.open(
            "output/intersection_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1],
                                                            args.key), "wb") as output_file:
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
    print "Finished processing {} lines.\nMatched {} lines".format(count, found)
    print "Finished generating the intersection"


def subtract():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("file_2", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    print "coming in here", args
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(args.file_2, "rb") as file_2, codecs.open(
            "output/subtraction_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1],
                                                           args.key), "wb") as output_file:
        cache = {}
        print "Loading file {} into memory.".format(args.file_2)
        for line in file_2:
            data = json.loads(line)
            cache[data[args.key]] = data
        count = 0
        found = 0
        for line in file_1:
            count += 1
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
            "output/union_of_{}_and_{}_on_{}".format(args.file_1.split("/")[-1], args.file_2.split("/")[-1], args.key),
            "wb") as output_file:
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
            if data[args.key] in cache and cache[data[args.key]] != "used":
                found += 1
                out = dict(data.items() + cache[data[args.key]].items())
                output_file.write("%s\n" % json.dumps(out))
                cache[data[args.key]] = "used"
            else:
                output_file.write("%s\n" % json.dumps(data))
        print "found {} title in common".format(found)
        print "Adding titles in {} that were not present in {}".format(args.file_1, args.file_2)
        for key, value in cache.items():
            if value != "used":
                output_file.write("%s\n" % json.dumps(value))

    print "Finished generating the union"


def filter_keys():
    parser.add_argument("file", help="input file 1")
    parser.add_argument("-k", "--keys", default="id", help="key to be retained")
    args = parser.parse_args(sys.argv[1:])
    keys = args.keys.strip().split(",")
    new_file = "output/{}_filtered_for_{}.json".format(args.file.split("/")[-1], "_".join(keys))
    with codecs.open(args.file, "rb") as read_file, codecs.open(new_file, "wb") as output_file:
        for line in read_file:
            new_data = {}
            data = json.loads(line)
            for key in keys:
                new_data[key] = data[key]
            output_file.write("{}\n".format(json.dumps(new_data)))

    print "Finished generating filtered file: " + new_file


def set_key():
    parser.add_argument("file", help="input file ")
    parser.add_argument("key", help="key to be set")
    parser.add_argument("value", help="value to be set")
    parser.add_argument("-k", "--type", default="string", help="data type (number/boolean/string)")
    args = parser.parse_args(sys.argv[1:])

    new_file = "output/{}_with_key_{}_set.json".format(args.file.split("/")[-1], args.key)
    with codecs.open(args.file, "rb") as read_file, codecs.open(new_file, "wb") as output_file:
        for line in read_file:
            data = json.loads(line)
            data[args.key] = args.value if args.type == "string" else ast.literal_eval(args.value)

            output_file.write("{}\n".format(json.dumps(data)))

    print "Finished generating filtered file: " + new_file


def rename_key():
    parser.add_argument("file", help="input file ")
    parser.add_argument("old_key", help="key to be renamed")
    parser.add_argument("new_key", help="new key name")

    args = parser.parse_args(sys.argv[1:])

    new_file = "output/{}_with_key_{}_renamed.json".format(args.file.split("/")[-1], args.old_key)
    with codecs.open(args.file, "rb") as read_file, codecs.open(new_file, "wb") as output_file:
        for line in read_file:
            data = json.loads(line)
            if args.old_key in data:
                data[args.new_key] = data[args.old_key]
                data.pop(args.old_key, None)

            output_file.write("{}\n".format(json.dumps(data)))

    print "Finished generating filtered file: " + new_file


def unique():
    parser.add_argument("file_1", help="input files 1")
    parser.add_argument("-k", "--key", default="id", help="key to join on")
    args = parser.parse_args(sys.argv[1:])
    with codecs.open(args.file_1, "rb") as file_1, codecs.open(
            "output/{}_unique_on_{}".format(args.file_1.split("/")[-1], args.key), "wb") as output_file:
        cache = set()
        print "Loading file {} into memory.".format(args.file_1)
        for line in file_1:
            data = json.loads(line)
            if data[args.key] not in cache:
                output_file.write(line)
                cache.add(data[args.key])

    print "Finished finding uniques"


def tab_to_json():
    parser.add_argument("file_1", help="input file 1")
    parser.add_argument("-k", "--keys", default=None, help="comma separated list of keys if no keys exists")
    args = parser.parse_args(sys.argv[1:])
    new_file = "output/{}.json".format(args.file_1.split("/")[-1].split(".")[0])

    with codecs.open(args.file_1, "rb") as file_1, codecs.open(
            new_file, "wb") as output_file:
        if not args.keys:
            keys = file_1.readline().strip().split("\t")
        else:
            keys = args.keys.strip().split(",")

        print "Loading file {} into memory.".format(args.file_1)
        count = 0
        for line in file_1:
            count += 1
            if count % 500000 == 0:
                print count
            data = line.strip().split("\t")
            data = [d.strip() for d in data]
            output_file.write("{}\n".format(json.dumps(dict(itertools.izip(keys, data)))))
    print "Finished converting {} to json.\nNew file located at {}".format(args.file_1, new_file)


def find_keys(input_file=None):
    if not input_file:
        parser.add_argument("file_1", help="input file")
        args = parser.parse_args(sys.argv[1:])
        input_file = args.file_1
    keys = set()
    print "Finding keys in json file"
    with codecs.open(input_file, "rb") as file_1:
        print "Loading file {} into memory.".format(input_file)
        for line in file_1:
            for key in json.loads(line).keys():
                keys.add(key.strip())
    print "Finished finding keys...\n Keys are:\n",
    for key in keys:
        print key,",\t",
    return keys


def json_to_tab():
    parser.add_argument("file_1", help="input file")
    args = parser.parse_args(sys.argv[1:])
    new_file_name = "output/{}.tab".format(args.file_1.split("/")[-1].split(".")[0])
    keys = find_keys(args.file_1)

    with codecs.open(args.file_1, "rb") as file_1, codecs.open( new_file_name, "wb") as output_file:
        [output_file.write("{}\t".format(key)) for key in keys]
        output_file.write("\n")

        print "Loading file {} into memory.".format(args.file_1)
        for line in file_1:
            data = json.loads(line)
            for key in keys:
                output_file.write("{}\t".format(data.get(key,"")))
            output_file.write("\n")
    print "Finished converting {} to tab.\nNew file located at {}".format(args.file_1, new_file_name)





if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print "please pass the command as the first argument"
        exit(0)

    if sys.argv[1] == 'intersect':
        intersect()
    elif sys.argv[1] == 'subtract':
        subtract()
    elif sys.argv[1] == 'union':
        union()
    elif sys.argv[1] == 'filter_keys':
        filter_keys()
    elif sys.argv[1] == 'set_key':
        set_key()
    elif sys.argv[1] == 'rename_key':
        rename_key()
    elif sys.argv[1] == 'unique':
        unique()
    elif sys.argv[1] == 't2j':
        tab_to_json()
    elif sys.argv[1] == 'j2t':
        json_to_tab()
    elif sys.argv[1] == 'find_keys':
        find_keys()
    else:
        print "Could not recognize command."
    print "done"
