from pathlib import Path
import re


class SolveJob:
    """ Model for a abaqus Job for solver """
    def __init__(self,inp=None):
        self.jobname = None
        self.inpfile = Inpfile(filename=str(inp.file))  # Inputfile for this job
        self.template = None
        self.timelimit = ""
        self.scratch = '/tmp'
        self.memory = None
        self.abaqus_licenses = {}
        self.submodel_odb = {}
        self.abaqus_module = {}
        self.nodes = None
        self.cpus = None
        self.ntasks_per_node = None
        self.partitions = []


class GenericJob:
    """ Model for a generic job """
    def __init__(self):
        self.jobname = None
        self.inpfile = inp  # Inputfile for this job
        self.template = None
        self.timelimit = ""
        self.scratch = '/tmp'
        self.memory = None
        self.abaqus_licenses = {}
        self.submodel_odb = {}
        self.abaqus_module = {}
        self.nodes = None
        self.cpus = None
        self.ntasks_per_node = None
        self.partitions = []


class Inpfile:
    """ Model for an .inp files """
    def __init__(self, filename=None):
        self.file = Path(filename)
        self.restart_read = None
        self.restart_write = None
        self.eigenfrequency = None
        self.random_response = None
        self.input_files = []
        self.other_files = []

        # input regexp
        self.input_regexp = re.compile(r'^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$', re.IGNORECASE)
        # restart read
        self._restart_read_regexp = re.compile(r'^\s*\*restart\s*.*read', re.IGNORECASE)
        # restart write
        self._restart_write_regexp = re.compile(r'^\s*\*restart\s*.*write', re.IGNORECASE)
        # eigenfrequency
        self._eigen_regexp = re.compile(r'^\s*\*FREQUENCY\s*', re.IGNORECASE)
        # random response
        self._random_re = re.compile(r'^\s\*RANDOM\s*.*RESPONSE', re.IGNORECASE)

    def files_to_stage(self):
        """
        Used to return all files required to run the job
        :return: List of required files, excluding restart files.
        """
        files_to_stage_up = list()

        # Append input file
        files_to_stage_up.append(self.file)

        # Append include files
        for file in self.input_files:
            files_to_stage_up.append(file)

        # Append include files
        for file in self.other_files:
            files_to_stage_up.append(file)

        return files_to_stage_up

    def __str__(self):
        return "Filename: {}\n" \
               "RestartRead: {}\n" \
               "RestartWrite: {}\n" \
               "Eigen: {}\n" \
               "RandomeResp: {}\n" \
               "Inputs: {}\n" \
               "Others: {}".format(self.file,
                                   self.restart_read,
                                   self.restart_write,
                                   self.eigenfrequency,
                                   self.random_response,
                                   self.input_files,
                                   self.other_files)

    def __repr__(self):
        return "<Inpfile: %s>" % str(self.file)
