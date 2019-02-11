import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/

#
# Example implementation of inquirer in combination with jinja2
#

def process():
    """ Returns a rendered template, 
    based on questions from inquirer
    as a string to stdout """

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
                      exists=True
        ),
    ]
    answers = inquirer.prompt(questions)


    TEMPLATE_FILE = answers['template']

    with open(TEMPLATE_FILE) as file_:
        template = jinja2.Template(file_.read())
    
    outputText = template.render(answers=answers)  # this is where to put args to the template renderer

    return outputText
