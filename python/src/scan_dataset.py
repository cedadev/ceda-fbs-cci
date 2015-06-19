#!/usr/bin/env python
#"""
#Usage:
#    scan_bataset.py [--help | --h]
#    scan_dataset.py (-d | --dataset=<dataset_id>)
#    scan_dataset.py (-l | --level=<level>)
#    scan_dataset.py [-m | --make-list]
#    scan_dataset.py [-c | --config=<path_to_config_dir>]
#    scan_dataset.py [-n | --num-files=<n_files>]

#Options:
#    -h --help                 Show this screen.
#    -d --dataset=<id>         Specify the dataset to be scanned wirhin the file datasets.ini.
#    -l --level=<level>        Specify the Level of information being retrieved about the files in the dataset, as follows:     
#                              Level 1: File names and sizes
#                              Level 2: File names, sizes and phenomena (e.g. "air temperature")
#                              Level 3: File names, sizes, phenomena and geospatial metadata 
#                              <level> is an integer of value 1, 2 or 3. 
#    -m --makelist=<m>         Make a list of files for the given dataset.
#    -c --config=<name>        Specify the main configuration directory.
#    -n --num-files=<n_files>  Specify the number of files to scan within each job.    
#"""

"""
Usage:
  scan_dataset.py -h | --help
  scan_dataset.py --version
  scan_dataset.py (-f <filename> | --filename <filename>) (-d <dataset_id> | --dataset <dataset_id> ) 
  scan_dataset.py (-l <level> | --level <level>)
  scan_dataset.py -m | --make-list
  scan_dataset.py -c <path_to_config_dir> | --config <path_to_config_dir>
  scan_dataset.py -n <n_files> | --num-files <n_files>
  scan_dataset.py -s <start_number> | --start <start_number>
  
Options:
  -h --help                           Show this screen.
  --version                           Show version.
  -d --dataset=<dataset_id>           Dataset id.
  -f --filename=<filename>            File from where the dataset will be read [default: datasets.ini]. 
  -l --level=<level>                  Level of search:
                                      Level 1: File names and sizes
                                      Level 2: File names, sizes and phenomena (e.g. "air temperature")
                                      Level 3: File names, sizes, phenomena and geospatial metadata.
  -m --make-list                      Stores the list of filenames to a file [default: file_lists.txt].
  -c --config=<path_to_config_dir>    Specify the main configuration directory.
  -n  --num-files=<n_files>           Number of files to scan.
  -s --start=<start_number>           Starting point within the cache file containing filenames [default: 10].
 """


import os

from docopt import docopt

import ceda_di.util.cmd as cmd
from ceda_di import __version__  # Grab version from package __init__.py
from ceda_di.extract import Extract
from ceda_di.index import BulkIndexer
from ceda_di.search import Searcher

def main():
    conf_args = cmd.sanitise_args(docopt(__doc__, version=__version__))
          
    """
    Basic algorithm :
        Validate input
        Implement command line options. 
    """
    
    #Argument validation.
    
    
    
    print "These are all the arguments :"
    for keys,values in conf_args.items():
        print(keys, " -->", values)
               
        
if __name__ == '__main__':
    main()