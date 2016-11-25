package algorithm.tagBasedRec;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.sql.SQLException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;

/**
 * Created by zhengyaolin on 2016/11/23.
 *
 * Description: diffusion integration
 *
 * resource := k * resource1 + (1-k) * resource2
 *
 * Input:
 *      key: item|item
 *      value: <resource, flag>
 *
 * Output:
 *      key: item|item|resource
 *      value: null
 *
 */
public class DiffusionIntegrateReducer extends Reducer<Text, TextPair, Text, NullWritable> {
    private Text result = new Text();
    private double lambda = 0;

    protected void setup(Context context)
            throws IOException, InterruptedException {
            Configuration conf = context.getConfiguration();
            lambda = Double.parseDouble(conf.get("lambda"));
    }

    public void reduce(Text key, Iterable<TextPair> values, Context context)
            throws IOException, InterruptedException {
        double res1 = 0;
        double res2 = 0;

        for(TextPair val : values) {
            String flag = val.getSecond().toString();
            if(flag.equals("1"))
                res1 += Double.parseDouble(val.getFirst().toString());
            else if(flag.equals("2"))
                res2 += Double.parseDouble(val.getFirst().toString());
            else
                throw new IOException("Wrong map Result!");
        }

        double res = lambda * res1 + (1 - lambda) * res2;
        result.set(key.toString() + "|" + res);
        context.write(result, NullWritable.get());
    }
}