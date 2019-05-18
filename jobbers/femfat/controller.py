import os
from pathlib import Path
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
import click
import jobbers
from jobbers.femfat.model import ( FemfatJob)
from jobbers.femfat.view import *
from jobbers import config


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('-t', '--template',
              required=False,
              type=click.Path(exists=True),
              help="Use custom jinja2 template.")
@click.option('-f', '--ffj',
              required=False,
              type=click.Path(exists=True),
              help="User supplied .ffj file for femfat")

def cli(output,template,ffj):
    """Processes questions and writes an script ready for slurm sbatch

    User can override default config in ~/.config/Jobbers/config.yaml
    it will take precedence over package defaults.

    Example usage: 

    # Output to stdout

    $ femtat-jobber  -

    # Output to myjob.job using my-template.j2

    $ femfat-jobber -t my-template.j2 myjob.job

    # Output to myjob.job using foobar.ffj as input .ffj-file and my-template.j2 as template

    $ femfat-jobber --template my-template.j2 --ffj foobar.ffj myjob.job
    """
    
    ###################################
    # Start state, which workflow?
    # <Debug> or <Run>
    ###################################
    wf = ask_workflow()['workflow']
    
    if wf == 'run':
        
        if not ffj:

            ffj = Path(ask_ffj()['ffjfile'])

        else:

            ffj = Path(ffj)
        
        _workflow_run(template,ffj,output)
            
    elif wf == 'debug':
        
        _workflow_debug()
        
    else:
        raise("Not implemented")

def _workflow_run(template,ffjfile,output):
    """
    The solve workflow.
    """

    femfatjob = FemfatJob(ffjfile)

    ##################################
    ## Collect needed resources.
    ##################################

    femfatjob.jobname = ask_jobname()['jobname']

    femfatjob.timelimit = 60 * int(ask_timelimit()['timelimit'])
    
    femfatjob.femfat_module = ask_femfat_module()

    femfatjob.cpus = ask_cpus_int()['cpus']

    femfatjob.partitions = ask_partitions()['partitions']
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir=os.path.join(os.path.dirname(jobbers.femfat.__file__), 'templates')
    
    if template:
        femfatjob.template = template
    else:
        femfat_template=config['femfat']['template'].get()
        femfatjob.template="{}/{}".format( templates_dir, femfat_template )

    _render_to_out(femfatjob,output)

        
def _workflow_debug():
    """ Help the user.
    """
    print("salloc -p debug -N 1")
    print("srun hostname")
    print("exit")

    
def _render_to_out(job,output):
    """ render job to a output file
    """
    with open(job.template) as file_:
    
        template = jinja2.Template(file_.read())

        o = template.render(job=job, template=job.template)
        
        output.write(o)

if __name__ == '__main__':
    cli()
