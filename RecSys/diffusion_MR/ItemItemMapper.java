package algorithm.tagBasedRec;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/24
 *
 * Input：
 *      item|item|resource
 *
 * Output：
 *      key：item
 *      value：<item, resource>
 *
 */
public class ItemItemMapper extends Mapper<Object, Text, Text, TextPair> {
    private Text resultKey = new Text();
    private TextPair resultValue = new TextPair();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {
        String line = new String(value.toString());
        //drop null
        if (line == null || line.equals("")){
            return;
        }
        String[] split = line.split("\\|");

        resultKey.set(split[0]);
        resultValue.set(split[1], split[2]);
        context.write(resultKey, resultValue);
    }
}
