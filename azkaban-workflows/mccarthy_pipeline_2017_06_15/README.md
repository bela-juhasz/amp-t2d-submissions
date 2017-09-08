# McCarthy pipeline

Azkaban tailored version of the McCarthy pipeline. Small modification done to the shell scripts to pass the parameters through command line instead of shell variables.

## Pipeline execution

To execute this pipeline in Azkaban you must fill these properties or the execution will fail.
```
input.stem=
ref.stem=
complex.regions=
```
With the location for your input study, the reference used to compare to and the list of complex regions to ignore. For all these parameters you need to put the relative path to the NFS volume mounted in the azkaban executors.

## Pipeline installation in Azkaban

Create a new zip file with all the .job files and the scripts folder, then upload to a new Azkaban project from the web UI. Modify the property ```external.volume``` with the path to the folder where your external data volume is mounted.
