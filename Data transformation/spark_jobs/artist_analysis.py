from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

def create_spark_session():
    return SparkSession.builder \
        .appName("Spotify Artist Analysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
        .getOrCreate()

def read_kafka_stream(spark, topic):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

def parse_artist_data(df):
    # Parse JSON from Kafka message
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
    
    return df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

def analyze_artists(df):
    # 1. Popularity Analysis
    popularity_stats = df.select(
        mean("popularity").alias("avg_popularity"),
        max("popularity").alias("max_popularity"),
        min("popularity").alias("min_popularity")
    )
    
    # 2. Genre Analysis
    genre_counts = df.select(explode("genres").alias("genre")) \
        .groupBy("genre") \
        .count() \
        .orderBy(desc("count"))
    
    # 3. Follower Analysis
    follower_stats = df.select(
        mean("followers.total").alias("avg_followers"),
        max("followers.total").alias("max_followers"),
        min("followers.total").alias("min_followers")
    )
    
    return popularity_stats, genre_counts, follower_stats

def main():
    spark = create_spark_session()
    
    # Read from Kafka
    kafka_df = read_kafka_stream(spark, "spotify_data_artists")
    
    # Parse data
    artist_df = parse_artist_data(kafka_df)
    
    # Perform analysis
    popularity_stats, genre_counts, follower_stats = analyze_artists(artist_df)
    
    # Write results to console (for demonstration)
    query1 = popularity_stats.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    query2 = genre_counts.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    query3 = follower_stats.writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    # Wait for termination
    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main() 