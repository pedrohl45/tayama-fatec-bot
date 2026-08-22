import os
import logging
import discord
from discord import app_commands
from discord.ext import commands

from database.mysql_db import get_aluno, upsert_aluno, get_notas, listar_alunos, deletar_aluno, get_nota_disciplina

logger = logging.getLogger("TayamaBot")

ADMIN_ID = int(os.getenv("ADMIN_DISCORD_ID", "0"))


def is_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.id == ADMIN_ID


class EditarAlunoModal(discord.ui.Modal, title="Editar Aluno"):
    nome = discord.ui.TextInput(label="Nome", max_length=150)
    curso = discord.ui.TextInput(label="Curso", max_length=100)
    semestre = discord.ui.TextInput(label="Semestre (número)", max_length=1)
    status = discord.ui.TextInput(label="Status (Matriculado/Ativa/etc)", max_length=30)
    horas = discord.ui.TextInput(label="Horas Complementares Cumpridas", max_length=5)

    def __init__(self, aluno: dict, discord_id: str):
        super().__init__()
        self.target_id = discord_id
        self.nome.default = aluno.get("nome", "")
        self.curso.default = aluno.get("curso", "")
        self.semestre.default = str(aluno.get("semestre", "1"))
        self.status.default = aluno.get("status_matricula", "Matriculado")
        self.horas.default = str(aluno.get("horas_cumpridas", 0))

    async def on_submit(self, interaction: discord.Interaction):
        try:
            sem = int(self.semestre.value)
            hc = int(self.horas.value)
        except ValueError:
            await interaction.response.send_message("⚠️ Semestre e Horas devem ser números.", ephemeral=True)
            return

        ok = await upsert_aluno(self.target_id, {
            "nome": self.nome.value,
            "curso": self.curso.value,
            "semestre": sem,
            "status_matricula": self.status.value,
            "horas_cumpridas": hc,
        })

        msg = "✅ Aluno atualizado com sucesso!" if ok else "❌ Erro ao atualizar aluno."
        await interaction.response.send_message(msg, ephemeral=True)


class AdminAlunosSelect(discord.ui.Select):
    def __init__(self, alunos: list[dict]):
        options = [
            discord.SelectOption(
                label=f"{a.get('nome', 'Sem nome')[:80]}",
                value=a.get("discord_id"),
                description=f"{a.get('curso', '')[:50]} • {a.get('semestre', '?')}° sem.",
            )
            for a in alunos
        ]
        super().__init__(placeholder="Selecione um aluno...", options=options)
        self._alunos = {a["discord_id"]: a for a in alunos}

    async def callback(self, interaction: discord.Interaction):
        discord_id = self.values[0]
        aluno = self._alunos.get(discord_id)
        if not aluno:
            return await interaction.response.send_message("Aluno não encontrado.", ephemeral=True)

        # Pega notas do MySQL
        notas_lista = await get_notas(discord_id)

        embed = discord.Embed(
            title=f"🗂️ {aluno.get('nome', '?')}",
            color=discord.Color.from_str("#c82245")
        )
        embed.add_field(name="Discord ID", value=f"`{discord_id}`", inline=True)
        embed.add_field(name="Curso", value=aluno.get("curso", "—"), inline=True)
        embed.add_field(name="Semestre", value=f"{aluno.get('semestre', '—')}°", inline=True)
        embed.add_field(name="Status", value=aluno.get("status_matricula", "—"), inline=True)
        embed.add_field(name="Horas Compl.", value=f"{aluno.get('horas_cumpridas', 0)}/{aluno.get('horas_exigidas', 120)}h", inline=True)
        embed.add_field(name="Cadastrado em", value=str(aluno.get("criado_em", "—"))[:10], inline=True)

        if notas_lista:
            linhas = []
            for n in notas_lista:
                linhas.append(
                    f"**{n['codigo_disciplina']}** | P1:{n.get('p1','—')} P2:{n.get('p2','—')} Proj:{n.get('projeto','—')} | Faltas:{n.get('faltas',0)}"
                )
            embed.add_field(name="📊 Notas & Faltas", value="\n".join(linhas)[:1020], inline=False)
        else:
            embed.add_field(name="📊 Notas & Faltas", value="Nenhuma nota lançada ainda.", inline=False)

        # Botões de ação
        view = discord.ui.View()

        btn_editar = discord.ui.Button(label="✏️ Editar", style=discord.ButtonStyle.secondary)
        async def editar_cb(btn_i: discord.Interaction):
            await btn_i.response.send_modal(EditarAlunoModal(aluno, discord_id))
        btn_editar.callback = editar_cb

        btn_deletar = discord.ui.Button(label="🗑️ Remover", style=discord.ButtonStyle.danger)
        async def deletar_cb(btn_i: discord.Interaction):
            ok = await deletar_aluno(discord_id)
            msg = f"✅ Aluno **{aluno.get('nome')}** removido." if ok else "❌ Erro ao remover."
            await btn_i.response.send_message(msg, ephemeral=True)
        btn_deletar.callback = deletar_cb

        view.add_item(btn_editar)
        view.add_item(btn_deletar)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="admin_alunos", description="[ADMIN] Lista todos os alunos cadastrados.")
    async def admin_alunos(self, interaction: discord.Interaction):
        if not is_admin(interaction):
            return await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        alunos = await listar_alunos(limit=25)

        if not alunos:
            return await interaction.followup.send("Nenhum aluno cadastrado ainda.", ephemeral=True)

        embed = discord.Embed(
            title=f"👥 Alunos Cadastrados ({len(alunos)})",
            description="Selecione um aluno para ver detalhes, editar ou remover.",
            color=discord.Color.from_str("#c82245")
        )
        for a in alunos[:10]:
            embed.add_field(
                name=a.get("nome", "Sem nome"),
                value=f"`{a.get('discord_id')}` • {a.get('semestre', '?')}° sem • {a.get('status_matricula', '—')}",
                inline=False,
            )

        view = discord.ui.View()
        view.add_item(AdminAlunosSelect(alunos))

        await interaction.followup.send(embed=embed, view=view, ephemeral=True)

    @app_commands.command(name="admin_checar", description="[ADMIN] Verifica se um usuário está cadastrado.")
    async def admin_checar(self, interaction: discord.Interaction, usuario: discord.Member):
        if not is_admin(interaction):
            return await interaction.response.send_message("❌ Sem permissão.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)
        aluno = await get_aluno(str(usuario.id))

        if aluno:
            embed = discord.Embed(
                title="✅ Aluno Encontrado",
                description=f"**{aluno.get('nome')}** está cadastrado no banco de dados.",
                color=discord.Color.from_str("#c82245")
            )
            embed.add_field(name="Curso", value=aluno.get("curso", "—"), inline=True)
            embed.add_field(name="Semestre", value=f"{aluno.get('semestre', '—')}°", inline=True)
            embed.add_field(name="Status", value=aluno.get("status_matricula", "—"), inline=True)
        else:
            embed = discord.Embed(
                title="❌ Não Cadastrado",
                description=f"**{usuario.display_name}** ainda não usou `/perfil_setup`.",
                color=discord.Color.from_str("#c82245")
            )

        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
