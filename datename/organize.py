"""This module is designed to organize files by prefixes.

This is currently explicitly coded to parsing year and month.
Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""

import os
import sys
import safemove


def organize(destination_root, file_path_list=[]):
    """Organize files named in iso 8601 format.
    
    Assumes filenames match strftime pattern '%Y%m%dT%H%M%SZ'
    Files will be in destination_root/<year>/<year>-<month>/<file>
    Filenames will only be changed to prevent overwriting an existing file.
    If a file exists in the destination location, an iterator will be added.
    Parses year from first 4 characters.
    Parses month from next 2 characters.
    """
    for file_path in file_path_list:
        file_name = os.path.basename(file_path)
        year = file_name[0:4]
        month = file_name[4:6]
        year_month = year + "-" + month
        destination = os.path.join(
            destination_root,
            year,
            year_month,
            file_path
            )
        safemove.move(file_path, destination)


# In case this is called from the command line, useful for testing.
if __name__ == "__main__":
    
    organize(sys.argv[1], sys.argv[2:])
