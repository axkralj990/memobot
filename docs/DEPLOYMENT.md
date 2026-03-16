# 🚀 Deployment Guide: Raspberry Pi Zero Feasibility

## Raspberry Pi Zero Specs
- **CPU**: Single-core 1GHz ARM11
- **RAM**: 512MB
- **Storage**: SD card
- **Network**: WiFi (Zero W) or requires USB adapter

## Resource Analysis

### ✅ What's LIGHTWEIGHT about this app

1. **No Local AI Models** 🎯
   - All AI processing happens on OpenAI servers
   - All data storage happens on Notion servers
   - App just orchestrates API calls
   - Minimal CPU usage

2. **Simple Architecture** 🎯
   - No database to run locally
   - No background jobs
   - No heavy computation
   - Just Python + HTTP requests

3. **Event-Driven** 🎯
   - Only active when messages received
   - Idle most of the time
   - No continuous polling

### ⚠️ What's POTENTIALLY HEAVY

1. **Discord.py Library** ⚠️
   - Maintains WebSocket connection
   - Can use 50-100MB RAM
   - Event loop overhead

2. **Python Runtime** ⚠️
   - Base Python: ~20-30MB
   - With libraries: ~100-150MB total
   - Not optimized for embedded systems

3. **Dependencies** ⚠️
   - discord.py (heavy)
   - openai (lightweight)
   - pydantic (medium)
   - requests (lightweight)

## Memory Usage Estimate

```
Base Python:           ~30 MB
discord.py:            ~70 MB
openai + requests:     ~20 MB
pydantic:              ~15 MB
Your code:             ~5 MB
OS overhead:           ~50 MB
────────────────────────────
TOTAL (idle):          ~190 MB
TOTAL (active):        ~250 MB
```

## Raspberry Pi Zero: VERDICT

### 🟡 BORDERLINE FEASIBLE

**Will it run?** YES, but with caveats ⚠️

**Performance:**
- Startup: SLOW (30-60 seconds)
- Response time: ACCEPTABLE (2-5 seconds)
- Stability: DECENT (if no memory leaks)
- RAM usage: ~40-50% of 512MB

### Issues You'll Face

1. **Slow Startup** 🐌
   - Cold boot: 30-60 seconds
   - Python import overhead significant on ARM11

2. **Memory Pressure** 🧠
   - ~190MB idle = 38% of RAM
   - ~250MB active = 50% of RAM
   - Little room for spikes
   - Swap will be SLOW on SD card

3. **Network Latency** 🌐
   - WiFi on Pi Zero can be flaky
   - Reconnection delays
   - Potential disconnects

4. **SD Card Wear** 💾
   - Logging to SD = faster wear
   - Recommend minimal logging
   - Consider read-only filesystem

## Better Alternatives

### Raspberry Pi 3/4 ✅ RECOMMENDED
- 1GB+ RAM
- Quad-core CPU
- Much better WiFi
- Cost: ~$35-55

**Verdict**: Smooth sailing, no issues

### Raspberry Pi Zero 2 W 🟢 GOOD OPTION
- Quad-core 1GHz
- 512MB RAM (same as Zero)
- Better CPU = faster startup
- Cost: ~$15

**Verdict**: Works well, minor delays

### VPS/Cloud (Free Tier) ✅ BEST FOR RELIABILITY
- Oracle Cloud: Free ARM instance (4GB RAM)
- AWS EC2 t4g.micro: Free tier (1GB RAM)
- Always online
- Better network
- No SD card wear

**Verdict**: Professional setup, zero hassle

## Optimization for Pi Zero

If you MUST use Pi Zero, optimize:

### 1. Reduce Memory Usage

```python
# In discord_bot.py, reduce cache
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Only what you need
# Disable unnecessary intents:
intents.members = False
intents.presences = False
```

### 2. Limit Discord Cache

```python
# Add to DailyLogBot.__init__
super().__init__(
    command_prefix="!",
    intents=intents,
    max_messages=50,  # Limit message cache
    chunk_guilds_at_startup=False
)
```

### 3. Use Lighter Python

```bash
# Use Python 3.11 (more efficient than 3.9/3.10)
sudo apt install python3.11 python3.11-venv
```

### 4. Reduce Logging

```python
# Only log errors, not info
import logging
logging.basicConfig(level=logging.ERROR)
```

### 5. Enable Swap (for safety)

```bash
# Create 1GB swap (slow but prevents crashes)
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

## Installation on Pi Zero

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11 (if available)
sudo apt install python3.11 python3.11-venv python3-pip -y

# 3. Install uv (faster than pip)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Clone repo
git clone <your-repo-url>
cd assistant

# 5. Create .env
cp .env.example .env
nano .env  # Add your keys

# 6. Install dependencies
uv sync

# 7. Test it
uv run main.py

# 8. If works, setup systemd service for auto-start
```

## Systemd Service (Auto-start on Boot)

```bash
# Create service file
sudo nano /etc/systemd/system/daily-log-bot.service
```

```ini
[Unit]
Description=Daily Log Discord Bot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/assistant
ExecStart=/home/pi/assistant/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment="PATH=/home/pi/assistant/.venv/bin:/usr/local/bin:/usr/bin"

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable daily-log-bot
sudo systemctl start daily-log-bot

# Check status
sudo systemctl status daily-log-bot
```

## Monitoring on Pi Zero

```bash
# Check memory usage
free -h

# Check CPU usage
top

# Check bot status
sudo systemctl status daily-log-bot

# View logs
sudo journalctl -u daily-log-bot -f
```

## Expected Performance

### Startup Time
- Pi Zero: 30-60 seconds ⚠️
- Pi Zero 2 W: 15-30 seconds 🟡
- Pi 3/4: 5-10 seconds ✅

### Response Time
- API latency: 1-3 seconds (same on all)
- Processing: <1 second (negligible)
- **Total: 2-5 seconds on any Pi** ✅

### Memory Usage
- Pi Zero: 40-50% (tight) ⚠️
- Pi Zero 2 W: 40-50% (manageable) 🟡
- Pi 3/4: 10-25% (comfortable) ✅

## Final Recommendation

### For Pi Zero (original) 🟡
**Status**: Borderline feasible
- Will work but not ideal
- Slow startup
- Memory pressure
- Potential stability issues
- **Only if you already have one**

### For Pi Zero 2 W 🟢
**Status**: Good enough
- Better CPU helps a lot
- Same RAM but faster processing
- Acceptable performance
- **Recommended if buying new**

### For Pi 3/4 ✅
**Status**: Excellent
- Smooth performance
- Plenty of headroom
- Rock solid
- **Best Raspberry Pi option**

### For VPS/Cloud ⭐
**Status**: Professional
- Always online
- Better uptime
- No hardware maintenance
- **Best overall option**

## Conclusion

**Can you run it on Pi Zero?** YES ✅  
**Should you run it on Pi Zero?** ONLY IF YOU MUST ⚠️

If you already have a Pi Zero: Try it, might work fine for your usage.  
If buying new hardware: Get Pi Zero 2 W ($15) or use free VPS.

The app is lightweight enough that it WILL run, but you'll notice:
- Slower startup
- Occasional memory pressure
- Need for optimization

For a $10-15 upgrade to Pi Zero 2 W, you get much better experience.
For free VPS (Oracle Cloud), you get professional reliability.

