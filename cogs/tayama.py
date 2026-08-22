import json
import random
import discord
from discord import app_commands
from discord.ext import commands

# ──────────────────────────────────────────────
# Carregamento Híbrido da Personalidade (Banco Tayama)
# ──────────────────────────────────────────────
def get_tayama_content():
    try:
        with open("database/tayama_content.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"quotes": ["Eu tô sem voz."], "dev_tips": ["Ligue o banco de dados."], "musicas": []}

# ──────────────────────────────────────────────
# Componentes (View UI)
# ──────────────────────────────────────────────
class MusicButtons(discord.ui.View):
    def __init__(self, links: dict):
        super().__init__()
        
        if links.get("spotify"):
            self.add_item(discord.ui.Button(label="Spotify", url=links["spotify"], style=discord.ButtonStyle.link, emoji="🟢"))
        
        if links.get("youtube"):
            self.add_item(discord.ui.Button(label="YouTube", url=links["youtube"], style=discord.ButtonStyle.link, emoji="🔴"))
            
        if links.get("soundcloud"):
            self.add_item(discord.ui.Button(label="SoundCloud", url=links["soundcloud"], style=discord.ButtonStyle.link, emoji="☁️"))


# ──────────────────────────────────────────────
# Cog: Tayama Corner
# ──────────────────────────────────────────────
class Tayama(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = discord.Color.from_str("#c82245")

    @app_commands.command(name="pausa", description="Faz uma pausa rápida atrás do supermercado com a Tayama.")
    async def pausa(self, interaction: discord.Interaction):
        conteudo = get_tayama_content()
        quote = random.choice(conteudo["quotes"])
        embed = discord.Embed(
            title="Área de Fumantes / Pausa 🚬",
            description=quote,
            color=self.color
        )
        if self.bot.user.display_avatar:
            embed.set_author(name="Tayama", icon_url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="som", description="Pede uma recomendação musical de Post-Punk / Darkwave pra focar.")
    async def som(self, interaction: discord.Interaction):
        conteudo = get_tayama_content()
        track = random.choice(conteudo["musicas"])
        
        embed = discord.Embed(
            title="🎧 Playlist da Tayama",
            description=f"Aperta o play em **{track['nome']}**.\n*Gênero:* {track['genre']}",
            color=self.color
        )
        if self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        view = MusicButtons(track)
        await interaction.response.send_message(embed=embed, view=view)


    @app_commands.command(name="dica_dev", description="Recebe uma dica prática de desenvolvimento (sem paciência).")
    async def dica_dev(self, interaction: discord.Interaction):
        conteudo = get_tayama_content()
        tip = random.choice(conteudo["dev_tips"])
        embed = discord.Embed(
            title="💻 Dica de Dev (Presta atenção)",
            description=tip,
            color=self.color
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tayama(bot))
