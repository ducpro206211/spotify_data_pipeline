-- Insert sample users
INSERT INTO users.user_profiles (username, email, country, is_premium) VALUES
    ('john_doe', 'john@example.com', 'US', true),
    ('jane_smith', 'jane@example.com', 'UK', false),
    ('music_lover', 'music@example.com', 'JP', true);

-- Insert sample artists
INSERT INTO music.artists (name, genres, popularity) VALUES
    ('Taylor Swift', ARRAY['Pop', 'Country'], 95),
    ('Ed Sheeran', ARRAY['Pop', 'Folk'], 90),
    ('BTS', ARRAY['K-Pop', 'Pop'], 88);

-- Insert sample albums
INSERT INTO music.albums (artist_id, title, release_date, total_tracks) VALUES
    (1, 'Folklore', '2020-07-24', 16),
    (2, 'Divide', '2017-03-03', 12),
    (3, 'Map of the Soul: 7', '2020-02-21', 20);

-- Insert sample tracks
INSERT INTO music.tracks (album_id, title, duration_ms, popularity) VALUES
    (1, 'Cardigan', 239000, 85),
    (1, 'The 1', 210000, 82),
    (2, 'Shape of You', 235000, 95),
    (2, 'Castle on the Hill', 265000, 88),
    (3, 'ON', 270000, 90),
    (3, 'Black Swan', 198000, 87);

-- Insert sample playlists
INSERT INTO playlists.playlists (user_id, name, description, is_public) VALUES
    (1, 'My Favorites', 'My favorite songs', true),
    (2, 'Workout Mix', 'Songs for working out', true),
    (3, 'Chill Vibes', 'Relaxing music', false);

-- Insert sample playlist tracks
INSERT INTO playlists.playlist_tracks (playlist_id, track_id, position) VALUES
    (1, 1, 1),
    (1, 3, 2),
    (2, 5, 1),
    (2, 6, 2),
    (3, 2, 1),
    (3, 4, 2);

-- Insert sample listening history
INSERT INTO analytics.user_listening_history (user_id, track_id, duration_played_ms) VALUES
    (1, 1, 239000),
    (1, 3, 235000),
    (2, 5, 270000),
    (3, 2, 210000);

-- Insert sample daily stats
INSERT INTO analytics.daily_streaming_stats (user_id, date, total_tracks_played, total_duration_ms) VALUES
    (1, CURRENT_DATE, 2, 474000),
    (2, CURRENT_DATE, 1, 270000),
    (3, CURRENT_DATE, 1, 210000); 