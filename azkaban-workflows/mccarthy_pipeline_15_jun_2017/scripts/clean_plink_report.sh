#!/bin/bash
#Cleans a PLINK report file (using spaces for human readable table)
sed 's/^ *//g' | tr -s ' ' '\t'