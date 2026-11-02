import os
import discord
from discord.ext import commands

# Pull token safely from Render environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

WELCOME_CHANNEL_ID = 1557958306960515122
WSP_CHANNEL_ID = 1557500794964545666
THEME_COLOR = 0xFFD72F

class GreetButton(discord.ui.View):
    def __init__(self, joined_user_id: int, is_test: bool = False):
        super().__init__(timeout=None)
        self.joined_user_id = joined_user_id
        self.is_test = is_test

    @discord.ui.button(label="👋 Say Hello!", style=discord.ButtonStyle.secondary)
    async def say_hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            description=f"{interaction.user.mention} said wsp to <@{self.joined_user_id}>",
            color=THEME_COLOR
        )
        if self.is_test:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            target_channel = interaction.client.get_channel(WSP_CHANNEL_ID)
            await target_channel.send(embed=embed)
            await interaction.response.send_message("Message sent!", ephemeral=True)

class WelcomeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = WelcomeBot()

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Welcome to winstreaksmp.xyz",
            description=f"{member.mention} is our newest member.",
            color=THEME_COLOR
        )
        await channel.send(embed=embed, view=GreetButton(joined_user_id=member.id))

@bot.tree.command(name="testwelcome", description="Simulate a fake welcome message (Restricted)")
async def testwelcome(interaction: discord.Interaction):
    if interaction.user.name != "thing_three_minecraft":
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return
        
    embed = discord.Embed(
        title="Welcome to winstreaksmp.xyz",
        description="<@000000000000000000> is our newest member.",
        color=THEME_COLOR
    )
    await interaction.response.send_message(
        embed=embed, 
        view=GreetButton(joined_user_id=000000000000000000, is_test=True), 
        ephemeral=True
    )

bot.run(TOKEN)
