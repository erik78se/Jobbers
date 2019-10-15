import math


def calculate_abaqus_licenses(cores):
    """
    This function calculates the number of Abaqus licenses
    needed by the job. The standard formula is 5*N^0.422,
    where N is the number of cores.
    # TODO:    Extend with other license models (i.e model=light).
    """
    return int(5 * math.pow(cores, 0.422))
