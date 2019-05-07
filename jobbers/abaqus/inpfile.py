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
    input_file = os.path.abspath(input_file)
    parsed_keywords, include_files, error_messages = _parse_input_file_keywords(input_file)
    analysis_facts['input_files'] = include_files
    #print("\n Parsed keywords: ")
    #for keyword in parsed_keywords:
    #    print("   {}".format(keyword))

    print("\n Parsed include files: ")
    for include_file in include_files:
        print("   {}".format(include_file))

    if error_messages:
        print("\n Parsed include files error_messages: ")
        for error_message in error_messages:
            print("   {}".format(error_message))

    # TODO: Fix function to find other files, currently re problems
    # Get all associated files
    #print("\nGet associated files")
    #other_files = _get_all_associated_files(parsed_keywords)
    #analysis_facts['other_files'] = other_files
    #print("\n Other files: ")
    #for other_file in other_files:
    #    print("   {}".format(other_file))

    print("\n Checking analysis type:")
    for keyword in parsed_keywords:
        # Get if restart read analysis
        if restart_read_re.match(keyword):
            print("\tThis is a restart analysis")
            analysis_facts['restart_read'] = True

        # Get if restart write analysis
        if restart_write_re.match(keyword):
            print("\tThis analysis write restart files")
            analysis_facts['restart_write'] = True

        # Get if eigenfrequency analysis
        if eigen_re.match(keyword):
            print("\tThis is a eigenfrequency analysis")
            analysis_facts['eigenfreqency'] = True

        # Get if random response analysis
        if random_re.match(keyword):
            print("\tThis is a random response analysis")
            analysis_facts['random_response'] = True

    # Return facts
    return analysis_facts


def _parse_input_file_keywords(input_file_name):
    """
    Recursive search style, if an include file is found parse include file first, and then continue.
    :param input_file_name: - Name of input / include file
    :return: parsed_input_file: - Array of keywords
    """

    parsed_input_file = []
    include_files = []

    error_messages = []

    current_path = os.path.dirname(input_file_name)
    include_re_input = re.compile(r'^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)
    try:
        with open(input_file_name, 'r') as input_file_handle:

            for line in input_file_handle:

                line = line.strip()

                if line.startswith('*') and not line.startswith('**'):
                    # If the line starts with a '*', check if it is a call to an include file
                    match_include_file = include_re_input.search(line)
                    if match_include_file:
                        # Get file name of include file
                        include_file_name = match_include_file.group(1).strip()
                        # Recursive call
                        if os.path.isabs(include_file_name) and os.path.isfile(include_file_name):
                            include_file_name = os.path.abspath(include_file_name)
                        else:
                            include_file_name = os.path.join(current_path, include_file_name)

                        if not os.path.isfile(include_file_name):
                            error_messages.append(' ERROR: File not found and hence not parsed:\n\t {}'.format(include_file_name))
                            break

                        # Add include file to list
                        include_files.append(include_file_name)

                        include_file_content, new_include_files_found, new_error_messages = _parse_input_file_keywords(include_file_name)
                        # Append content
                        parsed_input_file.extend(include_file_content)
                        include_files.extend(new_include_files_found)
                        error_messages.extend(new_error_messages)

                    # Add keyword
                    parsed_input_file.append(line)
    except NameError:
        sys.exit('ERROR - File was not found: {}'.format(input_file_name))

    return parsed_input_file, include_files, error_messages


def _get_all_associated_files(keywords):

    # Other files
    # Match lines of type:
    #    TYPE=RATIO, FILE=file, STEP=step, INC=inc, DRIVING ELSETS
    include_re_file = re.compile(r'^\s*\*\w.*file\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)

    for keyword in keywords:
        print(keyword)

    # Get all other files
    other_files = filter(include_re_file.search, keywords)
    for file in other_files:
        print("File:", file)
    # Check if include file exists
    missing_other_files = []

    if other_files:
        for other_file in other_files:
            if not os.path.isfile(os.path.abspath(other_file)):
                missing_other_files.append(other_file)
    if missing_other_files:
        print(' ERROR - Files are missing:')
        for file in missing_other_files:
            print("\t {}".format(file))
        print(' EXITING - Verify naming of files')

    if missing_other_files:
        sys.exit(1)

    return other_files


if __name__ == "__main__":
    """
    This is only for debugging
    """
    import fnmatch
    test_path = r'c://temp/jobber_submit_testdata2/'
    os.chdir(test_path)
    print(" Current directory content:", os.listdir(test_path))
    files = [os.path.join(test_path, file) for file in os.listdir(test_path) if fnmatch.fnmatch(file, '*.inp')]
    for file in files:
        print(" Input file:", file)
        print(facts(file))
