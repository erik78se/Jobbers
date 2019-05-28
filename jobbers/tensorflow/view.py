import os
import pathlib
from jobbers import config
import inquirer

def _list_pythonfiles(path=None):
    """ Returns a list of python files in a directory ( default: pwd) """
    if not path:
        path = pathlib.Path.cwd()

    tempfiles = list(path.glob('*.py'))

    inputfiles = []
    for item in tempfiles:
        if pathlib.Path.is_file(item):
            inputfiles.append(item)

    return inputfiles

def ask_jobname():
    """ Returns a dict with the answers for questions about jobname """

    questions = [
	inquirer.Text('jobname',
                      message="Name of job",
                      default='my-tensor-job'),
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

    print()

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

def ask_gpus():
    """ Returns a dict with the answers for questions about cpu """
    
    questions = [
        inquirer.List('gpus',
                      message="Needed GPUs",
                      choices=[1,2,4,8],),
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
                          ('Help for hebug session', 'debug'),
                          ('Run Tensorflow demo','run'),],
                      default='run'),
    ]

    return inquirer.prompt(questions)

def ask_python():
    """ Returns a dict with the answers """

    l = _list_pythonfiles()
    questions = None
    if not l:
        questions = [ inquirer.Path('pythonfile',
                        message="python input file (absolute path)",
                        path_type=inquirer.Path.FILE,
                        exists=True), ]
    else:
        questions = [ inquirer.List('pytonfile',
                      message=".py file to use (absolute path)",
                      choices=_list_pythonfiles()),
                        ]
    return inquirer.prompt(questions)

