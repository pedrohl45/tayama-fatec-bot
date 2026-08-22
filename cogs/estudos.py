import logging

import discord
from discord import app_commands
from discord.ext import commands

from database.json_db import carregar_dados, salvar_dados

logger = logging.getLogger("TayamaBot")


# ──────────────────────────────────────────────
# Modal: Registrar Sessão de Estudo
# ──────────────────────────────────────────────

class RegistroEstudoModal(discord.ui.Modal, title="📚 Registrar Sessão de Estudo"):
    materia = discord.ui.TextInput(
        label="Matéria",
        placeholder="Ex: Algoritmos e Lógica de Programação",
        max_length=80,
        required=True,
    )
    tempo = discord.ui.TextInput(
        label="Tempo estudado (em minutos)",
        placeholder="Ex: 90",
        max_length=5,
        required=True,
    )
    observacao = discord.ui.TextInput(
        label="Observação (opcional)",
        placeholder="Ex: Revisão de listas e funções recursivas",
        style=discord.TextStyle.paragraph,
        max_length=200,
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Valida que o tempo é um número inteiro positivo
        try:
            minutos = int(self.tempo.value.strip())
            if minutos <= 0:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message(
                "⚠️ Informe um número inteiro positivo de minutos (ex: 60).",
                ephemeral=True,
            )

        nome_materia = self.materia.value.strip()
        obs = self.observacao.value.strip() if self.observacao.value else None

        try:
            dados = await carregar_dados()
            focos = dados.setdefault("estudos_foco", [])

            # Acumula no registro existente ou cria um novo
            existente = next(
                (f for f in focos if f.get("materia", "").lower() == nome_materia.lower()),
                None,
            )
            if existente:
                existente["tempo_registrado_minutos"] += minutos
                if obs:
                    existente.setdefault("observacoes", []).append(obs)
            else:
                novo = {
                    "materia": nome_materia,
                    "tempo_registrado_minutos": minutos,
                }
                if obs:
                    novo["observacoes"] = [obs]
                focos.append(novo)

            await salvar_dados(dados)

            total = existente["tempo_registrado_minutos"] if existente else minutos
            horas, mins = divmod(total, 60)
            total_fmt = f"{horas}h {mins}min" if horas else f"{mins}min"

            embed = discord.Embed(
                title="✅ Sessão de estudo registrada!",
                color=discord.Color.green(),
            )
            embed.add_field(name="Matéria", value=nome_materia, inline=True)
            embed.add_field(name="Sessão", value=f"+{minutos} min", inline=True)
            embed.add_field(name="Total acumulado", value=total_fmt, inline=True)
            if obs:
                embed.add_field(name="📌 Observação", value=obs, inline=False)
            embed.set_footer(text="Tayama • Continue assim! 💪")

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception:
            logger.error("Erro ao salvar sessão de estudo", exc_info=True)
            await interaction.response.send_message(
                "⚠️ Erro ao salvar o registro. Tente novamente.", ephemeral=True
            )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error("Erro no RegistroEstudoModal", exc_info=error)
        await interaction.response.send_message(
            "⚠️ Ocorreu um erro inesperado.", ephemeral=True
        )


# ──────────────────────────────────────────────
# Cog
# ──────────────────────────────────────────────

class Estudos(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="estudo_resumo",
        description="Exibe o resumo das horas de estudo focadas.",
    )
    async def estudo_resumo(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            dados = await carregar_dados()
            focos = dados.get("estudos_foco", [])

            embed = discord.Embed(
                title="📈 Resumo de Foco & Estudos",
                color=discord.Color.green(),
            )

            if not focos:
                embed.description = (
                    "Nenhum tempo de estudo registrado ainda.\n"
                    "Use `/registrar_estudo` para começar! 📚"
                )
            else:
                total_geral = sum(f.get("tempo_registrado_minutos", 0) for f in focos)
                horas_g, mins_g = divmod(total_geral, 60)
                embed.description = (
                    f"⏱️ **Total geral:** "
                    f"{'%dh %02dmin' % (horas_g, mins_g) if horas_g else '%dmin' % mins_g}"
                )

                for item in focos:
                    t = item.get("tempo_registrado_minutos", 0)
                    h, m = divmod(t, 60)
                    tempo_fmt = f"{h}h {m:02d}min" if h else f"{m}min"
                    embed.add_field(
                        name=item.get("materia", "Geral"),
                        value=f"⏰ **{tempo_fmt}**",
                        inline=True,
                    )

            await interaction.followup.send(embed=embed)

        except Exception:
            logger.error("Erro em /estudo_resumo", exc_info=True)
            await interaction.followup.send(
                "⚠️ Não foi possível carregar o resumo de estudos. Tente novamente.",
                ephemeral=True,
            )

    @app_commands.command(
        name="registrar_estudo",
        description="Registra uma sessão de estudo com matéria e tempo dedicado.",
    )
    async def registrar_estudo(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RegistroEstudoModal())


async def setup(bot: commands.Bot):
    await bot.add_cog(Estudos(bot))