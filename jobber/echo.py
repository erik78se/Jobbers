#!/usr/bin/env python
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/

### Ask questions

questions = [
      inquirer.Checkbox('interests',
                    message="What are you interested in?",
                    choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
      ),
    ]
answers = inquirer.prompt(questions)

### Render using template
templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "echo.j2"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(answers=answers)  # this is where to put args to the template renderer

### Just dump to out
print(outputText)

