package clustering;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.Logger;

import java.io.IOException;
import java.net.URI;
import java.util.List;
import java.util.Properties;
import java.util.Iterator;
import utils.TextPair;

import org.dom4j.io.SAXReader;
import org.dom4j.Document;
import org.dom4j.Element;
import org.dom4j.DocumentException;

/**
 * Created by ZhengYaolin on 2016/10/8.
 */
public class ClusteringDriver extends Configured implements Tool{
    private static final Logger log = Logger.getLogger(ClusteringDriver.class);
    private static final int REDUCE_NUM = 10;
    private static final int MAX_K = 5;
    Properties params = new Properties();
    /**
     * Clustering Diver
     *
     */

    public void check(String fileName) {
        try {
            FileSystem fs = FileSystem.get(URI.create(fileName), new Configuration());
            Path f = new Path(fileName);
            boolean isExists = fs.exists(f);
            if (isExists) {    //if exists, delete
                boolean isDel = fs.delete(f, true);
                log.info(fileName + "  delete?\t" + isDel);
            } else {
                log.info(fileName + "  exist?\t" + isExists);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public boolean getParams(String[] args) {
        // Read Parameters from config file
        String configFilePath = args[0];
        SAXReader reader = new SAXReader();
        Document doc;
        try {
            doc = reader.read(configFilePath);
            List nodes = doc.getRootElement().elements("param");
            for (Iterator iter = nodes.iterator(); iter.hasNext(); ) {
                Element element = (Element) iter.next();
                String name = element.attributeValue("name");
                String value = element.getText();
                if (name == null || name.trim().isEmpty()) {
                    continue;
                }
                params.put(name, value);
            }
        } catch (DocumentException e) {
            String errorDesc = String.format("Read config file failed.[File:%s, Reason: %s]", configFilePath, e.getMessage());
            log.error(errorDesc);
            return false;
        }
        return true;
    }

    public int run(String[] args) throws IOException,
            InterruptedException, ClassNotFoundException {
        Configuration conf = new Configuration();
        if (!getParams(args)) return 1;

        log.info("Read config file success!");
        int reduceNum = params.containsKey("reduce_num") ? Integer.parseInt(params.getProperty("reduce_num")) : REDUCE_NUM;
        int maxK = params.containsKey("max_k") ? Integer.parseInt(params.getProperty("max_k")) : MAX_K;
        String s2Path = params.getProperty("s2_input");
        String dataPath = params.getProperty("iptv_family_clustering_data_path");

        Job job;
        int k = 2;

        String inputPath;
        String outputPath;
        while(k < maxK) {
            if (k == 2)
                inputPath = s2Path;
            else
                inputPath = dataPath + "/S" + k;
            outputPath = dataPath + "/result_tmp";
            job = Job.getInstance(conf, "clustering");
            job.setJarByClass(ClusteringDriver.class);  //Main
            job.setMapperClass(SplitMapper.class);      //Mapper
            job.setReducerClass(ClusterReducer.class);  //Reducer
            job.setNumReduceTasks(reduceNum);           //reduce num
            job.setInputFormatClass(TextInputFormat.class);     //input output type
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(Text.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(NullWritable.class);
            FileInputFormat.addInputPath(job, new Path(inputPath)); //input output path
            FileOutputFormat.setOutputPath(job, new Path(outputPath));
            check(outputPath);
            if(job.waitForCompletion(true))
                log.info("job[" + job.getJobID() + "] complete!");
            else
                return 1;

            inputPath = outputPath;
            outputPath = dataPath + "/S" + (k+1);
            job = Job.getInstance(conf, "filting");
            job.setJarByClass(ClusteringDriver.class);
            job.setMapperClass(MultiMapper.class);
            job.setReducerClass(FiltReducer.class);
            job.setNumReduceTasks(reduceNum);
            MultipleInputs.addInputPath(job, new Path(inputPath), TextInputFormat.class, MultiMapper.class);
            MultipleInputs.addInputPath(job, new Path(s2Path), TextInputFormat.class, MultiMapper.class);
            FileOutputFormat.setOutputPath(job, new Path(outputPath));
            job.setMapOutputKeyClass(Text.class);
            job.setMapOutputValueClass(TextPair.class);
            job.setOutputKeyClass(Text.class);
            job.setOutputValueClass(NullWritable.class);
            check(outputPath);
            if(job.waitForCompletion(true)) {
                log.info("job[" + job.getJobID() + "] complete!");
                log.info("Clustering complete: " + k + "-sets have been clusted to " + (k+1) + "-sets!!!");
            }
            else
                return 1;

            k++;
        }
        return 0;
    }

    public static void main(String[] args) throws Exception{
        int runCode = ToolRunner.run(new ClusteringDriver(), args);
        System.exit(runCode);
    }
}

