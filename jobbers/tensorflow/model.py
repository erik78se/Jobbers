from pathlib import Path
import re

class TensorJob:
    """ Model for a abaqus Job for solver """
    def __init__(self,ffjfile=None):
        self.jobname = None
        self.template = None
        self.timelimit = ""
        self.scratch = '/tmp'
        self.memory = None
        self.nodes = None
        self.cpus = None
        self.ntasks_per_node = None
        self.partitions = []
    
    def __str__(self):
        return "Jobname: {}\n".format(self.jobname)

    def __repr__(self):
        return "<TensorJob: %s>" % str(self.jobname)
