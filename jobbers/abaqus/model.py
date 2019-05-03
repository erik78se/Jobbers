class SolveJob:
    """ Model for a abaqus Job for solver """
    def __init__(self):
        self.inpfile = None # Inputfile for this job
        self.template = None
        self.generic_resources = {}
        self.abaqus_licenses = {}
        self.submodel_odb = {}

class GenericJob:
    """ Model for a generic job """
    def __init__(self):
        self.template = None
        self.script = None
        self.generic_resources = {}
