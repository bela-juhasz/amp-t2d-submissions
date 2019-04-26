from __future__ import print_function
from __future__ import division
import sys
import os
from subprocess import call
cmd = "zcat Hoorn_v2.BOLT.vcf.gz | grep -v \"#\" | awk \'{$6=$7=$8=$9=\"\"; print $0}\' | sed \'s/ \+/ /g\' | sed \'s/ /\\t/g\' | perl -pe \'s/^(\S+)\\t(\S+)\\t(\S+)\\t(\S+)\\t(\S+)/$3\\t$1\\t$2\\t$5\\t$4/;\' | bgzip -c > Hoorn_v2.BOLT.fin_ds_v2.vcf.gz"
call(cmd,shell=True)