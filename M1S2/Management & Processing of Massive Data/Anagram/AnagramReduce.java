package bgd.hadoop.anagram;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;
import java.util.Iterator;
import java.io.IOException;

// The "reducer" class
// org.apache.hadoop.mapreduce.Reducer<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class AnagramReduce extends Reducer<Text, Text, Text, Text>
{

	private Text result = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

		String anagramlist = ": [";
		
		int length = 0;
		
		
		for(Text val : values){
			anagramlist+= val.toString() + ", ";
			length++;
		}
		
		anagramlist=anagramlist.substring(0, anagramlist.length() - 2);
		anagramlist+= "]";
		
		//System.out.println(key+" "+anagramlist);
		
		if(length>2){
			result.set(anagramlist);
			context.write(key,result);
		}
	}
}
