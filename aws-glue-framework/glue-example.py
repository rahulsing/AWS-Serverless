import sys
import pyspark
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SQLContext
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME]
#args = getResolvedOptions(sys.argv, ['JOB_NAME'])
args = getResolvedOptions(sys.argv, ['JOB_NAME','REPARTITION_COUNT','WRITE_MODE','DEST_FOLDER','FORMAT'])

sc = pyspark.SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
sqlContext = SQLContext(sc)


job = Job(glueContext)
job.init(args['JOB_NAME'], args)

part_count=args['REPARTITION_COUNT']
write_mode=args['WRITE_MODE']
dest_folder=args['DEST_FOLDER']
out_format=args['FORMAT']

print('part_count:'+part_count)
print('write_mode:'+write_mode)
print('dest_folder:'+dest_folder)
print('out_format:'+out_format)


customer = glueContext.create_dynamic_frame.from_catalog(database = "sf_tpch_sf001", table_name = "customer")
lineitem = glueContext.create_dynamic_frame.from_catalog(database = "sf_tpch_sf001", table_name = "lineitem")
orders = glueContext.create_dynamic_frame.from_catalog(database = "sf_tpch_sf001", table_name = "orders")


df_customer = customer.toDF()
df_customer.registerTempTable('tbl_customer')

df_lineitem = lineitem.toDF()
df_lineitem.registerTempTable('tbl_lineitem')

df_orders = orders.toDF()
df_orders.registerTempTable('tbl_orders')

df_result = sqlContext.sql('select c.c_custkey as cust_key,sum(o.o_totalprice) as total_price from tbl_customer c inner join tbl_orders o on c.c_custkey=o.o_custkey group by c.c_custkey')

df_result.count()




#glue_df_result=DynamicFrame.fromDF(df_result, glueContext,"glue_df_result")
#glueContext.write_dynamic_frame.from_options(frame = glue_df_result, connection_type = "s3",connection_options = {"path": "s3://rlnusnowflakestage/glue_transformed"},format = "csv")

print('No of partitions: ' + str(df_result.rdd.getNumPartitions()))


df_result.coalesce(3).write.mode(write_mode).format(out_format).save(dest_folder)
