import java.io.IOException;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;


public class Sum {
    public static class SumMapper extends Mapper<Object, Text, Text, IntWritable> {
        protected void map(Object key, Text csv_data, Context context) throws IOException, InterruptedException {
            String[] data = csv_data.toString().replace(" ", "").replace("\'", "").split(",");
            if (Float.parseFloat(data[2]) >= 20) {
                context.write(new Text(data[0]), new IntWritable(Integer.parseInt(data[3])));
            }
        }
    }


    public static class SumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
        private IntWritable sum_nursing_home_count = new IntWritable();
        public void reduce(Text province, Iterable<IntWritable> values, Context context
                    ) throws IOException, InterruptedException {
                        int sum = 0;
                        for (IntWritable val : values) {
                            sum += val.get();
                        }
                        sum_nursing_home_count.set(sum);
                        context.write(province, sum_nursing_home_count);
                    }
                }


    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        for (int i = 0; i < otherArgs.length; i++) {
            System.out.println(otherArgs[i]);
        }
        Job job = Job.getInstance(conf, "HW5");
        job.setJarByClass(Sum.class);
        job.setMapperClass(SumMapper.class);
        job.setReducerClass(SumReducer.class);

        job.setNumReduceTasks(1);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        for (int i = 0; i < otherArgs.length - 1; ++i) {
            FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
        }
        FileOutputFormat.setOutputPath(job,
                new Path(otherArgs[otherArgs.length - 1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}