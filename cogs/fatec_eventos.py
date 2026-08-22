import discord
from discord.ext import commands
from discord import app_commands


class FatecEventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="eventos",
        description="Lista eventos acadêmicos, palestras e Innovation Week.",
    )
    async def listar_eventos(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        embed = discord.Embed(
            title="📅 Eventos Acadêmicos & FATEC SJC",
            description="Fique por dentro das palestras, semanas acadêmicas e workshops de tecnologia:",
            color=discord.Color.from_str("#ff73fa"),
        )

        embed.add_field(
            name="🚀 Innovation Week FATEC",
            value=(
                "**Data:** Em breve\n"
                "**Local:** Auditório / Remoto\n"
                "*Palestras sobre arquitetura de software, inteligência artificial e carreira em tecnologia.*"
            ),
            inline=False,
        )
        embed.add_field(
            name="💻 Workshops de Desenvolvimento",
            value=(
                "**Foco:** Python, Git Avançado e Linux Mint.\n"
                "*Acompanhe os avisos nos canais da faculdade para inscrições.*"
            ),
            inline=False,
        )

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FatecEventos(bot))