package algorithm.tagBasedRec;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/24.
 *
 * Description: merge item resource for every user
 *
 * input:
 *      user|item|resource
 *
 * output:
 *      key: user|item
 *      value: resource
 */

public class MergeUserResultMapper extends Mapper<Object, Text, Text, Text>{
    private Text resultKey = new Text();
    private Text resultValue = new Text();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {
        String line = new String(value.toString());
        //drop null
        if (line == null || line.equals("")){
            return;
        }
        String[] split = line.split("\\|");

        resultKey.set(split[0] + "|" + split[1]);
        resultValue.set(split[2]);

        context.write(resultKey, resultValue);
    }
}
