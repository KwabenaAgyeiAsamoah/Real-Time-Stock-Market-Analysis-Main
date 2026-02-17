from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType
from pyspark.sql.functions import from_json, col
import os
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.types import DoubleType

# directory where Spark will store its checkpoint data. crucial in streaming to enable fault tolerance
checkpoint_dir = "/tmp/checkpoint/stock_prices_to_postgres"
if not os.path.exists(checkpoint_dir):
  os.makedirs(checkpoint_dir)


postgres_config = {
    "url": "jdbc:postgresql://postgres:5432/stock_data",
    "dbtable": "public.stocks",
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}


# The schema/structure matching the new data coming from Kafka
kafka_data_schema = StructType([
  StructField("date", StringType()), 
  StructField("high", StringType()),
  StructField("low", StringType()),
  StructField("open", StringType()),
  StructField("close", StringType()),
  StructField("symbol", StringType())
])

spark = (
    SparkSession.builder
    .appName("KafkaSparkStreaming")
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
    .getOrCreate()
)

kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "stock_prices")
    .option("startingOffsets", "earliest")
    .load()
)


# Convert the 'value' column (which is a JSON string) into structured columns
parsed_df = kafka_df.selectExpr( 'CAST(value AS STRING)') \
              .select(from_json(col("value"), kafka_data_schema).alias("data")) \
              .select("data.*")

processed_df = parsed_df.select(
    to_timestamp(col("date")).alias("date"),
    col("open").cast(DoubleType()).alias("open"),
    col("high").cast(DoubleType()).alias("high"),
    col("low").cast(DoubleType()).alias("low"),
    col("close").cast(DoubleType()).alias("close"),
    col("symbol").alias("symbol"),
)

def write_to_postgres(batch_df, batch_id):
    """
    Writes a microbatch DataFrame to PostgreSQL using JDBC in 'append' mode.
    """
    print(f"Writing batch {batch_id} with {batch_df.count()} rows")
    
    batch_df.write \
        .format("jdbc") \
        .mode("append") \
        .options(**postgres_config) \
        .save()

# --- Stream to PostgreSQL using foreachBatch ---
query = (
  processed_df.writeStream
  .foreachBatch(write_to_postgres) # Use foreachBatch for JDBC sinks
  .option('checkpointLocation', checkpoint_dir)  # directory where Spark will store its checkpoint data. crucial in streaming to enable fault tolerance
  .outputMode('append') # Or 'append', depending on your use case and table schema
  .start()
)



# Wait for the termination of the query
query.awaitTermination()
