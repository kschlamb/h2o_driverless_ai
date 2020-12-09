import numpy as np
from numpy import nan
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
print("\nConnecting to database \'" + dbName + "\' ... ", end="")
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

# Select all of the rows from the IRIS table and score each row.

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
    print("Complete.")

# Keep reading and displaying the rows until there are none left.
noData = False
numRows = 0
while noData is False:
    # Retrieve A Record And Store It In A Python Tuple
    print('\n---------- Fetching & Scoring Row ' + str(numRows + 1) + ' ----------')
    try:
        print("Fetching row... ", end="")
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

        # The format of input record to the Scorer.score() method is as follows:
        #
        # ---------------------------------------------------------------
        # Name           Type      Range                                 
        # ---------------------------------------------------------------
        # sepal_length   float32   [4.300000190734863, 7.900000095367432]
        # sepal_width    float32   [2.0, 4.400000095367432]              
        # petal_length   float32   [1.0, 6.900000095367432]              
        # petal_width    float32   [0.10000000149011612, 2.5]            
        # ---------------------------------------------------------------

        # To score one row at a time, use the Scorer.score() method
        # (this can seem really slow due to one-time overhead):

        print("Calling scoring API... ", end="")
        rowScore = scorer.score([str(dataRecord[0]),   # SEPAL_LENGTH
                                 str(dataRecord[1]),   # SEPAL_WIDTH
                                 str(dataRecord[2]),   # PETAL_LENGTH
                                 str(dataRecord[3])])  # PETAL_WIDTH
        print("Complete.")

        # To determine the label to return, we first need to find the
        # highest confidence level in the result set.
        maxpos = rowScore.index(max(rowScore))
        label = labels[maxpos]

        print("\nROW: " + str(dataRecord[0]) + ", "
                        + str(dataRecord[1]) + ", "
                        + str(dataRecord[2]) + ", "
                        + str(dataRecord[3]))
        print(" SCORE: " + str(rowScore))
        print(" LABEL: " + str(label))

        numRows += 1

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
