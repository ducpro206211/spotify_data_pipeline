# Spotify OLTP Database Setup

This directory contains the setup for a PostgreSQL database that simulates Spotify's OLTP (Online Transaction Processing) system.

## Database Structure

The database is organized into the following schemas:

1. `users` - User profile information
2. `music` - Music catalog (artists, albums, tracks)
3. `playlists` - User playlists and playlist contents
4. `analytics` - User listening history and streaming statistics

## Setup Instructions

1. Make sure you have Docker and Docker Compose installed on your system.

2. Start the database:
```bash
docker-compose up -d
```

3. Connect to the database:
```bash
psql -h localhost -U spotify_user -d spotify_oltp
```
Password: spotify_password

## Database Schema Details

### Users Schema
- `user_profiles`: Stores user account information

### Music Schema
- `artists`: Artist information
- `albums`: Album information
- `tracks`: Track information

### Playlists Schema
- `playlists`: User playlist information
- `playlist_tracks`: Tracks in each playlist

### Analytics Schema
- `user_listening_history`: Individual track plays
- `daily_streaming_stats`: Daily streaming statistics per user

## Initialization Scripts

The database is automatically initialized with the following scripts:
1. `01_create_schemas.sql`: Creates all necessary schemas
2. `02_create_tables.sql`: Creates all tables with proper relationships

## Stopping the Database

To stop the database:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
``` 