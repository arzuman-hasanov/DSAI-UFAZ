package bgd.hadoop.wordlength;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import java.util.StringTokenizer;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;


// The "mapper" class
// org.apache.hadoop.mapreduce.Mapper<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class WordlengthMap extends Mapper<Object, Text, Text, IntWritable>
{
	private final static IntWritable one = new IntWritable(1);
	private Text word = new Text();

	protected void map(Object key, Text value, Context context) throws IOException, InterruptedException
	{  
		// StringTokenizer allows to iterate through each word of current line (given in "value" parameter) 
		StringTokenizer tok=new StringTokenizer(value.toString(), " ");
		while(tok.hasMoreTokens())
		{
			// Get the next word on current line
			word.set(tok.nextToken());
			int length = word.getLength();

			// Return (key,value) tuple: (current word,1) for each of condition
			if (length < 3) {
				context.write(new Text("Short words:"), one);
			} else if (length < 6) {
				context.write(new Text("Medium words:"), one);
			} else {
				context.write(new Text("Long words:"), one);
			}
		}
	}
}
