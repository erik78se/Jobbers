from pathlib import Path
import re

class SolveJob:
    """ Model for a abaqus Job for solver """
    def __init__(self,inp=None):
        self.jobname = None
        self.inpfile = inp # Inputfile for this job
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
        self.inpfile = inp # Inputfile for this job
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
        self.filename = filename
        self.restart_read = None
        self.restart_write = None
        self.eigenfreqency = None
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
    
    def __str__(self):
        return "Filename: {}\nRestartRead: {}\nRestartWrite: {}\nEigen: {}\nRandomeResp: {}\nInputs: {}\nOthers: {}".format(self.filename,
                                                                                                                            self.restart_read,
                                                                                                                            self.restart_write,
                                                                                                                            self.eigenfreqency,
                                                                                                                            self.random_response,
                                                                                                                            self.input_files,
                                                                                                                            self.other_files)

    def __repr__(self):
        return "<Inpfile: %s>" % str(self.filename)
