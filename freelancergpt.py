import os
import openai.api_resources.chat_completion as openai
import discord
from dotenv import load_dotenv
from discord.ext import commands
from pathlib import Path


# Get the path to the .env file located in the pythonlatest/app folder
env_path = Path(__file__).parent / ".env"

# Load environment variables
load_dotenv()

# Get the environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

print("Discord Bot Token:", TOKEN)
print("OpenAI API Key:", OPENAI_API_KEY)

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY\


intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # enables the privileged message content intent

bot = commands.Bot(command_prefix="?", intents=intents)

# Keep track of the conversation history
conversation_history = []


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.command(name="ask")
async def ask(ctx, *, question):
    # Combine the previous messages with the current question
    prompt = "Conversation:\n" + "\n".join(conversation_history) + "\nQuestion: " + question + "\nAnswer:"

    # Use v1/chat/completions endpoint instead of v1/completions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Freelancer-GPT On a mission from another dimension to all who ask for help. Build a living online doing what they love."},
            *[
                {"role": "user" if i % 2 == 0 else "assistant", "content": msg}
                for i, msg in enumerate(conversation_history)
            ],
            {"role": "user", "content": question},
        ],
        max_tokens=200,
        temperature=1.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        answer = response.choices[0].message['content'].strip()
    except AttributeError:
        print("Error occurred when trying to access 'text' attribute. Response:", response)
        answer = "I'm sorry, I'm unable to provide an answer at the moment."

    await ctx.send(answer)

    # Add the current question and answer to the conversation history
    conversation_history.append("You: " + question)
    conversation_history.append("AI: " + answer)

@bot.command(name="test_welcome")
async def test_welcome(ctx):
    member = ctx.message.author
    await send_welcome_message(member)

async def store_message(channel_id, message_id, content, user_id):
    message_data = (
        str(message_id),
        content,
        user_id,
        channel_id
    )
    cursor.execute("INSERT INTO messages (id, content, userId, channelId) VALUES (%s, %s, %s, %s)", message_data)
    conn.commit()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message starts with the command prefix
    if not message.content.startswith("?"):
        # If the message is a direct message (DM) or in the free-ai-mentoring
        if isinstance(message.channel, discord.DMChannel) or message.channel.name == "free-ai-mentoring":
            await ask(message.channel, question=message.content)
        else:
            await store_message(
                channel_id=str(message.channel.id),
                message_id=str(message.id),
                content=message.content,
                user_id=str(message.author.id)
            )

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)