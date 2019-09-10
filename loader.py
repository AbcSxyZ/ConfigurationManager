#!/usr/bin/env python3

from argparse import ArgumentParser
import configuration as conf
import os
import sys
from ConfigurationFolder import ConfigurationFolder
from diff import DiffTool


def get_options():
    """
    usage: options.py [-h] [--load | --save | --rm pattern [pattern ...]]
    
    optional arguments:
    -h, --help        show this help message and exit
    --load, -l        Load configuration files from git requisitory.
    --save, -s        Save local configuration to the remote requisitory.

    """
    parser = ArgumentParser(description="Controler for configuration files.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--load", "-l", action="store_true", \
            help="Load configuration files from git requisitory.")
    group.add_argument("--save", "-s", action="store_true", \
            help="Save local configuration to the remote requisitory.")
    group.add_argument("--rm", metavar="pattern", nargs="+", \
            help="Pattern to remove from the configuration.")
    group.add_argument("--status", "-S", action="store_true", \
            help="Get current diff for the 2 folders.")
    options = parser.parse_args()
    if options.rm is None and \
            not any([options.save, options.load, options.status]):
        parser.print_help()
        exit(1)
    return options

def main():
    options = get_options()
    local_conf = ConfigurationFolder(conf.CONFIGURATION_DIRECTORY)
    remote_conf = ConfigurationFolder(conf.REQUISITORY_LOCATION)

    if options.rm is not None:
        local_conf.remove_files(options.rm)
        remote_conf.remove_files(options.rm)
        return 0
    elif options.status:
        return DiffTool(local_conf, remote_conf).display_diff()
    elif options.load:
        dest_config = local_conf
        src_config = remote_conf
    elif options.save:
        dest_config = remote_conf
        src_config = local_conf

    moved_files = src_config.retrieve_files()
    with dest_config:
        dest_config.save_files(moved_files, src_config.directory)
    return 0

if __name__ == "__main__":
    exit(main())
