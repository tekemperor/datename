"""This module is designed to build timestrings from file metadata.

Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""
import sys
import getopt
import os
import datetime
import time
import safemove

def __build_timestring(utc_timestamp, format='%Y%m%d%T%H%M%S%Z'):
    
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

def rename(pathFull, style, timeString):
    if not os.path.isfile(pathFull):
        return
    pathDir = os.path.dirname(pathFull)
    pathFile = os.path.basename(pathFull)
    fileName, fileExt = os.path.splitext(pathFile)
    fileSuffix = "_" + fileName + fileExt
    if style == "-R":
        fileSuffix = fileExt
    tempPath = os.path.join(pathDir, timeString + fileSuffix)
    safemove.move(pathFull, tempPath)

if __name__ == "__main__":
    main()