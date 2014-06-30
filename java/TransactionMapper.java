package edu.sdsc.map_reduce_demo_test;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

// a transaction contains these fields:
// transactionId, productId, userId, purchaseAmount, productDescription
// data is tab delimited
// 

public class TransactionMapper extends Mapper<LongWritable, Text, TextTuple, TextTuple> {
  TextTuple outKey = new TextTuple();
  TextTuple outValue = new TextTuple();
  
  @Override  
  public void map(LongWritable key, Text value, Context context) 
  throws java.io.IOException, InterruptedException {
    String[] record = value.toString().split("\t");
    String productId = record[2];
    String uid = record[0];
    outKey.set(uid, "b");
    outValue.set("transaction", productId);
    context.write(outKey, outValue);
  }

}