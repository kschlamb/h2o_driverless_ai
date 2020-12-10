# Alternatively, you Can also specify on the java command with:
#  -Dai.h2o.mojos.runtime.license.file=/tmp/license.sig
export DRIVERLESS_AI_LICENSE_FILE=/tmp/license.sig

# UPDATE:
#
#  verbose=true: Includes extra debug lines showing what the threads are doing.
#  logging=true: Shows all values from table plus predictions all on one line.
#  save=false:   Attempts to execute updates.
#  save=true:    Instead of executing updates, it writes them out to stdout.

java -Dverbose=false -Dlogging=false -Dsave=false -Dwait=false -Dpause=false \
     -Dpropertiesfilename=properties-update -Dstats=true -Derrors=true \
     -Dthreads=2 -XX:+UseG1GC -XX:+UseStringDeduplication -Xms5g -Xmx5g \
     -cp db2jcc4.jar:mojo2-runtime.jar:DAIMojoRunner_DB.jar \
     daimojorunner_db.DAIMojoRunner_DB
