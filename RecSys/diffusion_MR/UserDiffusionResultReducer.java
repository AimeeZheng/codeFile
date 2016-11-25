package algorithm.tagBasedRec;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by zhengyaolin on 2016/11/24.
 *
 * Description: diffusion result for every user
 *
 * Input:
 *      key: item
 *      value: 1. <(user, count), flag:u>
 *             2. <item, resource>
 *
 * Output:
 *      key: user|item|resource
 *      value: null
 *
 * Note:
 *      resource = count * i-resource
 */
public class UserDiffusionResultReducer extends Reducer<Text, TextPair, Text, NullWritable> {
    private Text result = new Text();


    public void reduce(Text key, Iterable<TextPair> values, Context context)
            throws IOException, InterruptedException {
        ArrayList<String> users = new ArrayList<String>();
        ArrayList<String> items = new ArrayList<String>();
        ArrayList<String> itemRes = new ArrayList<String>();

        for (TextPair val : values) {
            String flag = val.getSecond().toString();
            if (flag.equals("u")) {
                users.add(val.getFirst().toString());
            } else {
                items.add(val.getFirst().toString());
                itemRes.add(val.getSecond().toString());
            }
        }

        int sumItem = items.size();

        for (String str : users) {
            String[] usr = str.split(",");
            for (int i = 0; i < sumItem; i++) {
                result.set(usr[0] + "|" + items.get(i) + "|" + Double.parseDouble(usr[1]) * Double.parseDouble(itemRes.get(i)));
                context.write(result, NullWritable.get());
            }
        }
    }
}