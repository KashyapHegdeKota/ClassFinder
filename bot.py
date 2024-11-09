import discord
import os # default module
from dotenv import load_dotenv,find_dotenv
import main
import time
load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.slash_command(name="classes", description="Check availability of a certain class at Arizona State University.", guild_ids=[1184747941848686653])
async def classes(ctx: discord.ApplicationContext, args: discord.Option(str, "Enter course name")): # type: ignore
    await ctx.defer()  # Defer the response to avoid the 3-second timeout

    # Fetch class availability
    string = main.check_class_availability(args)

    # After getting the result, respond with the content
    await ctx.respond(string)
print(os.getenv('TOKEN'))
bot.run(os.getenv('TOKEN')) # run the bot with the token