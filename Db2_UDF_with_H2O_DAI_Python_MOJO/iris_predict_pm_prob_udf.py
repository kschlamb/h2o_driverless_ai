# Sample code for calling an H2O Driverless AI Python MOJO scoring
# pipeline from a Db2 Python UDF (requires Db2 11.5.4+). Assumes that
# the necessary package prerequisites have been met (and that a DAI
# license is setup on the system).
#
# This is based on the well known Iris Species dataset.
#
# Kelly Schlamb (kschlamb@gmail.com)

import nzae
import daimojo.model
import datatable as dt

mojoFilename = "/home/db2inst1/MOJO_Pipelines/dai_iris_pipeline.mojo"


class inference_udf(nzae.Ae):

    # Function body for Db2 Python UDF.
    def _getFunctionResult(self, row):

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

        # Load the model from the MOJO binary. The MOJO is downloaded
        # from DAI after an experiment completes).
        m = daimojo.model(mojoFilename)

        # Setup an input Datatable frame with a single row that contains
        # the four input parameters (the column names correspond to the
        # column names that were specified when the model was built in
        # DAI).
        dtFrame = dt.Frame(sepal_length=[inSepalLength],
                           sepal_width=[inSepalWidth],
                           petal_length=[inPetalLength],
                           petal_width=[inPetalWidth])

        # For debug purposes, log the data table frame to Db2's routine
        # log (~/sqllib/db2dump/DIAG0000/routinelog/routine.0.log).
        self.log("INPUT FRAME:\n" + str(dtFrame), logLevel=None)

        # Score the input data (make a prediction).
        res = m.predict(dtFrame)

        # For debug purposes, log the prediction results to Db2's
        # routine log.
        self.log("PREDICTION RESULTS:\n" + str(res), logLevel=None)

        # The results are provided as a series of confidence levels,
        # We will find the highest value, and return the corresponding
        # label name (species type) for that value. The label name
        # is actually a two part name (e.g. species.<type>) but we
        # just want to return the individual species name.
        resList = res.to_list()

        maxpos = resList.index(max(resList))
        labelFull = res.names[maxpos]
        label = labelFull.split(".", 1)[1]
        result = "LABEL:" + label + ", PROBS:("

        for i in range(len(resList)):
            labelFull = res.names[i]
            label = labelFull.split(".", 1)[1]
            #result = result + label + " " + str(resList[i][0])
            result = result + label + " " + str(int(resList[i][0] * 100000) / 100000)

            if ((i + 1) < len(resList)):
                result = result + ", "

        result = result + ")"

        return(result)

inference_udf.run()
