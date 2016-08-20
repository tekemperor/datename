"""This Module contains the classes related to moving files.

There is only one class though.
"""

import os.path
import os.rename

class SafeMove:
    """This Class contains all the necessary functions to safely move files.

    There is only one function though.
    """


    def move (self, source, destination, itr_pre="_", itr_post="", itr_pad=0):
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
                self.__attempt_move_safely(source, desired_path)
                done = True
            except DestinationExistsError:
                iterator += 1
    
        
    def __attempt_move_safely (self, source_path, destination_path):
        """Try to move file non-destructively.

        Assumes source_path and destination_path point to files, not folders.
        Rather than simply moving it, it checks if a file exists. Raises Exception instead of overwrite.
        Raises DestinationExistsError if the destination_path already exists.
        """
        # Check same first, rename can raise errors unnecessarily..
        if source_path == destination_path:
            return
        elif not os.path.exists(destination_path):
            os.rename(source_path, destination_path)
        else:
            raise DestinationExistsError(destination_path) 

     
class DestinationExistsError(Exception):
    """Destination Exists

    This error is thrown instead of overwriting an existing file.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self) :
        return repr(self.value)

if __name__ == "__main__":
    thing = SafeMove()
    thing.move("this.txt","that.txt")
