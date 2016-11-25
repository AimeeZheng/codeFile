package clustering;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.ArrayList;

/**
 * Created by zhengyaolin on 2016/10/11.
 *
 * Description: two sets union
 *
 * Input:
 *      key: k-1 users (sep = "|")
 *      value: list<user>
 * Output:
 *      key: k+1 users (sep = "|")
 *      value: null
 *
 */
public class ClusterReducer extends Reducer<Text, Text, Text, NullWritable> {
    private Text result = new Text();

    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        ArrayList<String> list = new ArrayList<String>();
        for(Text t : values) {
            list.add(t.toString());
        }
        int len = list.size();
        if(len > 1) {
            for(int i = 0; i < len - 1; i++) {
                String u1 = list.get(i);
                for(int j = i + 1; j < len; j++) {
                    String u2 = list.get(j);
                    String pair;
                    if(u1.compareTo(u2) > 0) {
                        pair =  u2 + "|" + u1;
                    } else {
                        pair =  u1 + "|" + u2;
                    }
                    // Union
                    result.set(pair + "|" + key.toString());
                    context.write(result, NullWritable.get());
                }
            }
        }
    }
}
