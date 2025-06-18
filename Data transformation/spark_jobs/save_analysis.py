from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from datetime import datetime

def create_spark_session():
    return SparkSession.builder \
        .appName("Spotify Analysis Storage") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
        .getOrCreate()

def save_analysis_results(df, analysis_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as Parquet (columnar format, good for analytics)
    df.write \
        .mode("overwrite") \
        .parquet(f"/app/data/{analysis_type}_{timestamp}.parquet")
    
    # Save as JSON (for easy viewing)
    df.write \
        .mode("overwrite") \
        .json(f"/app/data/{analysis_type}_{timestamp}.json")

def main():
    spark = create_spark_session()
    
    # Read from Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "spotify_data_artists") \
        .option("startingOffsets", "earliest") \
        .load()
    
    # Parse JSON data
    schema = StructType([
        StructField("id", StringType()),
        StructField("name", StringType()),
        StructField("popularity", IntegerType()),
        StructField("followers", StructType([
            StructField("total", LongType())
        ])),
        StructField("genres", ArrayType(StringType())),
        StructField("timestamp", StringType())
    ])
    
    artist_df = kafka_df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Perform different types of analysis
    # 1. Popularity Analysis
    popularity_stats = artist_df.select(
        mean("popularity").alias("avg_popularity"),
        max("popularity").alias("max_popularity"),
        min("popularity").alias("min_popularity")
    )
    
    # 2. Genre Analysis
    genre_counts = artist_df.select(explode("genres").alias("genre")) \
        .groupBy("genre") \
        .count() \
        .orderBy(desc("count"))
    
    # 3. Follower Analysis
    follower_stats = artist_df.select(
        mean("followers.total").alias("avg_followers"),
        max("followers.total").alias("max_followers"),
        min("followers.total").alias("min_followers")
    )
    
    # Save results
    save_analysis_results(popularity_stats, "popularity")
    save_analysis_results(genre_counts, "genres")
    save_analysis_results(follower_stats, "followers")
    
    # Start streaming query
    query = artist_df.writeStream \
        .outputMode("complete") \
        .foreachBatch(lambda batch_df, batch_id: save_analysis_results(batch_df, f"raw_data_{batch_id}")) \
        .start()
    
    # Wait for termination
    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main() 