-- Users schema tables
CREATE TABLE IF NOT EXISTS users.user_profiles (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    country VARCHAR(2),
    is_premium BOOLEAN DEFAULT FALSE
);

-- Music schema tables
CREATE TABLE IF NOT EXISTS music.artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    genres TEXT[],
    popularity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS music.albums (
    album_id SERIAL PRIMARY KEY,
    artist_id INTEGER REFERENCES music.artists(artist_id),
    title VARCHAR(100) NOT NULL,
    release_date DATE,
    total_tracks INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS music.tracks (
    track_id SERIAL PRIMARY KEY,
    album_id INTEGER REFERENCES music.albums(album_id),
    title VARCHAR(100) NOT NULL,
    duration_ms INTEGER,
    popularity INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlists schema tables
CREATE TABLE IF NOT EXISTS playlists.playlists (
    playlist_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users.user_profiles(user_id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_public BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS playlists.playlist_tracks (
    playlist_id INTEGER REFERENCES playlists.playlists(playlist_id),
    track_id INTEGER REFERENCES music.tracks(track_id),
    position INTEGER,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, track_id)
);

-- Analytics schema tables
CREATE TABLE IF NOT EXISTS analytics.user_listening_history (
    history_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users.user_profiles(user_id),
    track_id INTEGER REFERENCES music.tracks(track_id),
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_played_ms INTEGER
);

CREATE TABLE IF NOT EXISTS analytics.daily_streaming_stats (
    stat_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users.user_profiles(user_id),
    date DATE,
    total_tracks_played INTEGER,
    total_duration_ms BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo schema mới
CREATE SCHEMA schema_name;

-- Xóa schema
DROP SCHEMA schema_name;

-- Xóa schema và tất cả các đối tượng trong nó
DROP SCHEMA schema_name CASCADE;

-- Liệt kê tất cả các schema
SELECT schema_name 
FROM information_schema.schemata;

-- Liệt kê tất cả các bảng trong một schema
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'schema_name';

-- Tạo bảng trong schema cụ thể
CREATE TABLE schema_name.table_name (
    column1 datatype,
    column2 datatype
);

-- Truy vấn dữ liệu từ bảng trong schema
SELECT * FROM schema_name.table_name;

-- Thêm dữ liệu vào bảng trong schema
INSERT INTO schema_name.table_name (column1, column2) 
VALUES (value1, value2); 