# Alternatively, you Can also specify on the java command with:
#  -Dai.h2o.mojos.runtime.license.file=/tmp/license.sig
export DRIVERLESS_AI_LICENSE_FILE=/tmp/license.sig

# Score to CSV:
#
# - The CSV data is outputed to stdout, it isn't written to a file.
# - To ensure no extra stuff is written out, you have to have VERBOSE, LOGGING
#   and WAIT all set to false. The value for SAVE doesn't seem to have any
#   impact on the output.

java -Dverbose=true -Dlogging=true -Dwait=true -Dpause=false \
     -Dpropertiesfilename=properties-csv -Dstats=false -Derrors=false \
     -Dthreads=2 -XX:+UseG1GC -XX:+UseStringDeduplication -Xms5g -Xmx5g \
     -cp db2jcc4.jar:mojo2-runtime.jar:DAIMojoRunner_DB.jar \
     daimojorunner_db.DAIMojoRunner_DB
