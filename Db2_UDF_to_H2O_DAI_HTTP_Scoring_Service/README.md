**Db2 11.5 User Defined Function Scoring via REST APIs to an HTTP Server Hosting an H2O Driverless AI Python Scoring Pipeline**

Db2 Setup:
- DBM CFG parameter PYTHON_PATH needs to be set (e.g. PYTHON_PATH=/bin/python3)

H2O Driverless AI Python Runtime Setup:
- See documentation describing how to run a standalone Python Scoring Pipeline with the example HTTP scoring service: http://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/scoring-standalone-python.html

Steps:
- Create database: db2 create database testdb
- Create function: db2 -tvf create_function.sql
- Start HTTP scoring service with standalone Python scoring pipeline
- Edit score_with_rest_api.py: If needed, change HTTP scoring service URL
- Call function:   db2 -tvf call_function.sql
