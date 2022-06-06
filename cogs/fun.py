import nextcord 
import random
from nextcord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def simprate(self, ctx):
        choices = [1, 101]
        await ctx.send(random.choice(choices))

def setup(client):
    client.add_cog(Fun(client))        