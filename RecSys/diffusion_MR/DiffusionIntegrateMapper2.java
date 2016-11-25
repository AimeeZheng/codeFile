package algorithm.tagBasedRec;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/23
 *
 * Input：
 *      item|item|resource
 *
 * Output：
 *      key：item|item
 *      value：<resource, 2>
 *
 * Note: item-tag diffusion result
 *
 */
public class DiffusionIntegrateMapper2 extends Mapper<Object, Text, Text, TextPair> {
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

        resultKey.set(split[0] + "|" + split[1]);
        resultValue.set(split[2], "2");
        context.write(resultKey, resultValue);
    }
}
