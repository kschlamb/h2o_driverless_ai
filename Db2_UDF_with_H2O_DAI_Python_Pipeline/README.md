**Embedding H2O Driverless AI Python Scoring Pipeline code in a Db2 11.5 User Defined Function**

NOTE: This isn't a suggested approach, nor does it perform well. Instead, the Python MOJO approach should be used instead. However, I ran these tests to show it can be done. I've made it work on Ubuntu 18.04 in VMware.

Db2 Setup:
- DBM CFG parameter PYTHON_PATH needs to be set (e.g. PYTHON_PATH=/bin/python3)

H2O Driverless AI Python Runtime Setup:
- See documentation: http://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scoring-pipeline-cpp.html

Steps:
- Create database: db2 create database testdb
- Create function: db2 -tvf create_function.sql
- Edit iris_predict_pp_udf.py: Change the import of scoring_h2oai_experiment* to the one associated with your experiment (from the downloaded scorer.zip file)
- Call function:   db2 -tvf call_function.sql
