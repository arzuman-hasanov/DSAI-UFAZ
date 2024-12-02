package bgd.hadoop.anagram;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.IntWritable;
import java.util.StringTokenizer;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;
import java.util.Arrays;

// The "mapper" class
// org.apache.hadoop.mapreduce.Mapper<KEYIN,VALUEIN,KEYOUT,VALUEOUT>
public class AnagramMap extends Mapper<Object, Text, Text, Text>
{

	private Text word = new Text();
	private Text sortedText = new Text();
	private Text orginalText = new Text();

	public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
	
		StringTokenizer itr = new StringTokenizer(value.toString());
		
		while (itr.hasMoreTokens()) {
			word.set(itr.nextToken());
			char[] wordChars = word.toString().toCharArray();
			Arrays.sort(wordChars);
			String sortedWord = new String(wordChars);
			sortedText.set(sortedWord);
			orginalText.set(word);
		//System.out.println(sortedText+" "+orginalText);
			context.write(sortedText, orginalText);
		}
		
	}
}
