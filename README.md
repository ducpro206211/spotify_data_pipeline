# Spotify Data Pipeline

Pipeline đơn giản để lấy dữ liệu từ Spotify API và lưu trữ vào Redpanda.

## Cấu trúc thư mục

```
spotify_data_pipeline/
├── src/
│   └── spotify_producer.py
├── config/
├── .env
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Cài đặt

1. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

2. Cấu hình credentials trong file `.env`:
```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
REDPANDA_BROKERS=localhost:9092
```

## Chạy

1. Khởi động Redpanda:
```bash
docker-compose up -d
```

2. Chạy producer:
```bash
python src/spotify_producer.py
```

## Dữ liệu

Dữ liệu sẽ được lưu trong topic `spotify_playlists` trên Redpanda. Mỗi message chứa thông tin về một playlist từ Spotify. 