import nextcord
from nextcord.ext import commands
import difflib
import os
import json


client = commands.Bot(command_prefix='a!', help_command=None, intents=nextcord.Intents.all(), owner_id=("695734833116086303"))
if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
@client.event
async def on_ready():
    print("Bot is ready")

    activity = nextcord.Game(name=f"on {len(client.guilds)} servers! | a!help ðŸ˜Ž")
    await client.change_presence(status=nextcord.Status.online, activity=activity)

@client.event    
async def on_command_error(ctx: commands.Context, error: Exception):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("You don't have the perms for that")
	elif isinstance(error,commands.CommandOnCooldown):
		m, s = divmod(error.retry_after, 60)
		h, m = divmod(m, 60)
		if int(h) == 0 and int(m) == 0:
			em = nextcord.Embed(title="**Command on cooldown**", description=f'You must wait {int(s)} seconds to use the {ctx.command} command!', colour=nextcord.Colour.red())
			await ctx.send(embed=em, delete_after=float(error.retry_after))
		elif int(h) == 0 and int(m) != 0:
			em = nextcord.Embed(title="**Command on cooldown**", description=f' You must wait {int(m)} minutes and {int(s)} seconds to use the {ctx.command} command!', colour=nextcord.Colour.red())
			await ctx.send(embed=em, delete_after=float(error.retry_after))
		else:
			em = nextcord.Embed(title="**Command on cooldown**", description=f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use the {ctx.command} command!', colour=nextcord.Colour.red())
			await ctx.send(embed=em, delete_after=float(error.retry_after))
	elif isinstance(error, commands.MissingRequiredArgument):
		ctx.command.reset_cooldown(ctx)
		em = nextcord.Embed(
			title="Missing Required Argument",
			color = nextcord.Color.red(),
			description=f"```\n{ctx.prefix}{ctx.command.name} {ctx.command.usage if ctx.command.usage else ctx.command.signature}\n```\n\n**{error.args[0]}**")
		await ctx.send(embed=em)
	elif isinstance(error, commands.CommandNotFound):
		# await ctx.send("That's not a command")
		matches = difflib.get_close_matches((ctx.message.content.split(' ')[0]).strip(ctx.prefix), [cmd.name for cmd in client.commands]) # this needs to be improved but i can't be bothered to do that rn
		if matches:
			em = nextcord.Embed(title='Command not found', description="Did you mean: \n"+' | '.join(f'`{match}`' for match in matches), color=nextcord.Color.red())
			return await ctx.send(embed=em)
		return await ctx.send(embed=nextcord.Embed(title='Command not found', description="That's not a command", color=nextcord.Color.red()))
	elif isinstance(error, commands.CheckFailure):
		notbotowner = nextcord.Embed(title="Error", description="You dont own the bot, you cant do that", color=nextcord.Colour.red())
		await ctx.send(embed=notbotowner)
	elif isinstance(error, commands.ExtensionNotLoaded):
		await ctx.send("That cog does not exist or is not loaded")
	elif isinstance(error, commands.DisabledCommand):
		await ctx.send("That command is disabled!")
	elif isinstance(error, commands.MemberNotFound):
		await ctx.send("Member is not found")
	else:
		await ctx.send(error)
		raise error

class Dropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Normal Commands", description="Commands any member can use"),
            nextcord.SelectOption(label="Moderation Commands", description="Commands moderators can use")
        ]
        super().__init__(placeholder="Select a catagory of commands to use!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Integration):
        if self.values[0] == "Normal Commands":
            embed = nextcord.Embed(title=f"Normal commands", description="Commands anyone can use :D")
            embed.add_field(name="\na!ping", value="Show's the bots current ping")
            embed.add_field(name="a!8ball", value=":8ball:")
            embed.add_field(name="a!coinflip", value="Flip a coin!")
            embed.add_field(name="a!avatar (@user)", value="Show's the avatar of a person in the server!")
            embed.add_field(name="a!poll (question)", value="Ask people a question with a poll")               
            embed.add_field(name="a!rps", value="Play rock, paper, scissors with the bot")                        
            embed.add_field(name="a!uptime", value="See the bots uptime")          
            return await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "Moderation Commands":
            embedmod = nextcord.Embed(title=f"Moderation Commands", description="Commands moderators can use")
            embedmod.add_field(name="\na!kick", value="Kicks a member from the server")
            embedmod.add_field(name="\na!ban", value="Ban a member from the server")
            embedmod.add_field(name="\na!unban", value="Unban a member from the server")     
            embedmod.add_field(name="\na!purge", value="Purge some messages")                    
            

            return await interaction.response.edit_message(embed=embedmod)

        await interaction.response.send_message(f"you choose {self.values[0]}")

class DropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

@client.command()
async def help(ctx):
    view = DropdownView()
    await ctx.send("Choose a category for help!", view=view)

client.run(token)
