package algorithm.tagBasedRec;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by zhengyaolin on 2016/11/23.
 *
 * Description: diffusion between items and users/tags
 *
 * Input:
 *      key: user/tag
 *      value:  1:<item, flag>   2:<(item, resource), flag>
 *
 * Output:
 *      key: item|item|resource
 *      value: null
 *
 */
public class BipartiteGraphDiffusionReducer extends Reducer<Text, TextPair, Text, NullWritable> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<TextPair> values, Context context)
            throws IOException, InterruptedException {
        ArrayList<String> item1 = new ArrayList<String>();
        ArrayList<String> item2 = new ArrayList<String>();
        for(TextPair val : values) {
            String flag = val.getSecond().toString();
            if(flag.equals("1"))
                item1.add(val.getFirst().toString());
            else if(flag.equals("2"))
                item2.add(val.getFirst().toString());
            else
                throw new IOException("Wrong map Result!");
        }
        int sum = item1.size();
        if(sum == 0 || item2.size() == 0)
            return;

        //source diffuse from item2 to item1
        for(String first : item2) {
            String[] strs = first.split(",");
            String from = strs[0];
            double source = Double.parseDouble(strs[1]);
            for(String to : item1) {
                result.set(from + "|" + to + "|" + (source / sum));
                context.write(result, NullWritable.get());
            }
        }
    }
}