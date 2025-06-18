CREATE TABLE listening_events (
    event_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    song_id UUID NOT NULL,
    event_type VARCHAR(20) NOT NULL, -- 'play', 'skip', 'like', 'share'
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    context JSONB, -- Lưu thêm metadata: device, IP, location
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id)
) PARTITION BY RANGE (timestamp);

CREATE INDEX idx_listening_events_user ON listening_events(user_id);
CREATE INDEX idx_listening_events_song ON listening_events(song_id);

CREATE TABLE user_interactions (
    interaction_id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    target_id UUID NOT NULL, -- ID bài hát/playlist/artist
    target_type VARCHAR(10) NOT NULL, -- 'song', 'playlist', 'artist'
    action VARCHAR(20) NOT NULL, -- 'like', 'repost', 'follow'
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (user_id, target_id, target_type, action) -- Tránh trùng lặp
);

-- Index hiệu suất
CREATE INDEX idx_interactions_user ON user_interactions(user_id);
CREATE INDEX idx_interactions_target ON user_interactions(target_id, target_type);