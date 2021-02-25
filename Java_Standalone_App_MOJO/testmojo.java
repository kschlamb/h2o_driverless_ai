// Compile command: javac -cp mojo2-runtime-2.1.4-all.jar testmojo.java
// Run command:     java -cp .:mojo2-runtime-2.1.4-all.jar testmojo <measurements>

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

public class testmojo {

    public static void main(String[] args) throws IOException, LicenseException {

        // Validate that the user provided the 4 required measurements.
        if (args.length != 4)
        {
           System.out.print("\nUsage: testmojo <sepal_length> <sepal_width> <petal_length> <petal_width>\n\n");
           System.exit(-1);
        }

        // Load the model.
        System.out.print("== Loading MOJO File ... ");
        final MojoPipeline model = MojoPipeline.loadFrom("pipeline.mojo");
        System.out.print("Complete\n");

        // Fill in the input columns. Ensure that you're using
        // the right input column name (case needs to match, etc.).
        final MojoFrameBuilder frameBuilder = model.getInputFrameBuilder();
        final MojoRowBuilder rowBuilder = frameBuilder.getMojoRowBuilder();
        rowBuilder.setValue("SepalLengthCm", args[0]);
        rowBuilder.setValue("SepalWidthCm", args[1]);
        rowBuilder.setValue("PetalLengthCm", args[2]);
        rowBuilder.setValue("PetalWidthCm", args[3]);
        frameBuilder.addRow(rowBuilder);

        // Create the input frame required by the MOJO pipeline.
        // Display it just for validation purposes.
        System.out.print("\n== Input Data:\n");
        final MojoFrame inputFrame = frameBuilder.toMojoFrame();
        inputFrame.debug();

        // Score the data in the input frame.
        final MojoFrame outputFrame = model.transform(inputFrame);

        // This can be used to view the contents of a frame. Basically, it
        // shows all of the output labels and percentags, separated across
        // multiple lines.
        System.out.print("\n== Output Predictions:\n");
        outputFrame.debug();

        // Output prediction to the screen as a CSV. It includes both the labels
        // as well as the confidence levels (percentages) for each label.
        // This can easily be modified to write to a file.
        System.out.print("\n== Output Predictions as CSV:\n");
        SimpleCSV outputCSV = SimpleCSV.read(outputFrame);
        outputCSV.write(System.out);

        System.out.print("\n== Prediction:\n");

    }
}
