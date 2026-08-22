import random
import discord
from discord import app_commands
from discord.ext import commands

# ──────────────────────────────────────────────
# Dados da Tayama
# ──────────────────────────────────────────────
QUOTES = [
    "Chegou na hora certa. Pega leve aí no trabalho, ninguém é de ferro.",
    "Tá precisando de uma pausa? Às vezes respirar 5 minutos resolve metade dos bugs.",
    "Você passa tempo demais olhando pra essa tela... mas fazer o que, né? A gente tem que pagar os boletos.",
    "Não fica esquentando a cabeça com detalhe bobo. Foca no que importa e resolve o resto depois, ou chora no banho.",
    "Se o código quebrou de novo, dá um passo pra trás antes de quebrar o teclado. Acredite, teclados são caros.",
    "O café esfriou e o código não compila? Calma, acende um cigarro (ou toma uma água) que a lógica clareia.",
    "A faculdade cobra caro da sua sanidade. Tenta não gastar ela toda no primeiro semestre.",
    "Eu não ligo se você usa light theme, desde que você sofra em silêncio cego.",
    "O prazo de entrega é hoje à meia-noite? Legal. Vou colocar um disco de vinil aqui e ver você chorar."
]

DEV_TIPS = [
    "**Git**: Faça commits pequenos e descritivos. Salvar 'ajustes' em 30 arquivos de uma vez é pedir pra sofrer no merge.",
    "**Python**: Sempre use `venv`. Se você poluir o ambiente global da sua máquina, não venha chorar pra mim depois.",
    "**Engenharia de Software**: Menos é mais no MVP. Entregue algo simples que funciona antes de inventar 50 features que ninguém vai usar.",
    "**Debug**: Colocar `print('CHEGOU AQUI')` no código inteiro é fofo, mas que tal você aprender a usar um debugger de verdade?",
    "**Documentação**: Eu sei que dá preguiça, mas escreve a droga do README. O você do futuro vai agradecer.",
    "**CSS**: Não sabe centralizar uma div? `flexbox` resolve 90% da sua ansiedade. Os outros 10% são terapia.",
    "**Mentalidade**: Todo código escrito há mais de 6 meses é legado. E adivinha? A culpa provavelmente é sua."
]

MUSICAS = [
    {
        "nome": "Lebanon Hanover - Gallowdance",
        "genre": "Darkwave / Post-Punk",
        "spotify": "https://open.spotify.com/track/74SUn8w4lYSwgOGPvVZiEo",
        "youtube": "https://www.youtube.com/watch?v=WPw7nlluKk8",
        "soundcloud": "https://soundcloud.com/lebanon-hanover/gallowdance"
    },
    {
        "nome": "She Wants Revenge - Tear You Apart",
        "genre": "Post-Punk Revival",
        "spotify": "https://open.spotify.com/track/3urJUvRhgMrwy5TMBJRjHN",
        "youtube": "https://www.youtube.com/watch?v=ixw_bLVUL34",
        "soundcloud": "https://soundcloud.com/she-wants-revenge-official/tear-you-apart"
    },
    {
        "nome": "Molchat Doma - Sudno",
        "genre": "Sovietwave / Post-Punk",
        "spotify": "https://open.spotify.com/track/3WS7spXVlbeC5kveVLFOPG",
        "youtube": "https://www.youtube.com/watch?v=HR5zpFs7YpY",
        "soundcloud": "https://soundcloud.com/molchatdoma/sudno"
    },
    {
        "nome": "Deftones - Be Quiet and Drive",
        "genre": "Alt Metal / Shoegaze",
        "spotify": "https://open.spotify.com/track/4Uiw0Sl9yskBaC6P4DcdVD",
        "youtube": "https://www.youtube.com/watch?v=KvknOXGPzCQ",
        "soundcloud": "https://soundcloud.com/deftones_official/be-quiet-and-drive-far-away"
    },
    {
        "nome": "Kino - Spokoynaya Noch (Спокойная Ночь)",
        "genre": "Sovietwave / Goth Rock",
        "spotify": "https://open.spotify.com/track/4jVn4wOedSOP0hK89rUaYg",
        "youtube": "https://www.youtube.com/watch?v=1b-3RkXp6bQ",
        "soundcloud": ""
    },
    {
        "nome": "Boy Harsher - Pain",
        "genre": "Darkwave",
        "spotify": "https://open.spotify.com/track/13HKm5ZYugOuuQ8d6N8tIf",
        "youtube": "https://www.youtube.com/watch?v=H1Zm6E6Sy4Y",
        "soundcloud": "https://soundcloud.com/boy-harsher/pain"
    }
]

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

    @app_commands.command(name="pausa", description="Faz uma pausa rápida atrás do supermercado com a Tayama.")
    async def pausa(self, interaction: discord.Interaction):
        quote = random.choice(QUOTES)
        embed = discord.Embed(
            title="Área de Fumantes / Pausa 🚬",
            description=quote,
            color=discord.Color.from_str("#c82245")
        )
        if self.bot.user.display_avatar:
            embed.set_author(name="Tayama", icon_url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="som", description="Pede uma recomendação musical de Post-Punk / Darkwave pra focar.")
    async def som(self, interaction: discord.Interaction):
        track = random.choice(MUSICAS)
        
        embed = discord.Embed(
            title="🎧 Playlist da Tayama",
            description=f"Aperta o play em **{track['nome']}**.\n*Gênero:* {track['genre']}",
            color=discord.Color.from_str("#c82245")
        )
        if self.bot.user.display_avatar:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
            
        view = MusicButtons(track)
        await interaction.response.send_message(embed=embed, view=view)


    @app_commands.command(name="dica_dev", description="Recebe uma dica prática de desenvolvimento (sem paciência).")
    async def dica_dev(self, interaction: discord.Interaction):
        tip = random.choice(DEV_TIPS)
        embed = discord.Embed(
            title="💻 Dica de Dev (Presta atenção)",
            description=tip,
            color=discord.Color.from_str("#c82245")
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tayama(bot))
