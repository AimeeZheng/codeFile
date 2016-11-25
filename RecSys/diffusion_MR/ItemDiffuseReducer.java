package algorithm.tagBasedRec;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by zhengyaolin on 2016/11/22
 *
 * Description: resource diffusion from item to users/tags
 *
 * Input:
 *      key: item
 *      value: list<user>
 *          or list<tag>
 *
 * Output:
 *      key: item|user|resource
 *        or item|tag|resource
 *      value: null
 *
 */
public class ItemDiffuseReducer extends Reducer<Text, Text, Text, NullWritable> {
    private Text resultKey = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        ArrayList<String> others =  new ArrayList<String>();
        for(Text val : values) {
            others.add(val.toString());
        }
        int sum = others.size();
        for(String str :  others) {
            resultKey.set(key.toString() + "|" + str + "|" + (1f / sum));
            context.write(resultKey, NullWritable.get());
        }
    }
}
