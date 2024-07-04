import argparse
import collections
import configparser
import grp, pwd
import hashlib
import os
import re
import sys
import zlib 
from datetime import datetime
from fnmatch import fnmatch
from math import ceil
from commands import vip_init
from repository import *
from utils import *

arg_parser = argparse.ArgumentParser(description="A minimal implementation of Git.")

arg_sub_parsers = arg_parser.add_subparsers(title="Commands", dest="command")
arg_sub_parsers.required = True
init_sub_parser = arg_sub_parsers.add_parser("init", help="For initializing new git repositories.")
init_sub_parser.add_argument("path",
                             metavar="directory",
                             nargs="?",
                             default=".",
                             help="The file path to create the repository at.")

cat_file_sub_parser = arg_sub_parsers.add_parser("cat-file",
                                                 help="Read the contents of repository objects.")
cat_file_sub_parser.add_argument("type",
                                 metavar="type",
                                 choices=["blob", "commit", "tag", "tree"],
                                 help="Specify object type.")

cat_file_sub_parser.add_argument("object", 
                                 metavar="object",
                                 help="The object to be displayed.")

hash_object_sub_parser = arg_sub_parsers.add_parser("hash-object",
                                   help="Produce an ID from an object and/or create blob from file.")

hash_object_sub_parser.add_argument("-t",
                                    metavar="type",
                                    dest="type",
                                    choices=["blob", "commit", "tag", "tree"],
                                    default="blob",
                                    help="Specify the object type"
                                    )

hash_object_sub_parser.add_argument("-w",
                                    dest="write",
                                    action="store_true",
                                    help="Write the specified object into the store."
                                    )

hash_object_sub_parser.add_argument("path",
                                    help="Read object from specified <path>"
                                    )
def main(argv=sys.argv[1:]):
    args = arg_parser.parse_args(argv)
    match args.command:
        case "add"          : vip_add(args)
        case "cat-file"     : vip_cat_file(args)
        case "check-ignore" : vip_check_ignore(args)
        case "checkout"     : vip_checkout(args)
        case "commit"       : vip_commit(args)
        case "hash-object"  : vip_hash_object(args)
        case "init"         : vip_init(args)
        case "log"          : vip_log(args)
        case "ls-files"     : vip_ls_files(args)
        case "ls-tree"      : vip_ls_tree(args)
        case "rev-parse"    : vip_rev_parse(args)
        case "rm"           : vip_rm(args)
        case "show-ref"     : vip_show_ref(args)
        case "status"       : vip_status(args)
        case "tag"          : vip_tag(args)
        case _              : print("Bad command.")