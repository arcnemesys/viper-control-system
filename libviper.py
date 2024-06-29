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

arg_parser = argparse.ArgumentParser(description="A minimal implementation of Git")

arg_sub_parsers = arg_parser.add_subparsers(title="Commands", dest="command")
arg_sub_parsers.required = True
init_sub_parser = arg_sub_parsers.add_parser("init", help="For initializing new git repositories.")
init_sub_parser.add_argument("path",
                             metavar="directory",
                             nargs="?",
                             default=".",
                             help="The file path to create the repository at.")


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