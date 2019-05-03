#
# Class for representing SLURM resources
#
import inquirer
import os
import jobbers
import glob

def _list_inputfiles(path=None):
    """ Returns a list of inputfiles in a directory ( default: pwd) """
    if not path:
        path = os.getcwd()

    files = glob.glob(os.path.join(path, '*.inp'))
    
    return(glob.glob(os.path.join(path, '*.inp')))


def ask_generic_resources():
    """ Returns a dict with the answers for questions about generic resources """

    questions = [
	inquirer.Text('jobname',
                      message="Name of job",
                      default='my-job'),
        inquirer.Text('memory',
                      message="Max Memory needed (GB)",
                      validate=lambda _, x: 0 <= int(x) <= 1000,
                      default='10'),
        inquirer.List('cpus',
                      message="Needed cpus:",
                      choices=[1,2,4,8,16,24,32],),
       inquirer.Path('scratch',
                      message="Path to scratch file (path)",
                      path_type=inquirer.Path.DIRECTORY,
                      default="/cluster/scratch",
                      exists=False,),
        inquirer.Checkbox('partitions',
                          message="Use SLURM partitions",
                          choices=['partition1','partition2','default'],
                          default=['default'],),
        inquirer.List('timelimit',
                          message="Set timelimit (hours)",
                          choices=[1,2,3,4,5,6,7,8,12,24],
                          default=1,),
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

def ask_abaqus_module():
    """ Ask for abaqus lmod module """
    q = [ inquirer.List('module',
                        message="Select abaqus module",
                        choices=['abaqus/2018-2','abaqus/2019'],
                        default='abaqus/2018-2'),
          ]

    return inquirer.prompt(q)

