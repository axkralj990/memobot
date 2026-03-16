# Discord Bot Setup Instructions

## 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under "Privileged Gateway Intents", enable:
   - ✅ MESSAGE CONTENT INTENT (required to read message content)
6. Copy the bot token and add it to `.env`:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```

## 2. Invite Bot to Your Server

1. In the Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

## 3. Get Channel ID

1. In Discord, enable Developer Mode:
   - Settings → Advanced → Developer Mode (toggle on)
2. Right-click on the channel you want the bot to listen to
3. Click "Copy Channel ID"
4. Add it to `.env`:
   ```
   DISCORD_CHANNEL_ID=123456789012345678
   ```

## 4. Run the Bot

```bash
uv run python -m src.discord_bot
```

## Usage

Once running, simply send a message in the configured channel:

```
Yesterday I slept 7 hours, had 2 coffees, feeling anxious (maybe a 4), 
took my omega3 and vitamins, went for a cold shower for 5 minutes
```

The bot will parse it and reply with a summary of the extracted data.
