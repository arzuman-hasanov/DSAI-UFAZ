package bgd.hadoop.wordlength;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;

//The main "driver" class that runs a MapReduce job
public class WordlengthMain
{
	
	public static void main(String[] args) throws Exception
	{
		// Create a Hadoop configuration (includes generic parameters)
		Configuration conf=new Configuration();
		
		// Get non-generic parameters (i.e. written after hadoop ones)
		String[] ourArgs=new GenericOptionsParser(conf, args).getRemainingArgs();
		
		// Create an Hadoop Job (new Hadoop task) from the configuration (+ naming it)
		Job job=Job.getInstance(conf, "Wordlength");

		// Assign "driver", "map" and "reduce" classes to the Job
		job.setJarByClass(WordlengthMain.class);
		job.setMapperClass(WordlengthMap.class);
		job.setReducerClass(WordlengthReduce.class);

		// Set key/values types for this Hadoop job
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);

		// Define the input and output files/directory 
		// Here, remaining arguments given after Hadoop onesin the command line
		FileInputFormat.addInputPath(job, new Path(ourArgs[0]));
		FileOutputFormat.setOutputPath(job, new Path(ourArgs[1]));

		// Run the Hadoop Job
		if(job.waitForCompletion(true))
			System.exit(0); // Job completed
		System.exit(-1); // Job failed
	}
}
