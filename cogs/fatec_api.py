import discord
from discord.ext import commands
from discord import app_commands
from database.json_db import carregar_dados
import logging

logger = logging.getLogger("TayamaBot")


class FatecApi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="api_sprints",
        description="Acompanha as Sprints e metas dos Projetos Integradores.",
    )
    async def listar_sprints(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            dados = await carregar_dados()

            # Corrigido: a chave real no dados.json é "projeto_integrador_api" -> "sprints"
            projeto = dados.get("projeto_integrador_api", {})
            sprints = projeto.get("sprints", [])

            embed = discord.Embed(
                title="🚀 Metodologia Ágil - Sprints do Projeto Integrador",
                color=discord.Color.green(),
            )

            if not sprints:
                embed.description = "Nenhuma sprint cadastrada no momento."
            else:
                tema = projeto.get("tema", "")
                semestre = projeto.get("semestre", "")
                if tema:
                    embed.description = f"**Tema:** {tema} · {semestre}"

                for s in sprints:
                    numero = s.get("numero", "?")
                    status = s.get("status", "?")
                    meta = s.get("meta", "Sem meta definida.")
                    inicio = s.get("data_inicio", "?")
                    fim = s.get("data_fim", "?")

                    embed.add_field(
                        name=f"Sprint {numero} — {status}",
                        value=f"**Meta:** {meta}\n📅 {inicio} → {fim}",
                        inline=False,
                    )

            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /api_sprints", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar as sprints. Tente novamente.",
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(FatecApi(bot))