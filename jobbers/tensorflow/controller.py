import os
from pathlib import Path
import click
from jobbers.templating import render_to_out
from jobbers.tensorflow.model import ( TensorJob)
from jobbers.tensorflow.view import *
import jobbers
from jobbers import config


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('-t', '--template',
              required=False,
              type=click.Path(exists=True),
              help="Use custom jinja2 template.")

def cli(output,template):
    """Processes questions and writes an script ready for slurm sbatch

    User can override default config in ~/.config/Jobbers/config.yaml
    it will take precedence over package defaults.

    Example usage: 

    # Output to stdout

    $ tensor-jobber  -

    # Output to myjob.job using my-template.j2

    $ tensor-jobber -t my-template.j1 myjob.job

    # Output to myjob.job using foobar.ffj as input .ffj-file and my-template.j2 as template

    $ tensor-jobber --template my-template.j2 --ffj foobar.ffj myjob.job
    """
    
    ###################################
    # Start state, which workflow?
    # <Debug> or <Run>
    ###################################
    wf = ask_workflow()['workflow']
    
    if wf == 'run':
        
        _workflow_run(template,output)
            
    elif wf == 'debug':
        
        _workflow_debug()
        
    else:
        raise("Not implemented")

def _workflow_run(template,output):
    """
    The solve workflow.
    """

    tensorjob = TensorJob()

    ##################################
    ## Collect needed resources.
    ##################################

    tensorjob.jobname = ask_jobname()['jobname']

    tensorjob.timelimit = 60 * int(ask_timelimit()['timelimit'])
    
    tensorjob.gpus = ask_gpus()['gpus']

    tensorjob.partitions = ask_partitions()['partitions']
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir=os.path.join(os.path.dirname(jobbers.tensorflow.__file__), 'templates')
    
    if template:
        tensorjob.template = template
    else:
        tensor_template=config['tensorflow']['template'].get()
        tensorjob.template="{}/{}".format( templates_dir, tensor_template )

    render_to_out(tensorjob,output)

        
def _workflow_debug():
    """ Help the user.
    """
    print("salloc -p debug -N 1")
    print("srun hostname")
    print("exit")


if __name__ == '__main__':
    cli()
