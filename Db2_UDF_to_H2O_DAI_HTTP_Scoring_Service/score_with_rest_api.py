import nzae       # Required for Db2 Python UDFs
import requests   # For HTTP processing
import json       # To manipulate JSON data in results

# Set this to the URL of the HTTP server hosting the Driverless AI model.
# For test purposes, the model can be run using the run_http_server.sh
# script that is included as part of the Python scoring pipeline that
# can be downloaded from Driverless AI.
url = 'http://127.0.0.1:9090/rpc'

class scoring_udf(nzae.Ae):

    # Main function for the Db2 UDF.
    def _getFunctionResult(self, row):

        # For debug purposes, log input data to Db2's routine.0.log.
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

        # There's an alternative way of calling requests() that's
        # described in the Driverless AI README file, but using the
        # following code as I know it works.

        payload = { "id": 1,             # Arbitrary identifier
                    "method": "score",   # Single row scoring function
                    "params": { "row": { "sepal_length": inSepalLength,
                                         "sepal_width": inSepalWidth,
                                         "petal_length": inPetalLength,
                                         "petal_width": inPetalWidth } } }
        headers = {}
        results = requests.post(url,
                                data=json.dumps(payload),
                                headers=headers)

        # If the call failed then exit out with the error code.
        if not results.ok:
            self.log("ERROR REASON: " + str(results.reason), logLevel=None)
            return(str(results.status_code))

        # Fields in results include (but not limited to):
        #  - text:        Returns the content of the response.
        #  - json():      Returns a JSON object of the result.
        #                 e.g. {"jsonrpc": "2.0", "id": 1,
        #                       "result": [0.9614821672439575,
        #                        0.020350966602563858,
        #                        0.008531522937119007,
        #                        0.004501492250710726,
        #                        0.005133881699293852]}
        #  - status_code: Returns status number (200 is OK, 404 is
        #                 Not Found).
        #  - reason:      Returns a text corresponding to the status
        #                 code (e.g. OK, Not Found)
        #  - ok:          Returns True if status_code < 400,
        #                 otherwise False.

        # To determine the label to return, we first need to find the
        # highest confidence level in the result set. Then we need to
        # query the label names.

        # For debug purposes, log the results to Db2's routine.0.log.
        self.log("SCORE RESULTS:\n" + str(results.json()), logLevel=None)

        result_list = results.json()['result']
        maxpos = result_list.index(max(result_list))

        # To return the actual class label, the columns need to be
        # queried. In practice, it's probably faster to maintain the
        # labels in a lookup table in the database (and have the caller
        # do the lookup) versus making a 2nd API call for each UDF call.
        # However, we'll do it via the API call here.

        payload = { "id": 1, "method": "get_target_labels", "params": {} }
        results2 = requests.post(url,
                                 data=json.dumps(payload),
                                 headers=headers)

        # For debug purposes, log the results to Db2's routine.0.log.
        self.log("QUERY RESULTS:\n" + str(results2.json()), logLevel=None)

        # If the call failed then exit out with the error code.
        if not results2.ok:
            self.log("ERROR REASON: " + str(results2.reason), logLevel=None)
            return(str(results2.status_code))

        label = results2.json()['result'][maxpos]

        # For debug purposes, log the label being returned to Db2's
        # routine.0.log.
        self.log("LABEL: " + label, logLevel=None)

        return(label)

scoring_udf.run()
