package algorithm.tagBasedRec;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/22
 *
 * Description：create association between item and users/tags
 *
 * Input：sep = "|"
 *      item|user
 *   or item|tag
 *
 * Output：
 *      key：item
 *      value：user/tag
 *
 */
public class ItemDiffuseMapper extends Mapper<Object, Text, Text, Text> {
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

        resultKey.set(split[0]);
        resultValue.set(split[1]);

        context.write(resultKey, resultValue);
    }
}
