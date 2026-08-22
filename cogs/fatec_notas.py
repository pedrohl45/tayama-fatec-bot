import logging

import discord
from discord import app_commands
from discord.ext import commands

from database.json_db import carregar_dados
from services.fatec_service import (
    calcular_media_necessaria,
    get_disciplinas_em_risco,
    get_todas_disciplinas,
)

logger = logging.getLogger("TayamaBot")


# ──────────────────────────────────────────────
# View: Select Menu para /media_necessaria
# ──────────────────────────────────────────────

class MediaSelect(discord.ui.Select):
    def __init__(self, disciplinas: list[dict]):
        options = [
            discord.SelectOption(
                label=d.get("nome", "?")[:100],
                value=d.get("codigo", "?"),
                description=d.get("codigo", ""),
                emoji="📊",
            )
            for d in disciplinas
        ]
        super().__init__(
            placeholder="Escolha uma disciplina para calcular a média...",
            min_values=1,
            max_values=1,
            options=options,
        )
        self._disciplinas = {d.get("codigo"): d for d in disciplinas}

    async def callback(self, interaction: discord.Interaction):
        disc = self._disciplinas.get(self.values[0])
        if not disc:
            return await interaction.response.send_message(
                "⚠️ Disciplina não encontrada.", ephemeral=True
            )

        notas = disc.get("desempenho", {}).get("notas", {})
        resultado = calcular_media_necessaria(notas)

        nome = disc.get("nome", "?")

        if resultado["media_final"] is not None:
            # Todas as notas já lançadas
            cor = discord.Color.green() if resultado["aprovado"] else discord.Color.red()
            situacao = "✅ Aprovado!" if resultado["aprovado"] else "❌ Reprovado"
            embed = discord.Embed(
                title=f"📊 Resultado Final — {nome}",
                description=f"**Média final: {resultado['media_final']}**\n{situacao}",
                color=cor,
            )
        else:
            # Ainda há avaliações pendentes
            faltantes_fmt = ", ".join(n.upper() for n in resultado["notas_faltantes"])
            cor = discord.Color.green() if resultado["possivel"] else discord.Color.red()

            if resultado["possivel"]:
                desc = (
                    f"**Média parcial:** {resultado['media_parcial']}\n"
                    f"**Avaliações pendentes:** {faltantes_fmt}\n\n"
                    f"Você precisa de pelo menos **{resultado['necessaria_por_avaliacao']}** "
                    f"em cada avaliação restante para ser aprovado."
                )
            else:
                desc = (
                    f"**Média parcial:** {resultado['media_parcial']}\n"
                    f"**Avaliações pendentes:** {faltantes_fmt}\n\n"
                    f"⚠️ Infelizmente já não é mais possível atingir {5.0} "
                    f"mesmo com 10 em todas as avaliações restantes."
                )

            embed = discord.Embed(
                title=f"🧮 Média Necessária — {nome}",
                description=desc,
                color=cor,
            )

        # Mostra as notas atuais
        notas_fmt = "\n".join(
            f"**{k.upper()}:** {v if v is not None else '—'}"
            for k, v in notas.items()
        )
        embed.add_field(name="📝 Notas Atuais", value=notas_fmt or "Nenhuma.", inline=False)
        embed.set_footer(text="Fórmula: P1×0.35 + P2×0.35 + Projeto×0.30 ≥ 5.0")

        await interaction.response.send_message(embed=embed, ephemeral=True)


class MediaView(discord.ui.View):
    def __init__(self, disciplinas: list[dict]):
        super().__init__(timeout=120)
        self.add_item(MediaSelect(disciplinas))


# ──────────────────────────────────────────────
# Cog
# ──────────────────────────────────────────────

