#
# Class for representing SLURM resources
#
import inquirer
import os
import jobbers
import glob
from jobbers import config

def _list_inputfiles(path=None):
    """ Returns a list of inputfiles in a directory ( default: pwd) """
    if not path:
        path = os.getcwd()

    inputfiles = glob.glob(os.path.join(path, '*.inp'))
    
    return inputfiles


def ask_jobname():
    """ Returns a dict with the answers for questions about jobname """

    questions = [
        inquirer.Text('jobname',
                      message="Name of job",
                      default='my-job'),
    ]

    return inquirer.prompt(questions)


def ask_memory():
    """ Memory """
    questions = [
        inquirer.Text('memory',
                      message="Max Memory needed (GB)",
                      validate=lambda _, x: 0 <= int(x) <= 1000,
                      default='10'),
        ]

    return inquirer.prompt(questions)


def ask_scratch():
    """ scratch """

    questions = [
        inquirer.Path('scratch',
                      message="Path to shared scratch directory (absolute path)",
                      path_type=inquirer.Path.DIRECTORY,
                      default=config['slurm']['shared_scratch'].get(),
                      exists=False,),
    ]

    return inquirer.prompt(questions)

def ask_timelimit():
    """ Returns a dict with the answers for questions about timelimit """
    questions = [
        inquirer.List('timelimit',
                          message="Set timelimit (hours)",
                          choices=[1,2,3,4,5,6,7,8,12,24],
                          default=1,),
    ]
    
    return inquirer.prompt(questions)


def ask_partitions():
    """ Returns a dict with the answers for questions about SLURM partitions """

    questions = [
        inquirer.Checkbox('partitions',
                          message="Use SLURM partitions",
                          choices=config['slurm']['partitions'].get(),
                          default=config['slurm']['default_partition'].get()) ]
    return inquirer.prompt(questions)


def ask_cpus_int():
    """ Returns a dict with the answers for questions about cpu """
    
    questions = [
        inquirer.List('cpus',
                      message="Needed cpus",
                      choices=[1,2,4,8,16,32,64],),
    ]
    
    return inquirer.prompt(questions)


def ask_nodes():
    """ Returns a dict with the answers for questions about nodes """
    
    questions = [
        inquirer.List('nodes',
                      message="Max nodes:",
                      choices=[1,2,3],
                      default=2),
    ]
    
    return inquirer.prompt(questions)


def ask_workflow():
    """ Returns a dict with the answers """

    questions = [

        inquirer.List('workflow',
                      message="What do you want to do?",
                      choices=[
                          ('Debug session', 'debug'),
                          ('Generic script submission','generic'),
                          ('Solve problem','solve'),],
                      default='solve'),

        # inquirer.Path('inputfile',
        #               message="Input file (absolute path)",
        #               path_type=inquirer.Path.FILE,
        #               exists=True,
        #               default=next(iter(_list_inputfiles()), None )),
    ]

    return inquirer.prompt(questions)


def ask_inp():
    """ Returns a dict with the answers """

    questions = [
        inquirer.Path('inpfile',
                      message=".inp file to use (absolute path)",
                      path_type=inquirer.Path.FILE,
                      exists=True,
                      default=next(iter(_list_inputfiles()), None )),
    ]

    return inquirer.prompt(questions)


def ask_submodel_odb():
    """ Ask for the supplementary ODB file used by a restart """
    q = [ inquirer.Path('filename',
                        message="Path to submodel ODB file (absolute)",
                        path_type=inquirer.Path.FILE,
                        default='submodel.odb',
                        exists=False), ]
    
    return inquirer.prompt(q)


def ask_abaqus_licenses():
    """ Ask for abaqus licenses """
    q = [ inquirer.List('license',
                        message="Select license",
                        choices=['abaqus@flex_host'],
                        default='abaqus@flex_host'),
          inquirer.Text('volume',
                        message="How many licenses of {license}",
                        validate=lambda _, x: 0 <= int(x) <= 1000,
                        default='30'),
          ]
          
    return inquirer.prompt(q)


def ask_abaqus_licenses_parallel(default_volume):
    """ Ask for abaqus licenses in multiples of max(node-cpus) """

    
    q = [ inquirer.List('license',
                        message="Select license",
                        choices=['abaqus@flex_host'],
                        default='abaqus@flex_host'),
          inquirer.List('volume',
                        message="How many licenses of {license}",
                        choices=[36,72,108],
                        default=72),
    ]
          
    return inquirer.prompt(q)


def ask_abaqus_module():
    """ Ask for abaqus lmod module """
    m = config['abaqus']['envmodules'].get()
    q = [inquirer.List('module',
                        message="Select abaqus module",
                        choices=m,
                        default=m[0] ),
          ]

    return inquirer.prompt(q)
