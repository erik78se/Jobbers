from pathlib import Path
import re
from jobbers.abaqus.model import Inpfile
import sys

# Module wide regular expressions used to find content in .inp files
input_regexp = re.compile(r'^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)
file_regexp = re.compile(r'^.*,*\s*FILE\s*=\s*([^,]+).*', re.IGNORECASE)
restart_read_regexp = re.compile(r'^\s*\*restart\s*.*read', re.IGNORECASE)
restart_write_regexp = re.compile(r'^\s*\*restart\s*.*write', re.IGNORECASE)
eigen_regexp = re.compile(r'^\s*\*FREQUENCY\s*', re.IGNORECASE)
random_regexp = re.compile(r'^\s\*RANDOM\s*.*RESPONSE', re.IGNORECASE)


def children(infile):
        """
        Returns a list of all include files in the infile.
        Iterates over the .inp file to find specific attributes and sets them
        for the root node (infile).
        """
        r = []
        if not Path(infile.file).is_file():
            print("Not found: " + str(infile.file), file=sys.stderr)
            return []

        # Set defaults for the attributes
        infile.restart_read = False
        infile.restart_write = False
        infile.random_response = False
        infile.eigenfrequency = False
        
        # Scan for items we need
        # TODO: Performance!
        # In Python 3.5 and 3.6, pathlib stuff (infile.file) must be converted to string
        with open(str(infile.file), 'r') as fh:
            for line in fh:
                line = line.strip()

                otherfile = file_regexp.search(line)
                include = input_regexp.search(line)
                restartr = restart_read_regexp.search(line)
                restartw = restart_write_regexp.search(line)
                eigen = eigen_regexp.search(line)
                random = random_regexp.search(line)

                if include:
                    c = include.group(1).strip()
                    child = Inpfile(filename=c)
                    infile.input_files.append(child)
                    r.append(child)

                if otherfile:
                    o = include.group(1).strip()
                    infile.input_files.append(o)

                if restartr:
                    infile.restart_read = True
                    print('debug: found restart_read in ' + str(infile.file))

                if restartw:
                    infile.restart_write = True

                if eigen:
                    infile.eigenfrequency = True

                if random:
                    infile.random_response = True
                
        return r


def traverse(infile, inp_result=[]):
    """ Recursive function.
    Produces a [<Inpfiles>]
    """
    inp_result.append(infile)
    for kid in children(infile):
        traverse(kid, inp_result)
    return inp_result
