package bgd.hadoop.wordlength;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;
import java.util.Iterator;
import java.io.IOException;

// The "reducer" class
// org.apache.hadoop.mapreduce.Reducer<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class WordlengthReduce extends Reducer<Text, IntWritable, Text, IntWritable>
{
	private IntWritable result = new IntWritable();

	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException
	{
		// Iterate through all values corresponding to the given key
		Iterator<IntWritable> i=values.iterator();
		
		// Initialize a counter
		int count=0;
		
		// Loop over values
		while(i.hasNext()) {
			// Increment the counter
			count+=i.next().get(); 
		}   
		result.set(count);
		// Return the tuple (key,value) of type (KEYOUT, VALUEOUT) with key = the word and value = its number of occurences
		context.write(key, result);
  }
}
