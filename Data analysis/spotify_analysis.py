from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

def create_spark_session():
    return SparkSession.builder \
        .appName("Spotify Analysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
        .getOrCreate()

def read_kafka_stream(spark, topic):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", topic) \
        .option("startingOffsets", "earliest") \
        .load()

def parse_artist_data(df):
    # Define schema for artist data
    artist_schema = StructType([
        StructField("id", StringType()),
        StructField("name", StringType()),
        StructField("popularity", IntegerType()),
        StructField("followers", StructType([
            StructField("total", LongType())
        ])),
        StructField("genres", ArrayType(StringType())),
        StructField("timestamp", StringType())
    ])
    
    # Parse JSON data
    return df.select(
        from_json(col("value").cast("string"), artist_schema).alias("data")
    ).select("data.*")

def analyze_artists(artist_df):
    # 1. Phân tích độ phổ biến
    popularity_analysis = artist_df \
        .select("name", "popularity", "followers.total") \
        .orderBy(desc("popularity"))
    
    # 2. Phân tích thể loại nhạc
    genre_analysis = artist_df \
        .select(explode("genres").alias("genre")) \
        .groupBy("genre") \
        .count() \
        .orderBy(desc("count"))
    
    # 3. Phân tích số lượng người theo dõi
    followers_analysis = artist_df \
        .select("name", "followers.total") \
        .orderBy(desc("followers.total"))
    
    return {
        "popularity": popularity_analysis,
        "genres": genre_analysis,
        "followers": followers_analysis
    }

def main():
    # Tạo Spark session
    spark = create_spark_session()
    
    # Đọc dữ liệu từ Kafka
    artist_stream = read_kafka_stream(spark, "spotify_data_artists")
    
    # Parse dữ liệu
    parsed_artists = parse_artist_data(artist_stream)
    
    # Thực hiện phân tích
    analysis_results = analyze_artists(parsed_artists)
    
    # Lưu kết quả phân tích
    # 1. Độ phổ biến
    popularity_query = analysis_results["popularity"] \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    # 2. Phân tích thể loại
    genre_query = analysis_results["genres"] \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    # 3. Phân tích người theo dõi
    followers_query = analysis_results["followers"] \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()
    
    # Đợi các query hoàn thành
    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main() 