package clustering;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/10/8.
 *
 * Description：set split
 *
 * Input：sep = "|"
 *      k-items sets（ascending）
 * Output：
 *      key：k-1 users (sep = "|")
 *      value：k users
 * Note: using phone number represent every user
 *
 */
public class SplitMapper extends Mapper<Object, Text, Text, Text> {
    private Text sameU = new Text();
    private Text lastU = new Text();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {
        String line = new String(value.toString());
        //drop null
        if (line == null || line.equals("")){
            return;
        }
        String[] phoNums = line.split("\\|");

        //k-items
        int k = phoNums.length;
        if(k == 2) {
            //2-items set (sort ascending)
            if(phoNums[0].compareTo(phoNums[1]) < 0) {
                sameU.set(phoNums[0]);
                lastU.set(phoNums[1]);
            } else {
                sameU.set(phoNums[1]);
                lastU.set(phoNums[0]);
            }
        } else if(k > 2) {
            //k-items set (ascending)
            String usrs = "";
            for(int i = 0; i < k - 2; i++) {
                String u = phoNums[i];
                if(u != null && !u.isEmpty()) {
                    usrs += u + "|";
                }
            }
            usrs += phoNums[k - 2];
            sameU.set(usrs);
            lastU.set(phoNums[k - 1]);
        } else {
            throw new IOException("Input Data Wrong！");
        }

        context.write(sameU, lastU);
    }
}
