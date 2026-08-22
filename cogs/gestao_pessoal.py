import os
import logging
import discord
from discord import app_commands
from discord.ext import commands

from database.mysql_db import (
    get_aluno, upsert_aluno, get_notas, upsert_nota,
    get_nota_disciplina, registrar_sessao, get_sessoes
)
from database.json_db import carregar_dados

logger = logging.getLogger("TayamaBot")

SEMESTRES = [
    app_commands.Choice(name="1° Semestre", value=1),
    app_commands.Choice(name="2° Semestre", value=2),
    app_commands.Choice(name="3° Semestre", value=3),
    app_commands.Choice(name="4° Semestre", value=4),
    app_commands.Choice(name="5° Semestre", value=5),
    app_commands.Choice(name="6° Semestre", value=6),
]


# Autocomplete de disciplinas baseado no dados.json global (grade da turma)
async def disciplina_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    dados = await carregar_dados()
    disciplinas = dados.get("disciplinas", [])
    choices = []
    for d in disciplinas:
        nome_completo = f"{d.get('codigo')} - {d.get('nome')}"
        if current.lower() in nome_completo.lower():
            choices.append(app_commands.Choice(name=nome_completo[:100], value=d.get("codigo")))
        if len(choices) >= 25:
            break
    return choices


class EditarPerfilModal(discord.ui.Modal, title="Editar Perfil"):
    nome = discord.ui.TextInput(label="Seu nome completo", placeholder="Ex: Julia Maria Helbusto", max_length=150)
    curso = discord.ui.TextInput(label="Curso", placeholder="Ex: DSM", default="Desenvolvimento de Software Multiplataforma (DSM)", max_length=100)

    def __init__(self, dados_atuais: dict):
        super().__init__()
        if dados_atuais:
            self.nome.default = dados_atuais.get("nome", "")
            self.curso.default = dados_atuais.get("curso", "Desenvolvimento de Software Multiplataforma (DSM)")

    async def on_submit(self, interaction: discord.Interaction):
        discord_id = str(interaction.user.id)
        ok = await upsert_aluno(discord_id, {
            "nome": self.nome.value,
            "curso": self.curso.value,
        })
        if ok:
            embed = discord.Embed(
                title="🖤 Perfil Atualizado",
                description=f"Seus dados foram atualizados, **{self.nome.value}**.",
                color=discord.Color.from_str("#c82245")
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Erro ao atualizar. Tente novamente.", ephemeral=True)


class GestaoPessoalMySQL(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ─────────────────────────────────────────
    # /perfil_setup
    # ─────────────────────────────────────────
    @app_commands.command(name="perfil_setup", description="Configure seu nome e perfil para aparecer no boletim.")
    @app_commands.choices(semestre=SEMESTRES)
    async def perfil_setup(
        self, interaction: discord.Interaction,
        nome: str,
        semestre: app_commands.Choice[int],
        curso: str = "Desenvolvimento de Software Multiplataforma (DSM)"
    ):
        await interaction.response.defer(ephemeral=True)
        discord_id = str(interaction.user.id)

        ok = await upsert_aluno(discord_id, {
            "nome": nome,
            "curso": curso,
            "semestre": semestre.value,
        })

        if ok:
            embed = discord.Embed(
                title="🖤 Perfil Configurado",
                description=f"Bem-vinda(o), **{nome}**! Seus dados estão salvos no banco externo e são só seus.",
                color=discord.Color.from_str("#c82245")
            )
            embed.add_field(name="Semestre", value=semestre.name, inline=True)
            embed.add_field(name="Curso", value=curso, inline=True)
            embed.set_footer(text="Use /meu_perfil para ver ou editar seus dados.")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Erro ao salvar perfil. Tente novamente.", ephemeral=True)

    # ─────────────────────────────────────────
    # /meu_perfil
    # ─────────────────────────────────────────
    @app_commands.command(name="meu_perfil", description="Veja e edite seus dados cadastrados.")
    async def meu_perfil(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        discord_id = str(interaction.user.id)
        aluno = await get_aluno(discord_id)

        if not aluno:
            await interaction.followup.send(
                "Você ainda não tem perfil. Use `/perfil_setup` para se cadastrar.", ephemeral=True
            )
            return

        embed = discord.Embed(title="🗂️ Meu Perfil", color=discord.Color.from_str("#c82245"))
        embed.add_field(name="Nome", value=aluno.get("nome", "—"), inline=True)
        embed.add_field(name="Curso", value=aluno.get("curso", "—"), inline=True)
        embed.add_field(name="Semestre", value=f"{aluno.get('semestre', '—')}°", inline=True)
        embed.add_field(name="Status", value=aluno.get("status_matricula", "Matriculado"), inline=True)
        embed.add_field(name="Horas Complementares",
            value=f"{aluno.get('horas_cumpridas', 0)} / {aluno.get('horas_exigidas', 120)}h", inline=True)

        view = discord.ui.View()
        btn = discord.ui.Button(label="✏️ Editar Perfil", style=discord.ButtonStyle.secondary)
        async def editar_callback(btn_interaction: discord.Interaction):
            await btn_interaction.response.send_modal(EditarPerfilModal(aluno))
        btn.callback = editar_callback
        view.add_item(btn)

        await interaction.followup.send(embed=embed, view=view)

    # ─────────────────────────────────────────
    # /lancar_nota
    # ─────────────────────────────────────────
    @app_commands.command(name="lancar_nota", description="Lance ou atualize uma nota (P1, P2 ou Projeto).")
    @app_commands.autocomplete(disciplina=disciplina_autocomplete)
    @app_commands.choices(avaliacao=[
        app_commands.Choice(name="Prova 1 (P1)", value="p1"),
        app_commands.Choice(name="Prova 2 (P2)", value="p2"),
        app_commands.Choice(name="Projeto Integrador", value="projeto"),
        app_commands.Choice(name="Exame Final", value="exame_final"),
    ])
    async def lancar_nota(
        self, interaction: discord.Interaction,
        disciplina: str,
        avaliacao: app_commands.Choice[str],
        nota: float
    ):
        await interaction.response.defer(ephemeral=True)
        if nota < 0 or nota > 10:
            await interaction.followup.send("⚠️ Nota deve ser entre 0.0 e 10.0.", ephemeral=True)
            return

        discord_id = str(interaction.user.id)
        aluno = await get_aluno(discord_id)
        if not aluno:
            await interaction.followup.send("Você precisa usar `/perfil_setup` antes.", ephemeral=True)
            return

        ok = await upsert_nota(discord_id, disciplina, avaliacao.value, nota)
        if ok:
            embed = discord.Embed(
                title="🩸 Nota Lançada!",
                description=f"**{avaliacao.name}** em `{disciplina}` registrada como **{nota:.1f}**.",
                color=discord.Color.from_str("#c82245")
            )
            embed.set_footer(text="Use /boletim para ver seu desempenho.")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Erro ao registrar nota.", ephemeral=True)

    # ─────────────────────────────────────────
    # /lancar_falta
    # ─────────────────────────────────────────
    @app_commands.command(name="lancar_falta", description="Adiciona ou remove faltas de uma disciplina.")
    @app_commands.autocomplete(disciplina=disciplina_autocomplete)
    async def lancar_falta(
        self, interaction: discord.Interaction,
        disciplina: str,
        quantidade: int = 2
    ):
        await interaction.response.defer(ephemeral=True)

        discord_id = str(interaction.user.id)
        aluno = await get_aluno(discord_id)
        if not aluno:
            await interaction.followup.send("Você precisa usar `/perfil_setup` antes.", ephemeral=True)
            return

        # Pega faltas atuais e soma
        registro = await get_nota_disciplina(discord_id, disciplina)
        faltas_atuais = registro.get("faltas", 0) if registro else 0
        novas_faltas = max(0, faltas_atuais + quantidade)

        ok = await upsert_nota(discord_id, disciplina, "faltas", novas_faltas)
        if ok:
            sinal = "Adicionada(s)" if quantidade > 0 else "Removida(s)"
            embed = discord.Embed(
                title="🦇 Controle de Faltas",
                description=f"{sinal} **{abs(quantidade)}** falta(s) em `{disciplina}`.\n**Total atual:** {novas_faltas}",
                color=discord.Color.from_str("#c82245")
            )
            embed.set_footer(text="Use /frequencia_risco para checar o risco de reprovação.")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("❌ Erro ao registrar falta.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(GestaoPessoalMySQL(bot))