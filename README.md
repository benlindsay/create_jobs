# create_jobs

A tool to facilitate creating a bunch of compute jobs

## What this tool does

If you use either PBS or SLURM and you want to run a series of jobs that are very similar but differ in 1 or more parameter values or input files, this tool could help.

## Installation

Install using `pip install create_jobs`. Click [here](https://pypi.python.org/pypi/create_jobs) to view this on the Python Package Index site. If you don't have `pip` on your computer, then [download Anaconda](https://www.continuum.io/downloads). You don't need root permissions. If you're on Linux, the download will give you a `bash` script that you just run using something like `bash Anaconda2-2.4.0-Linux-x86_64.sh`. This will give you a python distribution that includes `pip`.

## Usage

This tool operates on the concept of input files, a job submission file, and a table of parameters for each job. The table can be provided as either a pandas DataFrame, a Python dictionary, or tabular file (anything that `pandas.read_csv()` can read works). There is no limit to the number of input files you can have, and no default name for input files. The default name for job submission files is `sub.sh`.
