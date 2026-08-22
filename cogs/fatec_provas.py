import discord
from discord.ext import commands
from discord import app_commands
from database.json_db import carregar_dados
import logging

logger = logging.getLogger("TayamaBot")


class FatecProvas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="provas",
        description="Lista o cronograma de provas e entregas acadêmicas.",
    )
    async def listar_provas(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            dados = await carregar_dados()
            provas = dados.get("provas", [])

            if not provas:
                await interaction.followup.send(
                    "Nenhuma prova ou entrega cadastrada no momento."
                )
                return

            embed = discord.Embed(
                title="📝 Cronograma de Provas e Entregas - FATEC",
                color=discord.Color.from_str("#c82245"),
            )

            for p in provas:
                status = p.get("status", "?")
                titulo = p.get("titulo", "Sem título")
                disciplina = p.get("disciplina", "?")
                data = p.get("data", "A definir")

                embed.add_field(
                    name=f"[{status}] {titulo}",
                    value=f"**Matéria:** {disciplina}\n**Data Limite:** {data}",
                    inline=False,
                )

            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /provas", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar as provas. Tente novamente.",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(FatecProvas(bot))