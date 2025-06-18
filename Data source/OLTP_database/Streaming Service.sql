CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    premium_status BOOLEAN DEFAULT FALSE,
    country_code CHAR(2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ
);

-- Index cho tìm kiếm email và login
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_country ON users(country_code);

CREATE TABLE songs (
    song_id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id UUID NOT NULL,
    album_id UUID,
    duration_ms INTEGER NOT NULL,
    release_date DATE,
    genre VARCHAR(50),
    is_explicit BOOLEAN DEFAULT FALSE,
    spotify_uri VARCHAR(50) UNIQUE
);

-- Index cho tìm kiếm theo nghệ sĩ và album
CREATE INDEX idx_songs_artist ON songs(artist_id);
CREATE INDEX idx_songs_album ON songs(album_id);
-- Partition by month để dễ quản lý dữ liệu lớn
CREATE TABLE play_events (
    event_id BIGSERIAL,
    user_id UUID NOT NULL,
    song_id UUID NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    device_type VARCHAR(20),
    play_duration_ms INTEGER,
    skipped BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (event_id, timestamp)
) PARTITION BY RANGE (timestamp);

-- Tạo partition cho tháng hiện tại
CREATE TABLE play_events_2023_11 PARTITION OF play_events
    FOR VALUES FROM ('2023-11-01') TO ('2023-12-01');