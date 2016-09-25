#!/usr/bin/env python
"""Rename a file based on its filesystem timestamp attributes.

Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""

import sys
import os
import filetime
import safemove
import argparse

def main():
    """Handle interation.
    
    Parses arguments and stuff.
    """
    parser = argparse.ArgumentParser(description="Rename files by date")
    parser.add_argument('-d','--destination')
    parser.add_argument('files', nargs='*')
    arguments = parser.parse_args()
    datename(arguments.files, arguments.destination)


def datename(files, destination=None):
    """Rename files based on their modifiation timestamps
   
    Files will be renamed to an ISO 8601 compliant UTC time string.
    """
    if not destination == None:
        for file_path in files:
            __organize(file_path, destination)
    else:
        for file_path in files:
            time_string = filetime.filetime(file_path)
            __rename(file_path, time_string)


def __organize(file_path, destination_root):
    """Organize files into iso 8601 format.
    
    Files will be in destination_root/<year>/<year>-<month>/<timestring>.<ext>
    If a file exists in the destination location, an iterator will be added.
    Gets time string from filetime.
    Parses year from first 4 characters.
    Parses month from next 2 characters.
    """
    time_string = filetime.filetime(file_path)
    year = time_string[0:4]
    month = time_string[4:6]
    year_month = year + "-" + month
    full_file_name = os.path.basename(file_path)
    file_name_part, file_extension = os.path.splitext(full_file_name)
    new_file_name = time_string + file_extension.lower()
    destination = os.path.join(
        destination_root,
        year,
        year_month,
        new_file_name
        )
    safemove.move(file_path, destination)


def __rename(file_path, new_name):
    """Rename file with same extension.

    Given the full path of a file, this function will replace only the name.
    The directory and extension will remain the same.
    In case of existing file at destination, this will iterate until free.
    """
    directory = os.path.dirname(file_path)
    full_file_name = os.path.basename(file_path)
    file_name_part, file_extension = os.path.splitext(full_file_name)
    new_file_name = new_name + file_extension.lower()
    destination = os.path.join(directory, new_file_name)
    safemove.move(file_path, destination)


# This script is meant to be called from the command line.
if __name__ == "__main__":
    main()
