import os
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix="!")

currently_answering = None

## question is the same as round, its just round is already a variable in python. Most info will be obtained form CSV, which ill do later
class question_info():
    def __init__(self):
        self.value = 0 # How much the question is worth
        self.catagory = None # The catagory of the question
        self.question = None # The question itself
        self.answer = None # The answer to the question
        self.last_winner = None # The winner of the previous question, as they get to choose the next question
        self.answering = None # The person who is currently answering the question

question = question_info()

class buzzer_button(discord.ui.View):
    buzzed_in = []

    async def on_timeout(self) -> None:
        await self.disabled_all_items()
        await self.message.channel.send("No-one buzzed in!")


    # Removes the button, idk if disabling is needed
    async def disabled_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.delete()


    # When the button is pressed, it will add the user to the list of people who have buzzed in, and set them as the person answering the question
    #TODO: Add a way to answer a question
    @discord.ui.button(label='Buzz In!',style=discord.ButtonStyle.danger)
    async def buzzer(self,interaction: discord.Integration, button: discord):
        if interaction.user not in self.buzzed_in:
            await self.disabled_all_items()
            await self.message.channel.send(f"{interaction.user.mention} has buzzed in!")
            self.buzzed_in.append(interaction.user)
            question.answering = interaction.user.mention
        else:
            await self.message.channel.send(f"{interaction.user.mention} has already buzzed in, wait until the next question!")

@bot.event
async def on_ready():
    global accept_questions
    assert bot.user is not None
    accept_questions = False
    print(bot.user.name, "has connected to discord")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        ctx.reply("Command not found.")

#NOTE: DONT SPAM IT FLAME!!! 
#MSG: CY, copilot autofilled "I'm not spamming it, I'm just testing it" and that apparently if U spam something you will get '"Banned" from discord'
@bot.command()
async def sync(ctx):
    if str(ctx.message.author.id) in {
        "272342994999574528", #CY
        "555457001522724864", #Flame
    }:
        await ctx.reply("Beginning sync request")
        await bot.tree.sync()
        await ctx.reply("Commands have been synchronised.")
    else:
        await ctx.reply("Only some can sync commands due to ratelimiting.")


#Later on it will work as part of the question progression, but for now it will be seperate
@bot.hybrid_command(name="buzzer", description="Summons a buzzer, allowing users to buzz in.")
async def buzzer(ctx,timeout=15):
    await ctx.message.delete()
    buzzed_in = buzzer_button(timeout=timeout)
    message = await ctx.send(view=buzzed_in)
    # view.buzzed_in = []  # Reset the list of buzzed in users, unused rn as only way is called is by multiple uses of the command.
    buzzed_in.message = message

#TODO: Add a way to select the next question
@bot.hybrid_command(name="next_question", description=f"{question.last_winner}, select the first category and price to play for." if round == 0 else f"{question.last_winner}, select the next category and price to play for.")
async def next_question(ctx,Catagory,Value):
    pass



# Bans users who say taiwan, and collects answers to questions
@bot.listen()
async def on_message(message: discord.Message):
    global ans_list, accept_questions
    if "taiwan" in message.content.lower() and str(message.author.id) not in {
        "272342994999574528", #CY
        "555457001522724864", #Flame
    }:
        author = message.author
        await author.ban(reason="very bad citizen!")
    if accept_questions and message.content.lower().startswith("!") and message.author == currently_answering:
            ans_list.append(message.content)

# bot.add_command(next_question) # Github Copilot autofilled this, but I dont know what it does. I think it adds the command to the bot, but I dont know if its needed, does sync work better?

bot.run(TOKEN)