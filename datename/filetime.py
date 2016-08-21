"""This module is designed to build timestrings from file metadata.

Everything is done in seconds since the unix epoch or UTC.
Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""
import sys
import os
import datetime
import time

def __build_timestring(epoch_timestamp, format='%Y%m%d%T%H%M%S%Z'):
def __get_epochtime(file, type="modified"):
    """Get file metadata time in seconds since the unix epoch.
    
    Metadata time can be any of {'accessed','created','modified'}
    Defaults to modified.
    """
    if type == accessed:
        time_function = os.path.getatime
    elif type == created:
        time_function = os.path.getctime
    elif type == modified:
        time_function = os.path.getmtime
    else:
        raise InvalidMetadataTimeTypeError(type)
    return time_function(file)


class InvalidMetadataTimeTypeError(value):
    """Invalid Metadata Time Type Error
    Only {'accessed','created','modified'} are supported.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
    
def usage():
    print "Usage:"
    print "datename [-hcmapr] [-f <format>] <file> ..."
    print "	-h		help (this)"
    print "	-c		creation time"
    print "	-m		modified time (default)"
    print "	-a		accessed time"
    print "	-p		prefix filename"
    print "	-R		rename file (default)"
    print "	-u		use UTC (default)"
    print "	-l		use local time instead of UTC."
    print "	-f <format>	strftime format date (default is '%Y%m%dT%H%M%S%Z')"
    print "			Note: %Z and %z cannot be escaped."

def main ():
    # Defaults
    attribute = "-m"
    style = "-R"
    formatString = '%Y%m%dT%H%M%S%Z'
    utc = "-u"
    # Options
    a, s, f, l, u = getOptions(sys.argv, attribute, style, formatString, utc)
    attribute = a
    style = s
    formatString = f
    files = l
    utc = u
    # Iterate
    for path in files:
        rename(path, style, getTimeString(formatString, utc, path, attribute))

def getOptions(argv, attribute, style, formatString, utc):
    try:
        opts, fileList = getopt.getopt(argv[1:],"hcmapRful:",["help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-c", "-m", "-a"):
            attribute = o
        elif o in ("-p", "-R"):
            style = o
        elif o == "-f":
            formatString = a
        elif o in ("-u", "-l"):
            utc = o
        else:
            print "The programmer seems to have neglected to correctly map this option."
            print "Option: " + str(o)
            print "Please alert the programmer to his negligence."
            sys.exit()
    return attribute, style, formatString, fileList, utc

def getTimeObj(path, attribute, utc):
    timestamp = time.mktime(datetime.datetime.now().timetuple())
    if attribute == "-m":
        timestamp = os.path.getmtime(path)
    elif attribute == "-c":
        timestamp = os.path.getctime(path)
    elif attribute == "-a":
        timestamp = os.path.getatime(path)
    timeObj = datetime.datetime.utcfromtimestamp(timestamp)
    if utc == "-l":
        timeObj = datetime.datetime.fromtimestamp(timestamp)
    return timeObj

def getTimeZone(utc):
    if utc == "-l":
        return time.strftime('%Z')
    # UTC aka Zulu time following ISO 8601 (e.g. 12:00:00Z)
    return "Z"

def getTimeOffset(utc):
    if utc == "-l":
        return time.strftime('%z')
    return "+0000"

def fixFormat(formatString, utc):
    formatString = formatString.replace('%Z', getTimeZone(utc))
    formatString = formatString.replace('%z', getTimeOffset(utc))
    formatString = formatString.replace('+','_')
    formatString = formatString.replace(':','')
    return formatString

def getTimeString(formatString, utc, path, attribute):
    formatString = fixFormat(formatString, utc)
    timeObj = getTimeObj(path, attribute, utc)
    timeString = timeObj.strftime(formatString)
    return timeString

if __name__ == "__main__":
    main()
