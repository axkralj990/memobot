import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from src.agent import DailyLogAgent

load_dotenv()


class DailyLogBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
        self.target_channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
        
        # Initialize the AI agent
        self.agent = DailyLogAgent(
            notion_db_id=os.getenv("NOTION_DATABASE_ID"),
            notion_token=os.getenv("NOTION_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def on_ready(self):
        print(f"✅ Bot logged in as {self.user}")
        print(f"📝 Listening to channel ID: {self.target_channel_id}")
        print(f"🤖 AI Agent initialized and ready!")
    
    async def on_message(self, message):
        # Ignore bot's own messages
        if message.author == self.user:
            return
        
        # Only process messages from the target channel
        if message.channel.id != self.target_channel_id:
            return
        
        print(f"\n📨 New message from {message.author}: {message.content}")
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Let the agent handle the message
                response = self.agent.process_message(message.content)
                
                # Send response back to Discord
                await message.reply(response, mention_author=False)
                
                print(f"✅ Agent responded successfully")
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                await message.reply(error_msg, mention_author=False)
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()


def run_bot():
    """Start the Discord bot."""
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("DISCORD_BOT_TOKEN not found in .env")
    
    bot = DailyLogBot()
    bot.run(token)


if __name__ == "__main__":
    run_bot()
