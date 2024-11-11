import discord
import os  # default module
from dotenv import load_dotenv
import main  # assuming main.py has the check_class_availability function
import time

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.slash_command(name="classes", description="Check availability of a certain class at Arizona State University.")
async def classes(ctx: discord.ApplicationContext, args: discord.Option(str, "Enter course name")):  # type: ignore
    await ctx.defer()  # Defer the response to avoid the 3-second timeout

    # Fetch class availability
    string = main.check_class_availability(args)

    # Check if string is empty
    if not string.strip():
        string = "No class information found for the specified course."

    # After getting the result, respond with the content
    await ctx.respond(string)

bot.run(os.getenv('TOKEN'))  # run the bot with the token
