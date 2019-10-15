class FemfatJob:
    """ Model for a abaqus Job for solver """
    def __init__(self, ffjfile=None):
        self.jobname = None
        self.ffjfile = ffjfile
        self.template = None
        self.timelimit = ""
        self.scratch = '/tmp'
        self.memory = None
        self.femfat_licenses = {}
        self.femfat_module = {}
        self.nodes = None
        self.cpus = None
        self.ntasks_per_node = None
        self.partitions = []

    def __str__(self):
        return "FFJFile: {}\n".format(self.ffjfile)

    def __repr__(self):
        return "<Inpfile: %s>" % str(self.ffjfile)
