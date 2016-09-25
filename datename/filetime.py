"""This module is designed to build timestrings from file metadata.

Everything is done in seconds since the unix epoch or UTC.
Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""
import sys
import os
import datetime


def filetime(file_path):
   """Returns formatted time string from file metadata.

   Uses modification time.
   formattedtime string is in UTC.
   file_path - full path of file to get metadata time from.
   """
   epoch_timestamp = __get_epochtime(file_path)
   time_string = __build_timestring(epoch_timestamp)
   return time_string
    

def __build_timestring(epoch_timestamp, format_string='%Y%m%dT%H%M%SZ'):
    """Builds fromatted time string from seconds since the epoch.

    Currnetly only works for UTC.
    timestamp - seconds since the unix epoch.
    format - strftime format string
    TODO: support other timezones.
    """
    time_object = datetime.datetime.utcfromtimestamp(epoch_timestamp)
    time_string = time_object.strftime(format_string)
    return time_string
    

def __get_epochtime(file_path, metadata_type="modified"):
    """Get file metadata time in seconds since the unix epoch.
    
    file_path - full file path.
    metadata_type - metadata time type in {'accessed','created','modified'}
    Note: windows resets 'created' time on copy or move.
    """
    if metadata_type == "accessed":
        time_function = os.path.getatime
    elif metadata_type == "created":
        time_function = os.path.getctime
    elif metadata_type == "modified":
        time_function = os.path.getmtime
    else:
        raise InvalidMetadataTimeTypeError(metadata_type)
    epoch_timestamp = time_function(file_path)
    return epoch_timestamp


class InvalidMetadataTimeTypeError(Exception):
    """Invalid Metadata Time Type Error

    Only {'accessed','created','modified'} are supported.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    

#In case this is run on the command line, which is useful for tests.                                                   
if __name__ == "__main__":                                                                                              
    # Call filetime() with all command line arguments, but not the script name.                                             
    print filetime(*sys.argv[1:])                                                                                                 
