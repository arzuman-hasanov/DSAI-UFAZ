package bgd.hadoop.weather;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Reducer;
import java.util.Iterator;
import java.io.IOException;

// The "reducer" class
// org.apache.hadoop.mapreduce.Reducer<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class WeatherReduce extends Reducer<Text, Text, Text, Text>
{

	private Text result = new Text();

	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

		String output = "";
		
		double length = 0;
		double sum = 0;
		
		for(Text val : values){
			sum+= Double.parseDouble(val.toString());
			length++;
		}
		
		double avgTemp = 0.0;
		
		if(length>0)
			avgTemp = sum/length;
		
		output = ""+avgTemp;

		result.set(output);
		context.write(key,result);
		
	}
}
