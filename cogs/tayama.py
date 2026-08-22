import random
import discord
from discord import app_commands
from discord.ext import commands

class Tayama(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.quotes = [
            "Chegou na hora certa. Pega leve aí no trabalho/estudo, ninguém é de ferro.",
            "Tá precisando de uma pausa? Às vezes respirar 5 minutos resolve metade dos bugs.",
            "Você passa tempo demais olhando pra essa tela... mas fazer o que, né?",
            "Não fica esquentando a cabeça com detalhe bobo. Foca no que importa e resolve o resto depois.",
            "Se o código quebrou, dá um passo pra trás antes de quebrar o teclado.",
            "O café esfriou e o código não compila? Calma, acende um cigarro (ou toma uma água) que a lógica clareia."
        ]

        self.music_suggestions = [
            "Deftones - *Entombed*",
            "Deftones - *Digital Bath*",
            "Deftones - *Be Quiet and Drive (Far Away)*",
            "She Wants Revenge - *Tear You Apart*",
            "Lebanon Hanover - *Gallowdance*",
            "The Cure - *A Forest*",
            "Miss Construction - *Kunstprodukt*",
            "Bauhaus - *Bela Lugosi's Dead*",
            "Boy Harsher - *Pain*"
        ]

        self.dev_tips = [
            "**Git**: Faça commits pequenos e descritivos. Salvar 'ajustes' em 30 arquivos de uma vez é pedir pra sofrer no merge.",
            "**Python**: Sempre use `venv` ou gerenciador de pacotes isolado. Evite instalar libs globais no sistema operacional.",
            "**Banco de Dados**: Se a consulta estiver lenta, verifique se você criou índices para as chaves estrangeiras.",
            "**Engenharia de Software**: Menos é mais no MVP do API. Entregue algo simples e funcionando antes de inventar mil telas.",
            "**Linux/Terminal**: Use apelidos (`aliases`) no seu `.bashrc` ou `.zshrc` para comandos longos do dia a dia."
        ]

    @app_commands.command(name="pausa", description="Faz uma pausa rápida atrás do supermercado com a Tayama.")
    async def pausa(self, interaction: discord.Interaction):
        quote = random.choice(self.quotes)
        embed = discord.Embed(
            title="Área de Fumantes / Pausa 🚬",
            description=f"*{quote}*",
            color=discord.Color.from_rgb(45, 52, 54)
        )
        if self.bot.user.display_avatar:
            embed.set_author(name="Tayama", icon_url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="som", description="Pede uma recomendação musical para focar no código.")
    async def som(self, interaction: discord.Interaction):
        track = random.choice(self.music_suggestions)
        await interaction.response.send_message(
            f"🎧 **Recomendação da Tayama:** {track}"
        )

    @app_commands.command(name="dica_dev", description="Recebe uma dica prática de desenvolvimento e estudos da Tayama.")
    async def dica_dev(self, interaction: discord.Interaction):
        tip = random.choice(self.dev_tips)
        embed = discord.Embed(
            title="💡 Dica de Dev da Tayama",
            description=tip,
            color=discord.Color.dark_grey()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Tayama(bot))
