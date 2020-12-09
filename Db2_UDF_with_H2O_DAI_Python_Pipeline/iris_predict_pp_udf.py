import nzae

# DAI needs to write to the current working directory (which by default
# appears to be root /). Change to /tmp, which all processes should have
# access to.
import os
os.chdir('/tmp')

# Import the scoring class. This needs to match the wheel file included
# in the Python scoring pipeline zip file (scorer.zip) that is downloaded
# from Driverless AI after an experiment completes. It also has to be
# installed via pip prior to running this.
from scoring_h2oai_experiment_652df26e_3a53_11eb_9649_000c294285d8 import Scorer

class make_prediction(nzae.Ae):

    # Main function for the Db2 UDF.
    def _getFunctionResult(self, row):

        # For debug purposes, log the input data to Db2's routine
        # log (~/sqllib/db2dump/DIAG0000/routinelog/routine.0.log).
        self.log("INPUT ROW: \"" + str(row) + "\"", logLevel=None)

        # This function is defined in Db2 to accept 4 float parameters.
        # The function can be defined such that this code is not executed
        # if any input parameter is NULL, but to be safe we'll return
        # NULL (None in Python) if any one of the parameters is NULL.
        #
        # Alternatively, we could fail the SQL statement outright by
        # executing the following code, which results in an SQL0443N
        # error with the accompanying message returned:
        #
        #  self.userError("NULL inputs not allowed.")

        inSepalLength, inSepalWidth, inPetalLength, inPetalWidth = row
        if (inSepalLength is None or inSepalWidth is None or
             inPetalLength is None or inPetalWidth is None):
            return(None)

        # Create a singleton Scorer instance. According to H2O, for
        # optimal performance create a Scorer instance once, and call
        # score() or score_batch() multiple times.
        scorer = Scorer()

        # The score() method is used to score a single row. Note that this
        # can be slow due to one-time overhead. I've seen this take 5-30
        # seconds per function invocation. This does make it highly
        # impracticle, and in practice this isn't the approach that should
        # be used. It's highly suggested that the Python MOJO approach be
        # used instead. However, we're taking this approach simply to show
        # that it can be done.

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

        result = scorer.score([inSepalLength,
                               inSepalWidth,
                               inPetalLength,
                               inPetalWidth],
                              apply_data_recipes=False)

        # For debug purposes, log the result to Db2's routine.0.log.
        self.log("INPUT RESULT: \"" + str(result) + "\"", logLevel=None)

        # To determine the label to return, we first need to find the
        # highest confidence level in the result set. Then we need to
        # query the label names.

        maxpos = result.index(max(result))
        labels = scorer.get_target_labels()

        # For debug purposes, log the labels to Db2's routine.0.log.
        self.log("LABELS: \"" + str(labels) + "\"", logLevel=None)

        label = labels[maxpos]
        return(label);

make_prediction.run()
