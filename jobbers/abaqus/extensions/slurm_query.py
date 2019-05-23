import subprocess


def query_jobs_by_user(user_name):

    command = ['squeue', '-o', '"%A;%t;%j"', '-h', '-u', user_name]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        (std_out, std_err) = process.communicate(timeout=6)
    except subprocess.TimeoutExpired:
        print(" WARNING: SLURM is not responding...")
        return False

    # Convert byte string to string
    current_jobs = std_out.decode(errors='replace').split("\n")

    job_array = list()
    if current_jobs:
        for job in current_jobs:
            job_id, state, job_name = job.split(';')
            job_array.append([job_id, state, job_name])

    return job_array
