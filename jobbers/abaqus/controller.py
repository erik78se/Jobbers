import os
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
from pprint import pprint
import click
import jobbers
from jobbers.abaqus.inpfileparse import traverse
from jobbers.abaqus.licenser import calculate_abaqus_licenses
from jobbers.abaqus.model import ( SolveJob, GenericJob, Inpfile)
from jobbers.abaqus.view import *
from jobbers import config


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('-t', '--template',
              required=False,
              type=click.Path(exists=True),
              help="Use custom jinja2 template.")
@click.option('-i', '--inp',
              required=False,
              type=click.Path(exists=True),
              help="User supplied .inp file for abaqus")
def cli(output,template,inp):
    """Processes questions and writes an abaqus slurm to file

    User can override default config in ~/.config/Jobbers/config.yaml
    it will take precedence over package defaults.

    Example usage: 

    # Output to stdout

    $ abaqus-jobber  -

    # Output to myjob.job using my-template.j2

    $ abaqus-jobber -t my-template.j2 myjob.job

    # Output to myjob.job using solve.inp as inpfile and my-template.j2 as template

    $ abaqus-jobber -t my-template.j2 -i solve.inp myjob.job
    """
    
    ###################################
    # Start state, which workflow?
    # <Debug> or <Generic> or <Solve>
    ###################################
    wf = ask_workflow()['workflow']
    
    if wf == 'solve':

        # Collect "no such file"
        no_such_files = []
        
        if not inp:
            inp = ask_inp()['inpfile']

        inpFile = Inpfile(filename=inp)

        input_deck = traverse(inpFile)

        # Visualize missing files
        for i in input_deck:
            if not i.file.is_file():
                print("--- Unable to locate from input file (No such file?) ---")
                print(i)
                no_such_files.append(i)
        
        # If eigenfrequency == False then We can run with MPI.
        if not input_deck[0].eigenfrequency:   

            _workflow_solve_parallel(template,inpFile,output)
            
        else:
            
            _workflow_solve(template,inpFile,output)
            
    elif wf == 'debug':
        
        _workflow_debug()
        
    elif wf == 'generic':
        
        _workflow_generic(template,output)
        
    else:
        raise("Not implemented")

def _workflow_solve(template,inpfile,output):
    """
    The solve workflow.
    """
    solvejob = SolveJob(inpfile)

    ##################################
    ## Collect needed resources.
    ##################################
    solvejob.abaqus_module = ask_abaqus_module()

    solvejob.cpus = ask_cpus_int()['cpus']

    lics_needed = calculate_abaqus_licenses( solvejob.cpus )
    
    solvejob.abaqus_licenses = ask_abaqus_licenses()

    solvejob.partitions = ask_partitions()['partitions']
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir=os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')
    
    if template:
        solvejob.template = template
    else:
        solve_template=config['abaqus']['solve_template'].get()
        solvejob.template="{}/{}".format( templates_dir, solve_template )

    _render_to_out(solvejob,output)


def _workflow_solve_parallel(template,inpfile,output):
    """
    The solve-parallel sub workflow.
    """
    solvejob = SolveJob(inpfile)

    # If job is a restart read job, ask for restart files.
    if solvejob.inpfile.restart_read:
        solvejob.restartfile = ask_restart()

    ##################################
    ## Collect needed resources.
    ##################################
    solvejob.abaqus_module = ask_abaqus_module()

    solvejob.jobname = ask_jobname()['jobname']
    
    solvejob.nodes = ask_nodes()['nodes']

    solvejob.ntasks_per_node = 36  # We guess that cores =36 based on cluster sizes
    
    solvejob.cpus = int(solvejob.nodes * solvejob.ntasks_per_node)

    lics_needed = calculate_abaqus_licenses( solvejob.cpus )
    
    # solvejob.abaqus_licenses = ask_abaqus_licenses_parallel()

    solvejob.abaqus_licenses = { 'license': 'abaqus@flex_host', 'volume': lics_needed }

    solvejob.scratch = ask_scratch()['scratch']
    
    solvejob.partitions = ask_partitions()['partitions']

    solvejob.timelimit = int(ask_timelimit()['timelimit'])*60
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir = os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
        solvejob.template = template
    else:
        solve_par_template=config['abaqus']['solve_parallel_template'].get()
        solvejob.template="{}/{}".format( templates_dir, str(solve_par_template) )

    _render_to_out(solvejob,output)
    

def _workflow_generic(template,output):
    genericjob = GenericJob()
    genericjob.generic_resources = ask_generic_resources()

    templates_dir=os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
        genericjob.template = template
    else:
        genericjob.template="{}/{}".format( templates_dir, 'abaqus-generic-template.j2' )

    _render_to_out(genericjob,output)


        
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
