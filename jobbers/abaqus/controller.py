import os
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
from pprint import pprint
import click
import jobbers
import jobbers.abaqus.inpfile as inpfile
from jobbers.abaqus.model import ( SolveJob, GenericJob)
from jobbers.abaqus.view import ( ask_generic_resources,
                                  ask_workflow,
                                  ask_submodel_odb,
                                  ask_abaqus_licenses,
                                  ask_inp,
			          ask_abaqus_module,
)


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
    """Processes questions and writes to file

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
        _workflow_solve(template,inp,output)
    elif wf == 'debug':
        _workflow_debug()
    elif wf == 'generic':
        _workflow_generic(template,output)
    else:
        print("Not implemented")
        raise("Not implemented")

def _workflow_solve(template,inp,output):
    """
    The solve workflow.
    """
    solvejob = SolveJob()
    if inp:
        solvejob.inputfile = inp
    else:
        solvejob.inputfile = ask_inp()['inpfile']

    ##################################
    ## Collect needed resources.
    ##################################
    solvejob.abaqus_module = ask_abaqus_module()

    solvejob.generic_resources = ask_generic_resources()
    
    solvejob.abaqus_licenses = ask_abaqus_licenses()
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    templates_dir=os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
        solvejob.template = template
    else:
        solvejob.template="{}/{}".format( templates_dir, 'abaqus-test-template.tmpl.j2' )

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
