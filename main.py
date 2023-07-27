import discord
from what_if import chat
import os
from dotenv import load_dotenv
from what_if.profile import ProfileService

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

keyword = "&"

commands = {
    "reset": "reset",
    "background": "background",
    "query": "what if",
    "help": "help",
    "continue": "continue",
}

client = discord.Client(intents=intents)

profile_service = ProfileService()
agent = chat.ChatAgent()


def split_response(text):
    pool = text.split(".")
    composed = str()
    resp = list()
    while pool:
        sentence = pool.pop(0)
        if len(composed) + len(sentence) < 2000:
            composed = composed + sentence + "."
        else:
            resp.append(str(composed))
            composed = str()
    else:
        resp.append(composed)
    return resp


async def parse_query(channel, user, query):
    profile_service.update_chat(user, query)
    context = profile_service.read_chat(user)
    response = agent.beseech(context)["choices"][0]["message"]
    profile_service.update_chat(user, response)
    outputs = split_response(response["content"])

    for output in outputs:
        await channel.send(output)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    user = message.author.name

    if message.author == client.user:
        return

    if message.content.startswith(keyword):
        if message.content.startswith(keyword + commands["reset"]):
            profile_service.reset_chat(user)

        elif message.content.startswith(keyword + commands["background"]):
            content = message.content[len(keyword + commands["background"]) :].strip()
            profile_service.update_background(user, content)

        elif message.content.startswith(keyword + commands["query"]):
            content = message.content[1:].strip()
            query = {"role": "user", "content": content}
            await parse_query(message.channel, user, query)

        elif message.content.startswith(keyword + commands["continue"]):
            content = message.content[len(keyword + commands["continue"]) :].strip()
            query = {"role": "user", "content": content}
            await parse_query(message.channel, user, query)

        elif message.content.startswith(keyword + commands["help"]):
            await message.channel.send(str(commands))


client.run(os.getenv("discord_token"))
