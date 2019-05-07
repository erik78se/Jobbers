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
