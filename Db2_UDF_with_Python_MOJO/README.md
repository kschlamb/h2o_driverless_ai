**Embedding an H2O Driverless AI Python Mojo scoring pipeline in a Db2 11.5 User Defined Function**

Db2 Setup:
- DBM CFG parameter PYTHON_PATH needs to be set (e.g. PYTHON_PATH=/bin/python3)

H2O Driverless AI Python Runtime Setup:
- See documentation: http://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scoring-pipeline-cpp.html

Steps:
- Create database: db2 create database testdb
- Create function: db2 -tvf create_function.sql
- Edit iris_predict_udf.py: Change mojoFilename variable to point to location of the MOJO file
- Call function:   db2 -tvf call_function.sql
