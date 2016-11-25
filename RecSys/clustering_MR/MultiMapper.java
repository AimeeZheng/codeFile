package clustering;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.InputSplit;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import utils.TextPair;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/10/11.
 *
 * Description: multi-input
 *
 * Input: sep = "|"
 *      1. k+1-items sets
 *      2. 2-items sets
 * Output:
 *      key: last 2 users
 *      value: same users 1:k-1 2:""
 * Note:
 *      1. Inner join(key)   2.Result filting
 */

public class MultiMapper extends Mapper<Object, Text, Text, TextPair> {
    private Text pair = new Text();
    private TextPair sameU = new TextPair();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {

        //read data
        String line = new String(value.toString());
        //drop null
        if (line == null || line.equals("")){
            return;
        }
        String[] usrs = line.split("\\|");
        int n = usrs.length;
        String str = "";
        if(n == 2) {
            sameU.setFirst(new Text("orig"));
        } else if(n > 2) {
            for(int i = 2; i < n - 1; i++)
                str += usrs[i] + "|";
            str += usrs[n - 1];
            sameU.setFirst(new Text("clusted"));
        } else {
            throw new IOException("Bad Input!");
        }
        pair.set(usrs[0].compareTo(usrs[1]) < 0 ? usrs[0] + "|" + usrs[1] : usrs[1] + "|" + usrs[0]);
        sameU.setSecond(new Text(str));
        context.write(pair, sameU);
    }
}
