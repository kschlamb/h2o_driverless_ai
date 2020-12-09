import numpy as np
from numpy import nan
import pandas as pd
import ibm_db

# Import the scoring class. This needs to match the wheel file included
# in the Python scoring pipeline zip file (scorer.zip) that is downloaded
# from Driverless AI after an experiment completes. It also has to be
# installed via pip prior to running this.
from scoring_h2oai_experiment_652df26e_3a53_11eb_9649_000c294285d8 import Scorer

# Just for my own curiousity (not needed for rest of the program), show the
# arguments of the H2O DAI scoring functions.
#import inspect
#print("==== Function information for Scorer() ====")
#print(inspect.getargspec(Scorer.score))
#print(inspect.getargspec(Scorer.score).args)
#print(inspect.getargspec(Scorer.score_batch))
#print(inspect.getargspec(Scorer.score_batch).args)
#print("\n")

# Create a singleton Scorer instance.
# For optimal performance, create a Scorer instance once, and call score()
# or score_batch() multiple times. We'll also query the target labels
# (classes) at this point.
scorer = Scorer()
labels = scorer.get_target_labels()

# Initialize Db2 connection variables and construct the connection string.
hostName = "127.0.0.1"    # IP address of Db2 server
dbName = "TESTDB"         # Database name
portNum = "50000"         # Port number Db2 listening on
userID = "db2inst1"       # User ID to connect to Db2 with
passWord = "password"     # Password to connect to Db2 with
connectionID = None

connString = "DATABASE=" + dbName
connString += ";HOSTNAME=" + hostName
connString += ";PORT=" + portNum
connString += ";PROTOCOL=TCPIP"
connString += ";UID=" + userID
connString += ";PWD=" + passWord

# Connect to the database.
print('\n---------- Retrieving Data from Db2 ----------\n')
print("Connecting to database \'" + dbName + "\' ... ", end="")
try:
    connectionID = ibm_db.connect(connString, "", "")
except Exception:
    pass

# If the connection failed then display an error message and exit.
if connectionID is None:
    print("\nERROR: Unable to connect to database \'" + dbName + "\'.")
    print("Connection string used: " + connString + "\n")
    exit(-1)
else:
    print("Complete.\n")

# Select all of the rows from the IRIS table.

# Construct the SELECT statement.
selectStmt = "SELECT SEPAL_LENGTH" + \
                  ", SEPAL_WIDTH" + \
                  ", PETAL_LENGTH" + \
                  ", PETAL_WIDTH" + \
                  " FROM IRIS"

# Execute the SELECT statement.
print("Executing the SQL statement \"" + selectStmt + "\" ... ", end="")

try:
    resultSet = ibm_db.exec_immediate(connectionID, selectStmt)
except Exception:
    pass

# If there was an error then display an error message and exit.
if resultSet is False:
    print("\nERROR: Unable to execute the SQL statement specified.\n")
    conn.closeConnection()
    exit(-1)
else:
    print("Complete.\n")

# To score a batch of rows, use the Scorer.score_batch() method
# (which is much faster than repeated one-row scoring):
#
# This is an example of how a frame gets scored:
#
#   df = pd.DataFrame(columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
#   df.loc[0] = [ 2.0, 4.0, 2.0, 2.5 ]
#   df.loc[1] = [ 2.4, 3.0, 3.0, 1.7 ]
#   print(scorer.score_batch(df))

# The following code reads all of the data rows (one at a time) from the
# Db2 table into a Pandas dataframe. In reality you would probably construct
# this in a more efficient way and not read everything into a single frame.
# Instead, you could batch into 100 rows, for example, and repeat that
# as needed.

noData = False
rowNum = 0
df = pd.DataFrame(columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])

while noData is False:

    # Retrieve a record and store it in a Python tuple
    try:
        # Execute the SELECT statement.
        print("Fetching row " + str(rowNum + 1) + "... ", end="")
        dataRecord = ibm_db.fetch_tuple(resultSet)
    except:
        pass

    # If there was no data retrieved then set the flag to exit, otherwise
    # display the contents of the row.
    if dataRecord is False:
        print("No more data.")
        noData = True
    else:
        print("Complete.")

        # This code assumes everything is coming back from Db2 as valid,
        # non-NULL values. However, if a NULL value does get passed back
        # from Db2 then it will show up here as a value of None (with a
        # type of NoneType). Depending on the model, it might have to be
        # converted to a valid value instead (imputation).

        df.loc[rowNum] = [ float(dataRecord[0]),   # SEPAL_LENGTH
                           float(dataRecord[1]),   # SEPAL_WIDTH
                           float(dataRecord[2]),   # PETAL_LENGTH
                           float(dataRecord[3]) ]  # PETAL_WIDTH
        rowNum += 1

# Score all of the data in the dataframe and print the results.
print('\n---------- Batch Scoring ----------\n')
print("Calling Batch Scoring API... ", end="")
results = scorer.score_batch(df)
print("Complete.\n")

print('\n---------- Scoring Results ----------\n')
print(results)


# Disconnect from the database.
if not connectionID is None:
    print("Disconnecting from database \'" + dbName + "\' ... ", end="")
    try:
        returnCode = ibm_db.close(connectionID)
    except Exception:
        pass

    # If the disconnect failed then display an error message and exit.
    if returnCode is False:
        print("\nERROR: Unable to disconnect from database " + dbName + ".")
        exit(-1)

    # Otherwise, state that it was successful.
    else:
        print("Complete.\n")

# Exit from the application.
exit()
