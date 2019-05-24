import subprocess
import json

def query_jobs_by_user(user_name):

    # Query SLURM for current jobs by user
    command = ['squeue', '-o', '"%A;%t;%j;%Z"', '-h', '-u', user_name]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        (std_out, std_err) = process.communicate(timeout=6)
    except subprocess.TimeoutExpired:
        print(" WARNING: SLURM is not responding...")
        return []

    # Convert byte string to string
    current_jobs = std_out.decode(errors='replace').strip().split("\n")

    job_array = list()
    if current_jobs != ['']:
        for job in current_jobs:
            job_id, job_state, job_name, job_dir = job.split(';')
            job_array.append([job_id, job_state, job_name, job_dir])
        return job_array
    else:
        return []


def query_jobs_by_user_json(user_name):
    # Query SLURM for current jobs by user
    command = ['squeue', '-o', '%all', '-u', user_name]
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=False,
                               universal_newlines=True)
    try:
        (std_out, std_err) = process.communicate(timeout=6)
    except subprocess.TimeoutExpired:
        print(" WARNING: SLURM is not responding...")
        return []

    # Convert byte string to string
    #current_jobs = std_out.decode(errors='replace').strip().split("\n")
    current_jobs = std_out.strip().split("\n")

    headers = current_jobs[0]
    current_jobs.pop(0)

    job_array = dict()
    if current_jobs != ['']:
        for job in current_jobs:
            current_job = dict()
            for header, value in zip(headers.split('|'), job.split('|')):
                current_job[header] = value
            jobid = current_job['JOBID']
            job_array[jobid]=current_job
        return json.dumps(job_array, indent=2)
    else:
        return ''


if __name__ == '__main__':
    """
    Test code for simple debugging of modules
    """
    from getpass import getuser

    print(f' Current user name "{getuser()}" ')
    jobs = query_jobs_by_user(getuser())
    for a_job in jobs:
        id_job, state, name, dir_job = a_job
        print(f' {id_job} - {state} - {name} - {dir_job}')

    entries = query_jobs_by_user_json(getuser())
    print(entries)
