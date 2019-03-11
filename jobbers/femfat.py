from os import path
import os
import glob
import inquirer  # https://pypi.org/project/inquirer/
import jinja2    # http://jinja.pocoo.org/docs/2.10/
import jobbers.femfat

#
# Example implementation of inquirer in combination with jinja2
#

def process():
    """ Returns a rendered template, 
    based on questions from inquirer
    as a string to stdout """

    # Templates relative to the package
    templates_dir=path.join(path.dirname(jobbers.femfat.__file__), 'templates')
    template_files = glob.glob(os.path.join(templates_dir, 'femfat_*.j2'))

    #clusters = { 'partition1': 36, 'partition2': 20 }
    versions = [ '5.3.1', '5.3', '5.2b', '5.2a', '5.2' ]

    inifile = 'femfat.ini'

    #def get_cores(partition):
    #    node_cores = int(clusters.get(partition))
        #cores = node_cores * nodes

    #    return node_cores

    def get_inputfile(path, ext):
        inputfiles = []
        for file in os.listdir(path):
            if file.endswith(ext):
                inputfiles.append(os.path.join(path, file))

        return inputfiles


    current_dir = os.getcwd()
    inputfiles = get_inputfile(current_dir,'.ffj')


    ### Ask questions
    questions = [
        inquirer.List('versions',
                message="What Femfat version to use?",
                choices=versions,
                default='5.3',
        ),
        inquirer.List('inputfiles',
                message="Choose inputfile",
                choices=inputfiles,
        ),
        inquirer.List('template',
                 message="Which template shall be used?",
                 choices = template_files,
        ),
        inquirer.Confirm('starttime',
                 message="Do you want to set a starttime?",
                 default=False,
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers.get("starttime") == True:
        if 'slurm' in answers.get("template"):
            workloader = [
                    inquirer.Text('start',
                    message="YYYY-MM-DD[THH:MM[:SS]], E.g. 2019-05-20T19:30:00?",
                    ),
            ]
            workload_answers = inquirer.prompt(workloader)
            start = '#SBATCH --begin=' + workload_answers["start"]

        if 'lsf' in answers.get("template"):
            workloader = [
                    inquirer.Text('start',
                    message="[[year:][month:]day:]hour:minute?",
                    ),
            ]
            workload_answers = inquirer.prompt(workloader)
            start = '#BSUB -b ' + workload_answers["start"]
    else:
        start = ''


    version = answers.get("versions")
    jobname = answers.get("inputfiles")
    inputfile = os.path.basename(jobname)
    jobname = os.path.splitext(inputfile)[0]
    #partition = answers.get("partitions")
    #node_cores = get_cores(partition)

    # Check for existing femfat.ini file
    # and ask if overwrite the file

    if os.path.isfile(inifile):
        overwrite_file = [
            inquirer.Confirm('overwrite',
                message="Do you want to overwrite existing {} file?".format(inifile),
                default=False,
        ),
        ]
        overwrite_ini = inquirer.prompt(overwrite_file)
        overwrite = overwrite_ini.get('overwrite')
    else:
        overwrite = 'True'

    if overwrite:
        template_ini = glob.glob(os.path.join(templates_dir, 'femfat.ini.j2'))
        template_ini = ''.join(template_ini)

        with open(template_ini) as file_:
            template = jinja2.Template(file_.read())
        femini = template.render(version=version)
        try:
            f = open(inifile, 'w')
            f.write(femini)
            f.close()
        except:
            print('Error writing file {}'.format(inifile))


    TEMPLATE_FILE = answers['template']

    with open(TEMPLATE_FILE) as file_:
        template = jinja2.Template(file_.read())
    
    #outputText = template.render(answers=answers, version=version, inputfile=inputfile, jobname=jobname, partition=partition, node_cores=node_cores)  # this is where to put args to the template renderer
    outputText = template.render(answers=answers, version=version, inputfile=inputfile, jobname=jobname, start=start)  # this is where to put args to the template renderer

    try:
        f = open('{}.job'.format(jobname), 'w')
        f.write(outputText)
        f.close()
    except:
        print('Error writing jobfile!')

    return outputText
