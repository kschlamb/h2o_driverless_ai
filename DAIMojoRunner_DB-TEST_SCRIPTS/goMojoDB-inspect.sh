# Alternatively, you Can also specify on the java command with:
#  -Dai.h2o.mojos.runtime.license.file=/tmp/license.sig
export DRIVERLESS_AI_LICENSE_FILE=/tmp/license.sig

# INSPECT:

java -Dinspect=true -Dpropertiesfilename=properties-inspect \
     -XX:+UseG1GC -XX:+UseStringDeduplication -Xms5g -Xmx5g \
     -cp db2jcc4.jar:mojo2-runtime.jar:DAIMojoRunner_DB.jar \
     daimojorunner_db.DAIMojoRunner_DB 
