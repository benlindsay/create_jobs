#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from os import popen, mkdir
from os.path import join, isfile, isdir
import pandas as pd
import time
import string

def create_jobs(file_list=None, param_table=None, base_dir='.',
                table_sep='\s+', sub_file='sub.sh', sub_prog=None,
                sleep_time=0, submit=True):
    """
    Recursively generate the directory tree specified by values in files or
    functions from 'tier_list'. Copies the files in 'file_list' to each
    job directory and replaces all the variables with appropriate values
    """
    # Check variables
    if file_list is None:
        raise ValueError("No file_list provided")
    if param_table is None:
        raise ValueError("No param_table provided")
    if isinstance(param_table, pd.DataFrame):
        param_df = param_table
    elif isinstance(param_table, basestring):
        if isfile(param_table):
            param_df = pd.read_csv(param_table, sep=table_sep)
        else:
            raise ValueError("{} is not a valid file name!".format(param_table))
    elif isinstance(param_table, dict):
        param_df = pd.DataFrame(param_table)
    else:
        raise ValueError("param_table must be either a pandas DataFrame " +
                         "or a file name!")
    if sub_prog is None:
        sub_prog = _find_sub_prog()

    # Create JOB_NAME column if not already there
    if not 'JOB_NAME' in param_df.columns:
        param_df['JOB_NAME'] = param_df.index

    # Iterate over rows of dataframe, creating and submitting jobs
    param_dict_list = param_df.to_dict(orient='records')
    for param_dict in param_dict_list:
        job_dir = join(base_dir, str(param_dict['JOB_NAME']))
        if isdir(job_dir):
            print('{} already exists. Skipping.'.format(job_dir))
            continue
        else:
            mkdir(job_dir)
        _copy_and_replace_files(file_list, job_dir, param_dict)
        if submit:
            sub_file = _replace_vars(sub_file, param_dict)
            _submit_job(job_dir, sub_file, sleep_time, sub_prog)

def _find_sub_prog():
    """
    Returns the first job submission command found on the system.
    Currently, only qsub and sbatch are supported
    """
    possible_sub_prog_list = ['qsub', 'sbatch']
    for prog in possible_sub_prog_list:
        if popen('command -v ' + prog).read() != '':
            return prog
    raise ValueError("Could not find any of the following programs: {}",
                     possible_sub_prog_list)

def _copy_and_replace_files(file_list, job_dir, param_dict):
    """
    Given a list, `file_list`, whose members are either file paths or
    tuples like `('/path/to/from_file_name', 'to_file_name')` and job directory
    `job_dir`, copies the files to the job directory and replaces
    variables in those files and in the file names.
    """
    print("Copying files to {} and replacing vars".format(job_dir))
    for input_file in file_list:
        if isinstance(input_file, basestring):
            from_file = input_file
            to_file = join(job_dir, input_file)
        elif isinstance(input_file, tuple):
            from_file = input_file[0]
            to_file = join(job_dir, input_file[1])
        # Replace variables in file names, if any
        from_file = _replace_vars(from_file, param_dict)
        to_file = _replace_vars(to_file, param_dict)
        # Copy file to job_dir with variables in text of file replaced
        with open(from_file, 'r') as f_in, \
                open(to_file, 'w') as f_out:
            text = f_in.read()
            text = _replace_vars(text, param_dict)
            f_out.write(text)

def _replace_vars(text, param_dict):
    """
    Given a block of text, replace any instances of '{key}' with 'value'
    if param_dict contains 'key':'value' pair.
    This is done safely so that brackets in a file don't cause an error if
    they don't contain a variable we want to replace.
    See http://stackoverflow.com/a/17215533/2680824

    Examples:
        >>> _replace_vars('{last}, {first} {last}', {'first':'James', 'last':'Bond'})
        'Bond, James Bond'
        >>> _replace_vars('{last}, {first} {last}', {'last':'Bond'})
        'Bond, {first} Bond'
    """
    return string.Formatter().vformat(text, (), _Safe_Dict(param_dict))

class _Safe_Dict(dict):
    """
    Class with all the same functionality of a dictionary but if a key isn't
    present, it just returns '{key}'.
    This helps with _replace_vars().

    Examples:
        >>> d = _Safe_Dict({'last':'Bond'})
        >>> d['last']
        'Bond'
        >>> d['first']
        '{first}'
    """
    def __missing__(self, key):
        return '{' + key + '}'

def _submit_job(job_dir, sub_file, sleep_time, sub_prog):
    """
    Submit 'sub_file' in 'job_dir' using submission program 'sub_prog'.
    Wait 'sleep_time' seconds between each submission.
    """
    print("submitting {}".format(join(job_dir, sub_file)))
    popen('cd ' + job_dir + '; ' + sub_prog + ' ' + sub_file + '; cd -')
    if sleep_time > 0:
        time.sleep(sleep_time)
