from os import path
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
import click
import jobbers.jobber

#
# Example implementation of inquirer in combination with jinja2
#

def process(in_template):
    """ Returns a rendered template (may be provided as argument),
    based on questions from inquirer as a string to stdout """

    # Templates relative to the package
    templates_dir=path.join(path.dirname(jobbers.jobber.__file__), 'templates')

    if not in_template:
        in_template = "{}/{}".format( templates_dir, "echo.j2" )

    ### Ask questions
    questions = [
        inquirer.Checkbox('interests',
                          message="What are you interested in?",
                          choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
                          default='Computers'
        ),
        inquirer.Path('template',
                      message="Which template shall be used?",
                      path_type=inquirer.Path.FILE,
                      exists=True,
                      default=in_template),
    ]
    answers = inquirer.prompt(questions)


    TEMPLATE_FILE = answers['template']

    with open(TEMPLATE_FILE) as file_:
        template = jinja2.Template(file_.read())
    
    outputText = template.render(answers=answers)  # this is where to put args to the template renderer

    return outputText


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('-t', '--template',
              required=False,
              type=click.Path(exists=True),
              help="Use custom jinja2 template.")
def cli(output,template):
    """Processes questions and writes to file                                                                                                       

    Example: jobber -t templatet.j2 -                                                                                                               

    Example: jobber -t templatet.j2 myjob.job

    """
    rendered_template = process(template)
    output.write(rendered_template)

if __name__ == '__main__':
    cli()
