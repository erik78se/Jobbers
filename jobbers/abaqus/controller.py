import os
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
from pprint import pprint
import click
import jobbers
import jobbers.abaqus.inpfile as inpfile
from jobbers.abaqus.model import SolveJob
from jobbers.abaqus.view import ( ask_generic_resources,
                                  ask_jobclass_input,
                                  ask_submodel_odb,
                                  ask_abaqus_licenses, )


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('-t', '--template',
              required=False,
              type=click.Path(exists=True),
              help="Use custom jinja2 template.")
def cli(output,template):
    """Processes questions and writes to file

    Example: abaqus -t templatet.j2 -

    Example: abaqus -t templatet.j2 myjob.job

    """
    
    ###################################
    # Start state, which workflow?
    # <Debug> or <Generic> or <Solve>
    ###################################

    solvejob = SolveJob()
    
    solvejob.abaqus_jobclass = ask_jobclass_input()
    
    if solvejob.abaqus_jobclass['jobclass'] == 'solve':
        # Try gather information from inp file.
        f = inpfile.facts()
        
        print(f)
        
        if f['submodel']:

            solvejob.submodel_odb = ask_submodel_odb()
            
        else:
            
            submodel_odb = None

    else:
        
        print("Not implemented")
            

    ##################################
    ## Collect needed resources.
    ##################################

    solvejob.generic_resources = ask_generic_resources()
    
    solvejob.abaqus_licenses = ask_abaqus_licenses()
    
    ##########################################
    # Info gathered, dispatch to job rendering
    ##########################################

    # print(solvejob.generic_resources)

    templates_dir=os.path.join(os.path.dirname(jobbers.abaqus.__file__), 'templates')

    if template:
    
        TEMPLATE_FILE = template

    else:

        TEMPLATE_FILE="{}/{}".format( templates_dir, 'abaqus-test-template.tmpl.j2' )

    with open(TEMPLATE_FILE) as file_:

        template = jinja2.Template(file_.read())
        
        outputText = template.render(job=solvejob, template=TEMPLATE_FILE)

        output.write(outputText)
        
if __name__ == '__main__':
    cli()
