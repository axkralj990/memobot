# Docker Deployment Guide

This guide covers building, pushing, and running the assistant bot in Docker.

## Prerequisites

- Docker installed locally (for building)
- Docker Hub account
- Docker installed on Synology NAS

## Building and Pushing to Docker Hub

### 1. Build the Image

```bash
cd /path/to/assistant
docker build -t yourusername/memobot:latest .
```

Replace `yourusername` with your Docker Hub username.

### 2. Test Locally (Optional)

```bash
docker run --rm \
  --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.pickle:/app/token.pickle \
  yourusername/memobot:latest
```

### 3. Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push the image
docker push yourusername/memobot:latest
```

## Running on Synology NAS

### Option 1: Docker Compose (Recommended)

The repository includes a ready-to-use `docker-compose.yml`.

**Setup:**

1. Copy the files to your Synology (e.g., `/volume1/docker/memobot/`)
2. Edit `docker-compose.yml`:
   - Replace `yourusername` with your Docker Hub username
   - Fill in all environment variables (tokens, IDs, etc.)
3. Place `credentials.json` and `token.pickle` in the same directory
4. Start the bot:
   ```bash
   docker-compose up -d
   ```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the bot:**
```bash
docker-compose down
```

### Option 2: Docker Run Command

```bash
docker run -d \
  --name memobot \
  --restart unless-stopped \
  -e DISCORD_TOKEN="your_discord_token" \
  -e DISCORD_CHANNEL_ID="your_channel_id" \
  -e NOTION_TOKEN="your_notion_token" \
  -e NOTION_DATABASE_ID="your_database_id" \
  -e OPENAI_API_KEY="your_openai_api_key" \
  -e TIMEZONE="Europe/Zagreb" \
  -e CALENDAR_IDS="primary" \
  -v /path/to/credentials.json:/app/credentials.json:ro \
  -v /path/to/token.pickle:/app/token.pickle:rw \
  yourusername/memobot:latest
```

### Option 3: Synology Docker UI

1. Open Docker app on Synology
2. Go to **Registry** → Search for your image → Download
3. Go to **Image** → Select your image → Launch
4. Configure:
   - **Container Name**: memobot
   - **Environment**: Add all env variables listed above
   - **Volume**: 
     - Mount `/your/synology/path/credentials.json` → `/app/credentials.json` (read-only)
     - Mount `/your/synology/path/token.pickle` → `/app/token.pickle` (read-write)
   - **Network**: Bridge (default)
   - **Restart Policy**: Unless stopped
5. Click **Apply** → **Next** → **Done**

## Important Files

### credentials.json
Your Google OAuth client credentials. Get from Google Cloud Console.

**Location on Synology**: `/volume1/docker/memobot/credentials.json`

### token.pickle
Generated after first OAuth authorization. Contains refresh token.

**First-time setup**:
1. Authorize on your Mac (has browser)
2. Copy `token.pickle` to Synology
3. Mount as volume (read-write so it can refresh)

**Location on Synology**: `/volume1/docker/memobot/token.pickle`

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DISCORD_TOKEN` | Yes | Discord bot token | `MTIzNDU2Nzg5MA...` |
| `DISCORD_CHANNEL_ID` | Yes | Channel ID for bot | `1234567890123456789` |
| `NOTION_TOKEN` | Yes | Notion integration secret | `ntn_xxx` |
| `NOTION_DATABASE_ID` | Yes | Notion database ID | `04f42963328a4d91...` |
| `OPENAI_API_KEY` | Yes | OpenAI API key | `sk-proj-xxx` |
| `TIMEZONE` | No | Your timezone | `Europe/Zagreb` |
| `CALENDAR_IDS` | No | Comma-separated calendar IDs | `primary,cal2@group.calendar.google.com` |

## Viewing Logs

```bash
# Via docker-compose
docker-compose logs -f memobot

# Via docker command
docker logs -f memobot
```

## Updating the Bot

```bash
# Pull latest image
docker pull yourusername/memobot:latest

# Restart container
docker-compose down && docker-compose up -d

# OR via docker command
docker stop memobot && docker rm memobot
# Then run the docker run command again
```

## Troubleshooting

### Container exits immediately
Check logs: `docker logs memobot`
Common issues:
- Missing environment variables
- Invalid Discord token
- Missing credentials.json

### Calendar not working
- Ensure `credentials.json` is mounted correctly
- Ensure `token.pickle` is mounted as **read-write** (not read-only)
- Check logs for OAuth errors

### "No such file or directory: credentials.json"
- Verify file path on Synology
- Verify volume mount in docker-compose.yml
- Check file permissions (should be readable by container)

### Bot doesn't respond to messages
- Check Discord permissions
- Verify `DISCORD_CHANNEL_ID` is correct
- Check logs for errors

## Security Notes

- Never commit `credentials.json` or `token.pickle` to git
- Store sensitive files in secure location on Synology
- Use strong passwords for Docker Hub if image is public
- Consider using Docker secrets for production deployments
- Regularly update the base image for security patches

## Building Multi-Architecture Images (Optional)

If you want to support both x86 Synology and ARM devices:

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t yourusername/memobot:latest \
  --push .
```
