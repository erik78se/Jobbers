import os
import click
import jobbers
import confuse
from jobbers.abaqus.inpfileparse import traverse
from jobbers.abaqus.licenser import calculate_abaqus_licenses
from jobbers.abaqus.model import ( SolveJob, GenericJob, Inpfile)
from jobbers.abaqus.view import *
from jobbers import config
from jobbers.templating import render_to_out

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

    render_to_out(solvejob,output)


def _workflow_solve_parallel(template,inpfile,output):
    """
    The solve-parallel sub workflow.
    """
    solvejob = SolveJob(inpfile)

    # If job is a restart read job, ask for restart files.
    if inpfile.restart_read:
        restartfile = ask_restart()
        solvejob.restartjobname = os.path.splitext(os.path.basename(str(restartfile)))[0]
        solvejob.inpfile.restart_file = solvejob.restartjobname

    ##################################
    ## Collect needed resources.
    ##################################
    solvejob.abaqus_module = ask_abaqus_module()

    solvejob.jobname = ask_jobname(solvejob.inpfile.file.stem)['jobname']
    
    solvejob.nodes = ask_nodes()['nodes']

    # TODO: This should not be hardcoded here. Cluster config?
    solvejob.ntasks_per_node = 36  # We guess that cores =36 based on cluster sizes
    
    solvejob.cpus = int(solvejob.nodes * solvejob.ntasks_per_node)

    lics_needed = calculate_abaqus_licenses(solvejob.cpus)
    
    # solvejob.abaqus_licenses = ask_abaqus_licenses_parallel()

    solvejob.abaqus_licenses = { 'license': 'abaqus@flex_host', 'volume': lics_needed }

    # 20190521: Do not ask for scratch at the moment, go with config default /jhacxc
    # solvejob.scratch = ask_scratch()['scratch']
    #try:
    #if config['slurm']['shared_scratch'].get():
    solvejob.scratch = config['slurm']['shared_scratch'].get()
    #except NotFoundError:
    #    solvejob.scratch = ask_scratch()['scratch']
   
    # 20190521: Do not ask for partitions at the moment, go with config defaults /jhacxc
    # solvejob.partitions = ask_partitions()['partitions']
#    if config['slurm']['default_partition'].get():
    solvejob.partitions.append(config['slurm']['default_partition'].get())
#    else:
#        solvejob.partitions = ask_partitions()['partitions']

    solvejob.timelimit = int(ask_timelimit()['timelimit'])*60

    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir = os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
        solvejob.template = template
    else:
        solve_par_template = config['abaqus']['solve_distributed_template'].get()
        # solvejob.template = "{}/{}".format(templates_dir, str(solve_par_template))
        solvejob.template = str(pathlib.Path(templates_dir, solve_par_template))

    render_to_out(solvejob, output)
    

def _workflow_generic(template, output):
    genericjob = GenericJob()
    genericjob.generic_resources = ask_generic_resources()

    templates_dir=os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
        genericjob.template = template
    else:
        genericjob.template="{}/{}".format( templates_dir, 'abaqus-generic-template.j2' )

    render_to_out(genericjob,output)


        
def _workflow_debug():
    """ Help the user.
    """
    print("salloc -p debug -N 1")
    print("srun hostname")
    print("exit")

if __name__ == '__main__':
    cli()
