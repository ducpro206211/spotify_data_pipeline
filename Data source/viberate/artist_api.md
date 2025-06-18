# Viberate Artist Data Crawler

## Overview
Crawler này được thiết kế để thu thập dữ liệu nghệ sĩ từ Viberate API, một nền tảng thống kê và phân tích dữ liệu nghệ sĩ toàn cầu.

## Data Sources
- **Viberate API**: Nguồn dữ liệu chính
  - Endpoint: `https://api.viberate.com/v1/artists/{artist_slug}`
  - Authentication: API Key required
  - Rate Limit: 100 requests/minute

## Artist Information Collected

### 1. Basic Information
- Artist name
- Profile image
- Country of origin
- Main genres
- Sub-genres
- Profile creation date
- Trending status

### 2. Rankings
- Overall rank
- Country-specific rank
- Genre-specific rank
- Sub-genre rank

### 3. Social Media Presence
- Spotify
  - Overall rank
  - Country rank
  - Monthly listeners
  - Followers
- YouTube
  - Channel statistics
  - Video metrics
- Other platforms
  - Twitter
  - Instagram
  - TikTok
  - Facebook
  - SoundCloud
  - Deezer
  - Apple Music

### 4. Analytics
- Spotify analytics
- YouTube analytics
- Social media analytics
- Airplay analytics
- Streaming analytics

### 5. Performance Metrics
- Monthly listeners
- Total streams
- Engagement rates
- Growth metrics
- Cross-platform performance

## Data Structure
```json
{
  "basic_info": {
    "name": "string",
    "image": "string",
    "country": "string",
    "genres": ["string"],
    "subgenres": ["string"],
    "created_at": "datetime",
    "is_trending": "boolean"
  },
  "rankings": {
    "overall": "integer",
    "country": "integer",
    "genre": "integer",
    "subgenre": "integer"
  },
  "social_media": {
    "spotify": {
      "rank": "integer",
      "country_rank": "integer",
      "monthly_listeners": "integer",
      "followers": "integer"
    },
    "youtube": {
      "subscribers": "integer",
      "views": "integer"
    }
  },
  "analytics": {
    "spotify": {
      "available": "boolean",
      "metrics": "object"
    },
    "youtube": {
      "available": "boolean",
      "metrics": "object"
    }
  }
}
```
