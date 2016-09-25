# About
'datename' is a python package designed to organize files by modification date.
# Goals
Some of the goals for this project include
1. Should behave the same on any operating system which supports python.
2. Should behave ths same regardless of machine timezone
    1. This is achieved by using UTC internally.
3. Must never cause data loss.
    1. This is achieved by a trailing iterator on destination file names
    2. If the source file does not exist, or for some reason the destination cannot be written to, the package will fail without modifying the source file.

# Caveats
* Note: Author only uses UTC, specifying other timezones for output may not be as thoroughly tested.

# Usage
  TODO
