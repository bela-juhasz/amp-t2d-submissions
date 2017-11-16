xls2xml module
==============

### What is This?
This simple tool suite is for validating xls, converting xls to tsv or xml file.

### Prerequisites
Please install all the libraries and modules listed in requirements.txt. This suite works best with Python 2.7 or above.

### Using the scripts
There are a few scripts you can run under xls2xml subdirectory:
```commandline
validate_xls.py
validate_tsv.py
xls2tsv.py
xls2xml.py
tsv2xml.py
```
Please refer to their command line help for information about what they do and which arguments are required. e.g.:
```commandline
./xls2xml/xls2xml.py -h
```

### Writing the configuration files
There are a few different types of input files for these scripts. The examples of each could be found in tests/data:
```commandline
tests/data/example_AMP_T2D_Submission_form_V2.xlsx
tests/data/example_samples.tsv
tests/data/example_samples.xml
```
For the details of how they they should be written, there are comments in each examples above.