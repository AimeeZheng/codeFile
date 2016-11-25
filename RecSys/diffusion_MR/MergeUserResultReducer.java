package algorithm.tagBasedRec;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/24.
 *
 * Description: merge item resource for every user
 *
 * input:
 *      key: user|item
 *      value: resource
 *
 * output:
 *      key: user|item|resource
 *      value:null
 *
 */

public class MergeUserResultReducer extends Reducer<Text, Text, Text, NullWritable>{
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        double sum = 0;
        for (Text val : values) {
            sum += Double.parseDouble(val.toString());
        }
        result.set(key.toString() + "|" + sum);
        context.write(result, NullWritable.get());
    }
}
