package bgd.hadoop.weather;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import java.util.StringTokenizer;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;
import java.util.Arrays;

// The "mapper" class
// org.apache.hadoop.mapreduce.Mapper<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class WeatherMap extends Mapper<Object, Text, Text, Text>
{

	private Text valueout = new Text();
	private Text keyout = new Text();

	public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
	
		StringTokenizer itr = new StringTokenizer(value.toString());
		
		while (itr.hasMoreTokens()) {
		
			String line = itr.nextToken();
		
			//System.out.println(line);
		
			String[] values = line.split(";");
		
			
			if(values.length>78){
		
				String temperature = values[7];
				
				if(temperature.compareTo("")!=0){
				
					double tk = Double.parseDouble(temperature);
					
					double tc = tk-273.15;
					
					valueout.set(""+tc);
				
					String date = values[1];
					
					String[] datebits = date.split("T");
					
					String day=datebits[0];

					keyout.set(day);
				
					context.write(keyout, valueout);
				
				}
			}
		}
		
	}
}
