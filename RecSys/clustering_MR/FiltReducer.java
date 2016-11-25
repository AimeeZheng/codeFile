package clustering;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import utils.TextPair;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by zhengyaolin on 2016/10/8.
 *
 * Description: set filting
 *
 * Input:
 *      key: last 2 users
 *      value: same users (k-1)
 *
 * Output:
 *      key: k+1-items set
 *      value: null
 *
 */
public class FiltReducer extends Reducer<Text, TextPair, Text, NullWritable> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<TextPair> values, Context context)
            throws IOException, InterruptedException {
        ArrayList<String> clusted = new ArrayList<String>();
        boolean flag = false;
        for(TextPair val : values) {
            String tag = val.getFirst().toString();
            if(tag.equals("orig"))
                flag = true;
            else if(tag.equals("clusted"))
                clusted.add(val.getSecond().toString());
            else
                throw new IOException("Wrong map Result!");
        }
        if(clusted.size() == 0 || !flag)
            return;
        //Join
        for(String u : clusted) {
            if(!u.equals("")) {
                result.set(u + "|" + key.toString());
                context.write(result, NullWritable.get());
            }
        }
    }
}
