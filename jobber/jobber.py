import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/

def process():
    """ Returns the processed workflow as a string """

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
