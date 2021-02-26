/**
*
* This is a sample application that uses an H2O Driverless AI model MOJO to
* score against data queried from a Db2 (LUW) database.
*
* The app performs the following actions:
*
*  - Loads H2O Driverless AI MOJO file
*  - Connects to Db2 database
*  - Queries a table that has one or more rows of Iris flower measurements
*    (sepal length, sepal width, petal length, petal width).
*  - Gathers all input rows and uses the MOJO to score the data.
*  - All output predictions are written in CSV to the screen.
*
* Required Setup:
*
*  - Db2 table must be defined as follows with data inserted into it:
*
*      create table iris_new (sepal_length dec(2,1), sepal_width dec(2,1),
*                             petal_length dec(2,1), petal_width dec(2,1))
*      insert into iris_new values (5.2, 2.7, 1.7, 1.0)
*      insert into iris_new values (6.4, 3.0, 5.8, 2.3)
*      ...
*
*  - Driverless AI license must be setup prior to running the app.
*
*  - Compile: javac -cp mojo2-runtime-2.1.4-all.jar dai_mojo_db2_iris.java
*  - Run:     java -cp .:mojo2-runtime-2.1.4-all.jar:/opt/ibm/db2/v11.5/java/db2jcc4.jar dai_mojo_db2_iris <parms>
*
*  - Usage:   dai_mojo_db2_iris <Server IP> <Port #> <DBname> <UserID> <Password> <Table> <MOJO File>
*
* @author  Kelly Schlamb
* @since   2021-02-26 
*/

import ai.h2o.mojos.runtime.MojoPipeline;
import ai.h2o.mojos.runtime.frame.MojoFrame;
import ai.h2o.mojos.runtime.frame.MojoFrameBuilder;
import ai.h2o.mojos.runtime.frame.MojoRowBuilder;
import ai.h2o.mojos.runtime.lic.LicenseException;
import ai.h2o.mojos.runtime.utils.SimpleCSV;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.Arrays;
import java.lang.*;
import java.sql.*;

public class dai_mojo_db2_iris
{
   public static void main(String[] args) throws IOException, LicenseException
   {
      String           Db2ServerIP;
      String           Db2PortNum;
      String           Db2DBName;
      String           Db2UserID;
      String           Db2Password;
      String           Db2TableName;
      String           mojoFileName;
      Statement        stmt;
      String           stmtText;
      ResultSet        results;
      MojoFrameBuilder frameBuilder;
      MojoRowBuilder   rowBuilder;

      try
      {

         // Validate the parameters.

         if (args.length != 7)
         {
            System.out.print("\nUsage: dai_mojo_db2_iris <Server IP> <Port #> <DBname> <UserID> <Password> <Table> <MOJO File>\n\n");
            System.out.print("    Server IP: Hostname or IP address of Db2 server (e.g. 127.0.0.1).\n");
            System.out.print("    Port #:    Port number that Db2 server is listening on (e.g. 50000).\n");
            System.out.print("    DBname:    Name of Db2 database to connect to.\n");
            System.out.print("    UserID:    User ID to connect to database with.\n");
            System.out.print("    Password:  Password to connect to database with.\n");
            System.out.print("    Table:     Name of table with Iris flower measurements.\n");
            System.out.print("    MOJO File: Path to MOJO file (e.g. pipeline.mojo).\n\n");
            System.exit(-1);
         }

         Db2ServerIP = args[0];
         Db2PortNum = args[1];
         Db2DBName = args[2];
         Db2UserID = args[3];
         Db2Password = args[4];
         Db2TableName = args[5];
         mojoFileName = args[6];

         // Load the model (Driverless AI MOJO).

         System.out.print("== Loading MOJO file (" + mojoFileName + ")... ");
         final MojoPipeline model = MojoPipeline.loadFrom(mojoFileName);
         System.out.print("Complete\n");

         // Connect to the database.

         String url = "jdbc:db2://" + Db2ServerIP + ":" + Db2PortNum + "/" + Db2DBName;
         System.out.print("== Connecting to Db2 database (" + url + ")... ");

         Connection con = DriverManager.getConnection(url, Db2UserID, Db2Password);
         System.out.print("Complete\n");

         // Query the table specified by the user and load it into the input
         // frame. The expectation is that there are 4 columns in the table as
         // shown here:
         //
         //  create table iris_new (sepal_length dec(2,1), sepal_width dec(2,1),
         //                         petal_length dec(2,1), petal_width dec(2,1))

         stmtText = "SELECT * FROM " + Db2TableName;
         System.out.print("== Querying database table (" + stmtText + ")... ");
         stmt = con.createStatement();
         results = stmt.executeQuery(stmtText);

         // For each row in the result set, add it to the MOJO frame builder.
         // It will later be converted as a whole into a MOJO input frame to
         // be scored as a whole.

         frameBuilder = model.getInputFrameBuilder();
         rowBuilder = frameBuilder.getMojoRowBuilder();

         while (results.next())
         {
            System.out.print("\n=== Row: "
                              + results.getString(1) + ","
                              + results.getString(2) + ","
                              + results.getString(3) + ","
                              + results.getString(4));

            // Note that when filling in the input values, the variable/feature
            // names must match (name, case) with what the model expects.

            rowBuilder.setValue("SepalLengthCm", results.getString(1));
            rowBuilder.setValue("SepalWidthCm", results.getString(2));
            rowBuilder.setValue("PetalLengthCm", results.getString(3));
            rowBuilder.setValue("PetalWidthCm", results.getString(4));
            frameBuilder.addRow(rowBuilder);
         }
         System.out.print("\n");

         // Create the input frame required by the MOJO pipeline. This contains
         // all of the rows read in from the Db2 table.

         final MojoFrame inputFrame = frameBuilder.toMojoFrame();
         //inputFrame.debug();

         // Score the data in the input frame, with the results going into
         // an output frame.

         final MojoFrame outputFrame = model.transform(inputFrame);
         //outputFrame.debug();

         // Display the predictions to the screen as a CSV. This includes the
         // class labels as the first row, followed by the confidence levels
         // (percentages) for all classes for each of the predictions. This can
         // easily be modified to write to a file, or to a Db2 table.

         System.out.print("== Predictions (CSV):\n");
         SimpleCSV outputCSV = SimpleCSV.read(outputFrame);
         outputCSV.write(System.out);

         System.out.print("== Exiting\n");
      }
      catch (SQLException e)
      {
         System.out.println("SQL exception occurred:");
         System.out.println(" *Error message: " + e.getMessage());
         System.out.println(" *Error code: " + e.getErrorCode());
         System.out.println(" *SQL state: " + e.getSQLState());
         System.out.println("== EXITING DUE TO ERROR ==");
      }
      catch (Exception e)
      {
         System.out.println("Exception occurred:");
         System.out.println(" *Error message: " + e.getMessage());
         System.out.println("== EXITING DUE TO ERROR ==");
      }
   }
}
