import logging
import discord
from discord import app_commands
from discord.ext import commands

from database.json_db import carregar_dados
from services.fatec_service import get_aulas_do_dia, get_todas_disciplinas

logger = logging.getLogger("TayamaBot")

class DisciplinaSelect(discord.ui.Select):
    def __init__(self, disciplinas: list[dict]):
        options = [
            discord.SelectOption(
                label=d.get("nome", "?")[:100],
                value=d.get("codigo", "?"),
                description=f"{d.get('codigo', '')} · {d.get('carga_horaria', '?')}h",
                emoji="??",
            )
            for d in disciplinas
        ]
        super().__init__(
            placeholder="Escolha uma matéria...",
            min_values=1,
            max_values=1,
            options=options,
        )
        self._disciplinas = {d.get("codigo"): d for d in disciplinas}

    async def callback(self, interaction: discord.Interaction):
        disc = self._disciplinas.get(self.values[0])
        if not disc:
            return await interaction.response.send_message("?? Disciplina não encontrada.", ephemeral=True)

        desemp = disc.get("desempenho", {})
        notas = desemp.get("notas", {})
        profs = disc.get("professores", [])
        professor = profs[0].get("nome", "A definir") if profs else "A definir"

        freq = desemp.get("frequencia_percentual", 100.0)
        alerta_freq = " ??" if freq <= 75 else ""

        horarios_fmt = "\n".join(
            f"• {h.get('dia_semana')} · {h.get('inicio')} às {h.get('fim')} · {h.get('sala')}"
            for h in disc.get("horarios", [])
        ) or "Sem horário definido."

        notas_fmt = "\n".join(
            f"**{k.upper()}:** {v if v is not None else '—'}"
            for k, v in notas.items()
        ) or "Nenhuma nota lançada."

        embed = discord.Embed(
            title=f"?? {disc.get('nome', '?')}",
            color=discord.Color.from_str("#c82245"),
        )
        embed.add_field(name="Código", value=disc.get("codigo", "?"), inline=True)
        embed.add_field(name="Carga", value=f"{disc.get('carga_horaria', '?')}h", inline=True)
        embed.add_field(name="Status", value=desemp.get("situacao", "?"), inline=True)
        embed.add_field(name="Professor", value=f"?? {professor}", inline=False)
        embed.add_field(name="Horários", value=horarios_fmt, inline=False)
        embed.add_field(
            name=f"Frequência{alerta_freq}",
            value=f"**{freq}%** · {desemp.get('faltas', 0)} falta(s)",
            inline=False,
        )
        embed.add_field(name="Notas", value=notas_fmt, inline=False)
        embed.add_field(name="Ementa", value=disc.get("ementa", "Não informada.")[:1020], inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


class DisciplinaView(discord.ui.View):
    def __init__(self, disciplinas: list[dict]):
        super().__init__(timeout=120)
        self.add_item(DisciplinaSelect(disciplinas))


class FatecAulas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="aulas_hoje", description="Exibe as aulas do dia.")
    @app_commands.describe(dia="Escolha um dia da semana")
    @app_commands.choices(dia=[
        app_commands.Choice(name="Segunda-feira", value="Segunda-feira"),
        app_commands.Choice(name="Terça-feira",   value="Terça-feira"),
        app_commands.Choice(name="Quarta-feira",  value="Quarta-feira"),
        app_commands.Choice(name="Quinta-feira",  value="Quinta-feira"),
        app_commands.Choice(name="Sexta-feira",   value="Sexta-feira"),
    ])
    async def aulas_hoje(self, interaction: discord.Interaction, dia: str = "Segunda-feira"):
        await interaction.response.defer(thinking=True)
        try:
            aulas = await get_aulas_do_dia(dia)
            embed = discord.Embed(title=f"?? Grade de Aulas — {dia}", color=discord.Color.from_str("#c82245"))

            if not aulas:
                embed.description = "Nenhuma aula. Pode voltar a dormir. ??"
            else:
                for aula in aulas:
                    embed.add_field(
                        name=f"?? {aula['codigo']} — {aula['nome']}",
                        value=(
                            f"? **{aula['inicio']} às {aula['fim']}**\n"
                            f"?? {aula['professor']}\n"
                            f"?? {aula['sala']}\n\u200b"
                        ),
                        inline=False,
                    )
            await interaction.followup.send(embed=embed)
        except Exception:
            logger.error("Erro em /aulas_hoje", exc_info=True)
            await interaction.followup.send("?? Erro.", ephemeral=True)

    @app_commands.command(name="disciplina", description="Detalhes de uma matéria.")
    async def disciplina(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            disciplinas = await get_todas_disciplinas(interaction.user.id)
            if not disciplinas:
                return await interaction.followup.send("Nenhuma disciplina.", ephemeral=True)
            view = DisciplinaView(disciplinas)
            await interaction.followup.send("?? Escolha uma matéria:", view=view)
        except Exception:
            logger.error("Erro em /disciplina", exc_info=True)
            await interaction.followup.send("?? Erro.", ephemeral=True)

    @app_commands.command(name="materias", description="Lista todas as matérias e seus horários.")
    async def materias(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            dados = await carregar_dados()
            disciplinas = dados.get("disciplinas", [])
            embed = discord.Embed(title="?? Disciplinas do Semestre", color=discord.Color.from_str("#c82245"))

            if not disciplinas:
                embed.description = "Nenhuma disciplina cadastrada."
            else:
                for disc in disciplinas:
                    horarios_fmt = " | ".join(f"{h.get('dia_semana', '?')} {h.get('inicio', '?')}" for h in disc.get("horarios", [])) or "Sem horário"
                    profs = disc.get("professores", [])
                    prof = profs[0].get("nome", "A definir") if profs else "A definir"
                    embed.add_field(
                        name=f"?? {disc.get('codigo', '?')} — {disc.get('nome', '?')}",
                        value=f"?? {prof}\n?? {horarios_fmt}\n\u200b",
                        inline=False,
                    )
            await interaction.followup.send(embed=embed)
        except Exception:
            logger.error("Erro em /materias", exc_info=True)
            await interaction.followup.send("?? Erro.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(FatecAulas(bot))
