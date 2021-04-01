These scripts use **DAIMojoRunner_DB**, which is an H2O.ai-provided application that uses your MOJO scoring pipeline (pipeline.mojo) to access databases through JDBC. This includes being able to score data in the database, inserting scoring results into the database, and updating tables in-place with the scoring results.

- The latest version of DAIMojoRunner_DB that I'm aware of (1.9.0.4 as of 03/03/2021) can be downloaded from H2O.ai [here](https://s3.amazonaws.com/artifacts.h2o.ai/releases/ai/h2o/dai-custom-scorers/DAI-1.9.0.4/index.html) (download the Database scorer).

Two .jar files are needed:

- DAI-Mojo-DB-<version>.jar (included in that package from H2O)
- db2jcc4.jar (Db2's type 4 JDBC driver)

There are four separate scripts and associated properties files:

- inspect: Displays information about the scoring pipeline
- csv: Scoring results (based on a Db2 query) are displayed to stdout in CSV format
- insert: Inserts scoring results into a Db2 table, separate from the input data
- updated: Inserts scoring results into the Db2 table that holds the input data
