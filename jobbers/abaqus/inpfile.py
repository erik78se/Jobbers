# Import modules
import re
import sys
import os


def facts(input_file):

    # Define arguments to return
    analysis_facts = dict()
    analysis_facts['restart_read'] = False
    analysis_facts['restart_write'] = False
    analysis_facts['eigenfreqency'] = False
    analysis_facts['random_response'] = False
    analysis_facts['input_files'] = []
    analysis_facts['other_files'] = []

    # Check if restart read analysis
    restart_read_re = re.compile(r'^\s*\*restart\s*.*read', re.IGNORECASE)
    # Check if restart write analysis
    restart_write_re = re.compile(r'^\s*\*restart\s*.*write', re.IGNORECASE)
    # Check if eigenfrequency analysis
    eigen_re = re.compile(r'^\s*\*FREQUENCY\s*', re.IGNORECASE)
    # Check if random response
    random_re = re.compile(r'^\s\*RANDOM\s*.*RESPONSE', re.IGNORECASE)

    # Get all model keywords
    parsed_keywords = _parse_input_file_keywords(input_file)
    # Get all associated files
    input_files, other_files = _get_all_associated_files(parsed_keywords)
    analysis_facts['input_files'] = input_files
    analysis_facts['other_files'] = other_files

    # Get if restart read analysis
    is_restart_read = filter(restart_read_re.match, parsed_keywords)
    if is_restart_read:
        analysis_facts['restart_read'] = True
    # Get if restart write analysis
    is_restart_write = filter(restart_write_re.match, parsed_keywords)
    if is_restart_write:
        analysis_facts['restart_write'] = True
    # Get if eigenfrequency analysis
    is_eigenfrequency = filter(eigen_re.match, parsed_keywords)
    if is_eigenfrequency:
        analysis_facts['eigenfreqency'] = True
    # Get if random response analysis
    is_random_response = filter(random_re.match, parsed_keywords)
    if is_random_response:
        analysis_facts['random_response'] = True

    # Return facts
    return analysis_facts


def _parse_input_file_keywords(input_file_name):
    """
    Recursive search style, if an include file is found parse include file first, and then continue.
    :param input_file_name: - Name of input / include file
    :return: parsed_input_file: - Array of keywords
    """

    # Get all lines starting with '*'
    parsed_input_file = []

    include_re_input = re.compile(r'^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)

    try:
        with open(input_file_name, 'r') as input_file_handle:

            for line in input_file_handle:

                line = line.strip()

                if line.startswith('*'):

                    # If the line starts with a '*', check if it is a call to an include file
                    match_include_file = include_re_input.search(line)
                    if match_include_file:
                        # Get file name of include file
                        include_file_name = match_include_file.group(1).strip()
                        # Recursive call
                        include_file_content = _parse_input_file_keywords(include_file_name)
                        # Append content
                        parsed_input_file.append(include_file_content)
    except NameError:
        sys.exit('ERROR - File was not found: {}'.format(input_file_name))

    return parsed_input_file


def _get_all_associated_files(keywords):

    # Include files
    include_re_input = re.compile(r'^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)

    # Other files
    include_re_file = re.compile(r'^\s*\*\w.*file\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)

    # Get all include files
    include_files = filter(include_re_input.search, keywords)
    # Check if include file exists
    missing_include_files = []
    if include_files:
        for include_file in include_files:
            if not os.path.isfile(os.path.abspath(include_file)):
                missing_include_files.append(include_file)
    if missing_include_files:
        print(' ERROR - Included files are missing:')
        for file in missing_include_files:
            print("\t {}".format(file))
        print(' EXITING - Verify naming of include files')

    # Get all other files
    other_files = filter(include_re_file.search, keywords)
    # Check if include file exists
    missing_other_files = []
    if other_files:
        for other_file in other_files:
            if not os.path.isfile(os.path.abspath(other_file)):
                missing_include_files.append(other_file)
    if missing_other_files:
        print(' ERROR - Files are missing:')
        for file in missing_other_files:
            print("\t {}".format(file))
        print(' EXITING - Verify naming of files')

    if missing_include_files or missing_other_files:
        sys.exit(1)

    return include_files, other_files
