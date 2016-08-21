"""This Module is designed to safely move a file.

Author: Brian Lindsay
Author Email: tekemperor@gmail.com
"""

import os
import sys


def move (source, destination, itr_pre="_", itr_post="", itr_pad=0):
    """Try to move a file iteratively.

    Attempts to move a file, appends increasing number if unsuccessful.

    source - full path of file to be moved.
    destination - full path including file name of desired location.
    Optional Iteration parameters in case desired path is taken.
    itr_pre - iterator prefix, will be to the left of the iterator.
    itr_post - iterator postfix, will be to the right of the iterator.
    itr_pad - iterator padding, ensures minimum width for iteration.

    If ltr_pad is specified, the first case will use an iterator.
    """
    directory = os.path.dirname(destination)
    full_file_name = os.path.basename(destination)
    file_name_part, file_extension = os.path.splitext(full_file_name)
    file_extension = file_extension.lower()
    iterator = 0
    done = False
    while not done:
        iteration_string = (""
            + itr_pre
            + str(iterator).zfill(itr_pad)
            + itr_post
            )
        # omit iteration string for first pass, unless padded.
        if iterator == 0 and itr_pad == 0:
            iteration_string = ""
        desired_file = (""
            + file_name_part
            + iteration_string 
            + file_extension
            )
        desired_path = os.path.join(directory, desired_file)
        try:
            __attempt_move_safely(source, desired_path)
            done = True
        except DestinationExistsError:
            iterator += 1

    
def __attempt_move_safely (source, destination):
    """Try to move file non-destructively.

    Assumes 'source' and 'destination' point to files, not folders.
    Raises 'SourceDoesNotExistError' if 'source' does not exist.
    Raises 'DestinationExistsError' if 'destination' already exists.
    Note: The check for existing file and the move is not atomic.
    """
    # Check same path, rename can raise errors if source is destionation.
    if source == destination:
        return
    elif not os.path.exists(destination):
        os.rename(source, destination)
    else:
        # The path exists, this script WILL NOT OVERWRITE!
        raise DestinationExistsError(destination) 

     
class DestinationExistsError(Exception):
    """Destination Exists

    This error is thrown instead of overwriting an existing file.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


# In case this is run on the command line, which is useful for tests.
if __name__ == "__main__":
    # Call move() with all command line arguments, but not the script name.
    move(*sys.argv[1:])
