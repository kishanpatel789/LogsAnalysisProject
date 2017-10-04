# Logs Analysis Project
This repository highlights an internal reporting tool that uses information from a newspaper database to discover what kind of articles the site's readers like. The questions of interest are the following:
1. What are the three most popular articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements
- [Python 2.7.3](https://www.python.org/download/releases/2.7.3/) is installed.
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) is installed.
- [Vagrant](https://www.vagrantup.com/downloads.html) is installed.
- [VM configuration files](https://github.com/udacity/fullstack-nanodegree-vm) are set up.

## Getting Started
- Download the repository to a local machine.
- Verify the following files are present before continuing:
  - `reporting_tool.py`
  - `newsdata.zip`
  - `fsnd-virtual-machine.zip`
  - `output_of_reporting_tool.txt` (example of output)
- Unzip the fsnd-virtual-machine.zip file (This contains the VM files).
- Unzip the newsdata.zip file (contains the PostgreSQL database for this project)
- Copy reporting_tool.py and newsdata.sql to the vagrant directory in the VM.
- Enter the virtual machine directory.
- Startup the virtual machine.

    `$vagrant up`

- Log in to the virtual machine.

    `$ vagrant ssh`

- Enter the shared vagrant directory and load the data from newsdata.sql.
    ```
    $ cd /vagrant
    $ psql -d news -f newsdata.sql
    ```

- Run the reporting_tool.py report generator from the command-line.

    `$ reporting_tool.py`

    The results will automatically be output to the terminal once the command is run.
    The results should match the sample output in `output_of_reporting_tool.txt`.
