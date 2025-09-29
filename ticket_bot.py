import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

SUPPORT_ROLE_ID = 1417532337226383401  # Your support role ID

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="ticket", description="Open a support ticket")
async def ticket(ctx):
    # Check if user already has a ticket open
    existing = discord.utils.get(ctx.guild.channels, name=f"ticket-{ctx.author.id}")
    if existing:
        await ctx.respond("You already have an open ticket.", ephemeral=True)
        return

    # Find the support role by ID
    support_role = ctx.guild.get_role(SUPPORT_ROLE_ID)
    if not support_role:
        await ctx.respond(f"Support role not found. Please check the SUPPORT_ROLE_ID.", ephemeral=True)
        return

    # Create ticket channel with permissions
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        ctx.guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await ctx.guild.create_text_channel(f"ticket-{ctx.author.id}", overwrites=overwrites, reason="Support ticket")

    await channel.send(f"{ctx.author.mention} Your ticket has been created. Support will be with you soon!")
    await ctx.respond(f"Ticket created: {channel.mention}", ephemeral=True)

@bot.slash_command(name="close", description="Close this ticket (support only)")
async def close(ctx):
    support_role = ctx.guild.get_role(SUPPORT_ROLE_ID)
    if not support_role or support_role not in ctx.author.roles:
        await ctx.respond("You do not have permission to close tickets.", ephemeral=True)
        return
    if ctx.channel.name.startswith("ticket-"):
        await ctx.respond("Closing ticket...", ephemeral=True)
        await ctx.channel.delete()
    else:
        await ctx.respond("This command can only be used in a ticket channel.", ephemeral=True)

bot.run("YOUR_BOT_TOKEN")
