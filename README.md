# create_jobs

A tool to facilitate creating a bunch of compute jobs

## What this tool does

If you use either PBS or SLURM and you want to run a series of jobs that are very similar but differ in 1 or more parameter values or input files, this tool could help.

## Installation

Install using `pip install create_jobs`. Click [here](https://pypi.python.org/pypi/create_jobs) to view this on the Python Package Index site. If you don't have `pip` on your computer, then [download Anaconda](https://www.continuum.io/downloads). You don't need root permissions. If you're on Linux, the download will give you a `bash` script that you just run using something like `bash Anaconda2-2.4.0-Linux-x86_64.sh`. This will give you a python distribution that includes `pip`.

If you're in the Riggleman lab and using our research cluster (`rrlogin`), then I already have the Anaconda install script ready to go. You just need to run `bash /opt/share/lindsb/Anaconda3-4.4.0-Linux-x86_64.sh`. Make sure to let it add the line to alter your `PATH` in `.bashrc`, then source your `.bashrc` file with `source .bashrc`. Then you can type `pip install create_jobs`.

## Basic Usage

This tool operates on the concept of input files, a job submission file, and a table of parameters for each job. The table is just a space-separated text file with columns representing variables and rows representing simulations.

Here's a sample workflow. Let's say I have some simulation code that reads a file called `bcp.input`, which specifies a nanorod length, and other input parameters. I want to generate 3 folders, each of which will run a simulation with a different nanorod length. My `bcp.input` file looks something like this:

```
1000        # Number of iterations
60          # Polymer length
1           # Nanorod radius
{NRLENGTH}  # Nanorod length
```

Note that I put a variable `NRLENGTH` inside brackets `{}`. You can have as many variables like this in as many input files as you want as well as your submission script. My submission script, `sub.sh`, looks something like this:

```
#!/bin/sh
#PBS -N {JOB_NAME}
#PBS -l nodes=1:ppn=1
#PBS -l walltime=01:00:00,mem=2gb

cd $PBS_O_WORKDIR

# Run code that happens to look for bcp.input in the current directory
mpirun $HOME/code/awesome_code.exe
```

I put the variable `JOB_NAME` in brackets here too, so that each simulation will have a unique name when examining your jobs with something like `qstat` or `squeue`. (Note: `JOB_NAME` is a special variable. More on that in the next section.) Finally, I need to make a file that contains a space-separated table where each row represents a simulation and each column represents a variable. I'll call it `trials.txt`. Here's what it looks like:

```
JOB_NAME    NRLENGTH
lnr-4       4
lnr-5       5
lnr-6       6
```

With those files in place, I just need to call `create_jobs` and pass those files as arguments. The command looks like this:

```
$ create_jobs -i bcp.input -s sub.sh -t trials.txt
Copying files to ./lnr-4 and replacing vars
submitting ./lnr-4/sub.sh
3719921.rrlogin.internal
Copying files to ./lnr-5 and replacing vars
submitting ./lnr-5/sub.sh
3719922.rrlogin.internal
Copying files to ./lnr-6 and replacing vars
submitting ./lnr-6/sub.sh
3719923.rrlogin.internal
```

## `JOB_NAME` Variable

The `JOB_NAME` variable is actually a special variable that determines the name of the simulation folder. It is generated automatically if not provided in the table (`trials.txt` in this case). If it's not provided, the `JOB_NAME` column will be internally created by copying the first column it sees with unique values for each row. So in this case, we could simply use the following for `trials.txt`:

```
NRLENGTH
4
5
6
```

and the simulation folders would just be `4`, `5`, and `6`. `{JOB_NAME}` in `sub.sh` would also be replaced with either `4`, `5`, or `6` in each simulation folder.

## Make use of defaults

The default submission script name and parameter table file names looked for with this tool are `sub.sh` and `trials.txt`, respectively. So if you happen to be using those file names for your templates, you can simply type `create_jobs -i bcp.input` and skip the `-s` and `-t` flags.

## Other Notes

1. You can put as many input files as you want after the `-i` flag.
2. If you want to generate all the folders and files but not submit the jobs as a dry-run, you can add the `-n` flag to your command.
3. This tool can be used to help generate some more complex workflows as well, like including changing file names when they're copied like including variables within input file names. I haven't added documentation for those capabilities, but email me or raise an issue if you'd like to know how to use them.
