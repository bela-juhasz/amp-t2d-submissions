AMP T2D configuration
=====================

### What is This?
This directory contains configuration files for validating the AMP T2D submission pack and converting the XLS spreadsheets to XML objects.

### Prerequisites
To play with these configuration files or use them for actually producing XML objects that are ready for submitting to the EGA, you will need to have this repository checked out and install dependencies. 
```commandline
git clone https://github.com/EBIvariation/amp-t2d-submissions
cd amp-t2d-submissions/xls2xml
virtualenv -p python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Running the Tests
```commandline
source venv/bin/activate
cd amp-t2d/tests/
pytest
deactivate
```

### Converting Submission XLS
You can validate the submission xlsx file and generate XML objects using the example commands as below.
```commandline
source venv/bin/activate
# validating the submission xlsx file
python ./xls2xml/validate_xls.py --conf amp-t2d/T2D_xlsx.conf --schema amp-t2d/T2D_xlsx.schema amp-t2d/tests/data/example_AMP_T2D_Submission_form_V2_DB_25_01_2018.xlsx 
# generating sample xml
python ./xls2xml/xls2xml.py --conf amp-t2d/T2D_xlsx.conf --schema amp-t2d/T2D_xlsx.schema --conf-key Sample,Cohort --xslt amp-t2d/T2D_xls2xml.xslt amp-t2d/tests/data/example_AMP_T2D_Submission_form_V2_DB_25_01_2018.xlsx amp-t2d/output_sample.xml
# generating study xml
python ./xls2xml/xls2xml.py --conf amp-t2d/T2D_xlsx.conf --schema amp-t2d/T2D_xlsx.schema --conf-key Project --xslt amp-t2d/T2D_xls2xml.xslt amp-t2d/tests/data/example_AMP_T2D_Submission_form_V2_DB_25_01_2018.xlsx amp-t2d/output_study.xml
# generating analysis xml
python ./xls2xml/xls2xml.py --conf amp-t2d/T2D_xlsx.conf --schema amp-t2d/T2D_xlsx.schema --conf-key Analysis,File --xslt amp-t2d/T2D_xls2xml.xslt amp-t2d/tests/data/example_AMP_T2D_Submission_form_V2_DB_25_01_2018.xlsx amp-t2d/output_analysis.xml
deactivate
```
After this, you will find the XML files are generated in amp-t2d/output_*.xml

### Making change
You may need to make change to the configuration files so that they work for new requirements. You should find some references at the top of each configuration file. Please make sure you update the test cases as well so that the test cases still work.