class FatecNotas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="boletim", description="Visão geral de faltas, presenças e status.")
    async def boletim(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            disciplinas = await get_todas_disciplinas(interaction.user.id)
            embed = discord.Embed(
                title="📊 Boletim de Frequência e Desempenho",
                color=discord.Color.from_str("#c82245"),
            )

            if not disciplinas:
                embed.description = "Nenhuma disciplina cadastrada para o seu semestre."
            else:
                for disc in disciplinas:
                    desempenho = disc.get("desempenho", {})
                    frequencia = desempenho.get("frequencia_percentual", 100.0)
                    faltas = desempenho.get("faltas", 0)
                    situacao = desempenho.get("situacao", "—")
                    alerta = " ⚠️" if frequencia <= 75 else ""

                    embed.add_field(
                        name=f"{disc.get('codigo', '?')} — {disc.get('nome', '?')}",
                        value=(
                            f"📈 Frequência: **{frequencia}%**{alerta}\n"
                            f"❌ Faltas: {faltas}\n"
                            f"📌 Status: {situacao}"
                        ),
                        inline=True,
                    )

            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /boletim", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar o boletim. Tente novamente.",
                ephemeral=True,
            )

    @app_commands.command(name="avaliacoes", description="Cronograma de provas e trabalhos.")
    async def avaliacoes(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            dados = await carregar_dados()
            embed = discord.Embed(
                title="📝 Cronograma de Avaliações",
                color=discord.Color.from_str("#c82245"),
            )

            provas = dados.get("cronograma_avaliacoes", [])
            if not provas:
                embed.description = "Nenhuma avaliação cadastrada no momento."
            else:
                for prova in provas:
                    status = prova.get("status", "?")
                    titulo = prova.get("titulo", "Sem título")
                    data = prova.get("data", "A definir")
                    peso = prova.get("peso", "?")
                    disciplina = prova.get("disciplina", "?")
                    embed.add_field(
                        name=f"[{status}] {titulo}",
                        value=f"📅 Data: {data} | Peso: {peso}\n📘 Matéria: {disciplina}",
                        inline=False,
                    )

            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /avaliacoes", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar as avaliações. Tente novamente.",
                ephemeral=True,
            )

    @app_commands.command(
        name="frequencia_risco",
        description="Lista disciplinas com frequência em risco (≤ 75%).",
    )
    async def frequencia_risco(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            em_risco = await get_disciplinas_em_risco(interaction.user.id)

            embed = discord.Embed(
                title="⚠️ Disciplinas com Frequência em Risco",
                color=discord.Color.from_str("#c82245") if em_risco else discord.Color.green(),
            )

            if not em_risco:
                embed.description = (
                    "✅ Nenhuma disciplina com frequência em risco. Continue assim!"
                )
            else:
                embed.description = (
                    f"Você tem **{len(em_risco)}** disciplina(s) "
                    f"abaixo do limite mínimo de **75%** de frequência."
                )
                for disc in em_risco:
                    embed.add_field(
                        name=f"🔴 {disc['codigo']} — {disc['nome']}",
                        value=(
                            f"📉 Frequência: **{disc['frequencia']}%**\n"
                            f"❌ Faltas: **{disc['faltas']}** "
                            f"(máximo permitido: {disc['faltas_max_permitidas']})\n"
                            f"⚡ Excedeu em **{disc['faltas_acima_limite']}** falta(s)"
                        ),
                        inline=False,
                    )

            embed.set_footer(text="FATEC exige mínimo de 75% de frequência para aprovação.")
            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /frequencia_risco", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível verificar a frequência. Tente novamente.",
                ephemeral=True,
            )

    @app_commands.command(
        name="media_necessaria",
        description="Calcula a nota mínima necessária para aprovação em cada disciplina.",
    )
    async def media_necessaria(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            disciplinas = await get_todas_disciplinas(interaction.user.id)
            if not disciplinas:
                await interaction.followup.send(
                    "Nenhuma disciplina cadastrada no momento.", ephemeral=True
                )
                return

            view = MediaView(disciplinas)
            await interaction.followup.send(
                "🧮 Selecione uma disciplina para calcular a média necessária:",
                view=view,
            )

        except Exception:
            logger.error("Erro em /media_necessaria", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar os dados. Tente novamente.",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(FatecNotas(bot))
