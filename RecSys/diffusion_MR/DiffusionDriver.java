package algorithm.tagBasedRec;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;
import org.apache.log4j.Logger;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

import java.io.IOException;
import java.net.URI;
import java.util.Iterator;
import java.util.List;
import java.util.Properties;

/**
 * Created by ZhengYaolin on 2016/11/23.
 *
 * Description: Diffusion Diver
 *
 * Note:
 *      1. diffusion between users and items
 *      2. diffusion between items and tags
 */
public class DiffusionDriver extends Configured implements Tool{
    private static final Logger log = Logger.getLogger(DiffusionDriver.class);
    private static final int REDUCE_NUM = 10;
    private static final double LAMBDA = 0.5;
    Properties params = new Properties();

    /**
     * Check if there is a file named fileName
     * @param fileName
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

    /**
     * Read parameters
     * @param args
     * @return true if read args successfully
     */
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

    /**
     * Run jobs
     */
    public int run(String[] args) throws IOException,
            InterruptedException, ClassNotFoundException {
        Configuration conf = new Configuration();
        if (!getParams(args)) return 1;

        log.info("Read config file success!");
        int reduceNum = params.containsKey("reduce_num") ? Integer.parseInt(params.getProperty("reduce_num")) : REDUCE_NUM;
        double lambda = params.containsKey("lambda") ? Double.parseDouble(params.getProperty("lambda")) : LAMBDA;

        String inputPath1 = params.getProperty("user_item_input");
        String inputPath2 = params.getProperty("item_tag_input");
        String inputPath3 = params.getProperty("user_item_orig");
        String outputPath = params.getProperty("resource_diffusion_output");
        String userOutput = outputPath + "/user_resource_output";
        String tagOutput = outputPath + "/tag_resource_output";
        String userItemOut = outputPath + "/user_item_result";
        String ItemTagOut = outputPath + "/item_tag_result";
        String finalDiffusion = outputPath + "/final_diffusion";
        String userResultTmp = outputPath + "/user_result_tmp";
        String userResult = outputPath + "/user_result";

        check(outputPath);

        /* 1. user-item diffusion */
        // 1.1 Resource diffuse from items to users
        Job job = Job.getInstance(conf, "item to user diffusion");
        job.setJarByClass(DiffusionDriver.class);           //Main
        job.setMapperClass(ItemDiffuseMapper.class);        //Mapper
        job.setReducerClass(ItemDiffuseReducer.class);      //Reducer
        job.setNumReduceTasks(reduceNum);                   //reduce num
        job.setInputFormatClass(TextInputFormat.class);     //input output type
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath1));    //input output path
        FileOutputFormat.setOutputPath(job, new Path(userOutput));
        //check(userOutput);
        if(job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Resource diffuse from items to users ********");
        } else
            return 1;

        // 1.2 Resource diffuse from users to items
        job = Job.getInstance(conf, "user-tag diffusion");
        job.setJarByClass(DiffusionDriver.class);                       //Main
        job.setReducerClass(BipartiteGraphDiffusionReducer.class);      //Reducer
        job.setNumReduceTasks(reduceNum);                               //reduce num
        MultipleInputs.addInputPath(job, new Path(userOutput), TextInputFormat.class, BipartiteGraphDiffusionMapper.class);
        MultipleInputs.addInputPath(job, new Path(inputPath1), TextInputFormat.class, BipartiteGraphDiffusionMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(TextPair.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileOutputFormat.setOutputPath(job, new Path(userItemOut));
        //check(userItemOut);
        if(job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Diffusion between items and users complete ********");
        } else
            return 1;

        /* 2. item-tag diffustion */
        // 2.1 Resource diffuse from items to tags
        job = Job.getInstance(conf, "item to tag diffusion");
        job.setJarByClass(DiffusionDriver.class);           //Main
        job.setMapperClass(ItemDiffuseMapper.class);        //Mapper
        job.setReducerClass(ItemDiffuseReducer.class);      //Reducer
        job.setNumReduceTasks(reduceNum);                   //reduce num
        job.setInputFormatClass(TextInputFormat.class);     //input output type
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileInputFormat.setInputPaths(job, new Path(inputPath2));    //input output path
        FileOutputFormat.setOutputPath(job, new Path(tagOutput));
        //check(tagOutput);
        if(job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Source diffuse from items to tags ********");
        } else
            return 1;

        // 2.2 Resource diffuse from tags to items
        job = Job.getInstance(conf, "item-tag diffusion");
        job.setJarByClass(DiffusionDriver.class);                       //Main
        job.setReducerClass(BipartiteGraphDiffusionReducer.class);      //Reducer
        job.setNumReduceTasks(reduceNum);                               //reduce num
        MultipleInputs.addInputPath(job, new Path(tagOutput), TextInputFormat.class, BipartiteGraphDiffusionMapper.class);
        MultipleInputs.addInputPath(job, new Path(inputPath2), TextInputFormat.class, BipartiteGraphDiffusionMapper.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(TextPair.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileOutputFormat.setOutputPath(job, new Path(ItemTagOut));
        //check(ItemTagOut);
        if(job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Diffusion between items and tags complete ********");
        } else
            return 1;

        /* 3. integrate diffusions */
        conf = new Configuration(getConf());
        conf.set("lambda", Double.toString(lambda));
        job = Job.getInstance(conf, "integrate diffusions");
        job.setJarByClass(DiffusionDriver.class);                   //Main
        job.setReducerClass(DiffusionIntegrateReducer.class);       //Reducer
        job.setNumReduceTasks(reduceNum);                           //reduce num
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(TextPair.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        MultipleInputs.addInputPath(job, new Path(userItemOut), TextInputFormat.class, DiffusionIntegrateMapper1.class);
        MultipleInputs.addInputPath(job, new Path(ItemTagOut), TextInputFormat.class, DiffusionIntegrateMapper2.class);
        FileOutputFormat.setOutputPath(job, new Path(finalDiffusion));
        //check(finalDiffusion);
        if(job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Merge item-tag diffusion result ********");
        } else
            return 1;

        /* 4. get diffusion result for every user */
        // 4.1 get user result tmp
        conf = new Configuration(getConf());
        job = Job.getInstance(conf, "get user diffusion result tmp");
        job.setJarByClass(DiffusionDriver.class);
        job.setNumReduceTasks(reduceNum);
        MultipleInputs.addInputPath(job, new Path(inputPath3), TextInputFormat.class, ItemUserMapper.class);
        MultipleInputs.addInputPath(job, new Path(finalDiffusion), TextInputFormat.class, ItemItemMapper.class);
        job.setReducerClass(UserDiffusionResultReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(TextPair.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileOutputFormat.setOutputPath(job, new Path(userResultTmp));
        //check(userResultTmp);
        if (job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Get user diffusion result tmp ********");
        } else
            return 1;

        // 4.2 merge user result
        job = Job.getInstance(conf, "get user diffusion result");
        job.setJarByClass(DiffusionDriver.class);
        job.setNumReduceTasks(reduceNum);
        job.setMapperClass(MergeUserResultMapper.class);
        job.setReducerClass(MergeUserResultReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(NullWritable.class);
        FileInputFormat.setInputPaths(job, new Path(userResultTmp));
        FileOutputFormat.setOutputPath(job, new Path(userResult));
        //check(userResult);
        if (job.waitForCompletion(true)) {
            log.info("job[" + job.getJobID() + "] complete!");
            log.info("********* Get user diffusion result ********");
        } else
            return 1;

        return 0;
    }


    public static void main(String[] args) throws Exception{
        int runCode = ToolRunner.run(new DiffusionDriver(), args);
        System.exit(runCode);
    }
}

