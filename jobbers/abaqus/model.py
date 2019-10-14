from pathlib import Path
import re
import os


class SolveJob:
    """ Model for a abaqus Job for solver """

    def __init__(self, inp=None):
        self.jobname = None
        # self.inpfili = Inpfile(filename=str(inp.file))  # Inputfile for this job
        # TODO: Reflect - should not reconstruct the inputfile, right?!
        self.inpfile = inp  # Inputfile for this job
        self.template = None
        self.timelimit = ""
        self.scratch = "/tmp"
        self.memory = None
        self.abaqus_licenses = {}
        self.submodel_odb = {}
        self.abaqus_module = {}
        self.nodes = None
        self.cpus = None
        self.gpus = None
        self.ntasks_per_node = None
        self.partitions = []


class GenericJob:
    """ Model for a generic job """

    def __init__(self, inp=None):
        self.jobname = None
        self.inpfile = inp  # Inputfile for this job
        self.template = None
        self.timelimit = ""
        self.scratch = "/tmp"
        self.memory = None
        self.abaqus_licenses = {}
        self.submodel_odb = {}
        self.abaqus_module = {}
        self.nodes = None
        self.cpus = None
        self.ntasks_per_node = None
        self.partitions = []
        self.restartjobname = None


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
        self.restart_files = []
        self.restart_file = None

        # input regexp
        self.input_regexp = re.compile(
            r"^\s*\*\w.*input\s*=\s*([\w\./-]+)\s*$", re.IGNORECASE
        )
        # restart read
        self._restart_read_regexp = re.compile(r"^\s*\*restart\s*.*read", re.IGNORECASE)
        # restart write
        self._restart_write_regexp = re.compile(
            r"^\s*\*restart\s*.*write", re.IGNORECASE
        )
        # eigenfrequency
        self._eigen_regexp = re.compile(r"^\s*\*FREQUENCY\s*", re.IGNORECASE)
        # random response
        self._random_re = re.compile(r"^\s\*RANDOM\s*.*RESPONSE", re.IGNORECASE)

    def files_to_stage(self):
        """
        Used to return all files required to run the job
        :return: List of required files, including restart files.
        """
        files_to_stage_up = list()

        # Append input file (self.file is a PosixPath)
        files_to_stage_up.append(str(self.file))

        # Append include files
        for file in self.input_files:
            # TODO: the input_files are also Inpfiles. should really abspath be done here?
            # files_to_stage_up.append(os.path.abspath(str(file.file)))
            files_to_stage_up.extend(file.files_to_stage())

        # Append other files
        for file in self.other_files:
            files_to_stage_up.append(file)

        # Append restart files
        if self.restart_file:
            self.__get_restart_files__()
            files_to_stage_up.extend(self.restart_files)

        return files_to_stage_up

    def __get_restart_files__(self):
        """
        TODO: write
        """
        self.restart_files = []

        for ext in [
            ".res",
            ".stt",
            ".prt",
            ".mdl",
            ".abq",
            ".sel",
            ".pac",
            ".odb",
            ".sim",
        ]:
            if os.path.isfile(self.restart_file + ext):
                self.restart_files.append(os.path.abspath(self.restart_file + ext))

    def __str__(self):
        return (
            "Filename: {}\n"
            "RestartRead: {}\n"
            "RestartWrite: {}\n"
            "Eigen: {}\n"
            "RandomeResp: {}\n"
            "Inputs: {}\n"
            "Others: {}".format(
                self.file,
                self.restart_read,
                self.restart_write,
                self.eigenfrequency,
                self.random_response,
                self.input_files,
                self.other_files,
            )
        )

    def __repr__(self):
        return "<Inpfile: %s>" % str(self.file)
