package algorithm.tagBasedRec;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/11/23.
 *
 * Description: diffusion between items and users/tags
 *
 * Input: sep = "|"
 *      1. item|user
 *      2. item|user|resource
 *  or
 *      1.item|tag
 *      2.item|tag|resource
 *
 * Output:
 *      key: user/tag
 *      value:  1:<item, flag>   2:<(item, resource), flag>
 *
 * Note: this is a multi-input mapper
 */
public class BipartiteGraphDiffusionMapper extends Mapper<Object, Text, Text, TextPair>{
    private Text resultKey = new Text();
    private TextPair item = new TextPair();

    public void map(Object key, Text value, Mapper.Context context)
            throws IOException, InterruptedException {
        //read data
        String line = new String(value.toString());

        //drop null
        if (line == null || line.equals("")){
            return;
        }

        String[] str = line.split("\\|");
        int n = str.length;

        if (n == 2) {
            resultKey.set(str[1]);
            item.setFirst(str[0]);
            item.setSecond("1");
        } else if (n == 3) {
            resultKey.set(str[1]);
            item.setFirst(str[0] + "," + str[2]);
            item.setSecond("2");
        } else {
            throw new IOException("Bad Input!");
        }

        context.write(resultKey, item);
    }
}
