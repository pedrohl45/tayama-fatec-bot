import logging
import discord
from discord import app_commands
from discord.ext import commands

from database.json_db import carregar_dados
from database.user_db import get_user_data, update_user_data

logger = logging.getLogger("TayamaBot")

# ──────────────────────────────────────────────
# Auto-Complete de Disciplinas
# ──────────────────────────────────────────────
async def disciplina_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    """Gera sugestões de disciplinas baseadas na grade da turma (dados globais)."""
    dados = await carregar_dados()
    disciplinas = dados.get("disciplinas", [])
    
    choices = []
    for d in disciplinas:
        nome_completo = f"{d.get('codigo')} - {d.get('nome')}"
        if current.lower() in nome_completo.lower():
            # O value será o código da disciplina para facilitar a busca no DB do aluno
            choices.append(app_commands.Choice(name=nome_completo[:100], value=d.get("codigo")))
            
        if len(choices) >= 25:
            break
            
    return choices


# ──────────────────────────────────────────────
# Cog: Gestão Pessoal
# ──────────────────────────────────────────────
class GestaoPessoal(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="perfil_setup",
        description="Configure seu nome e perfil para aparecer no boletim."
    )
    async def perfil_setup(self, interaction: discord.Interaction, nome: str, curso: str = "DSM"):
        await interaction.response.defer(ephemeral=True)
        try:
            user_data = await get_user_data(interaction.user.id)
            
            # Garante que a estrutura base exista
            if "aluno" not in user_data:
                user_data["aluno"] = {}
                
            user_data["aluno"]["nome"] = nome
            user_data["aluno"]["curso"] = curso
            
            await update_user_data(interaction.user.id, user_data)
            
            embed = discord.Embed(
                title="✅ Perfil Configurado",
                description=f"Bem-vindo(a), **{nome}**! Seu perfil foi atualizado com sucesso. Seus dados e notas agora estão protegidos e vinculados ao seu usuário.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Erro no setup de perfil: {e}", exc_info=True)
            await interaction.followup.send("Houve um erro ao salvar o perfil.", ephemeral=True)


    @app_commands.command(
        name="lancar_nota",
        description="Lance ou atualize uma nota (P1, P2 ou Projeto) de uma disciplina."
    )
    @app_commands.autocomplete(disciplina=disciplina_autocomplete)
    @app_commands.choices(avaliacao=[
        app_commands.Choice(name="Prova 1 (P1)", value="p1"),
        app_commands.Choice(name="Prova 2 (P2)", value="p2"),
        app_commands.Choice(name="Projeto Integrador", value="projeto"),
        app_commands.Choice(name="Exame Final", value="exame_final")
    ])
    async def lancar_nota(
        self, 
        interaction: discord.Interaction, 
        disciplina: str, 
        avaliacao: app_commands.Choice[str], 
        nota: float
    ):
        await interaction.response.defer(ephemeral=True)
        
        # Validação da nota
        if nota < 0.0 or nota > 10.0:
            await interaction.followup.send("⚠️ A nota deve ser um valor entre 0.0 e 10.0.", ephemeral=True)
            return

        try:
            user_data = await get_user_data(interaction.user.id)
            
            # Garantir a árvore do dicionário
            desempenho_db = user_data.setdefault("desempenho_disciplinas", {})
            disc_db = desempenho_db.setdefault(disciplina, {})
            notas_db = disc_db.setdefault("notas", {"p1": None, "p2": None, "projeto": None})
            
            # Salvar a nova nota
            notas_db[avaliacao.value] = nota
            
            await update_user_data(interaction.user.id, user_data)
            
            embed = discord.Embed(
                title="📝 Nota Lançada!",
                description=f"Sua nota de **{avaliacao.name}** na disciplina `{disciplina}` foi registrada como **{nota:.1f}**.",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Use /boletim ou /media_necessaria para acompanhar seu progresso.")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Erro ao lançar nota: {e}", exc_info=True)
            await interaction.followup.send("Houve um erro ao registrar a nota.", ephemeral=True)


    @app_commands.command(
        name="lancar_falta",
        description="Adiciona ou remove faltas de uma disciplina."
    )
    @app_commands.autocomplete(disciplina=disciplina_autocomplete)
    async def lancar_falta(
        self, 
        interaction: discord.Interaction, 
        disciplina: str, 
        quantidade: int = 2
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            user_data = await get_user_data(interaction.user.id)
            
            desempenho_db = user_data.setdefault("desempenho_disciplinas", {})
            disc_db = desempenho_db.setdefault(disciplina, {})
            
            faltas_atuais = disc_db.get("faltas", 0)
            novas_faltas = max(0, faltas_atuais + quantidade)  # Impede faltas negativas
            
            disc_db["faltas"] = novas_faltas
            
            await update_user_data(interaction.user.id, user_data)
            
            sinal = "Adicionada(s)" if quantidade > 0 else "Removida(s)"
            embed = discord.Embed(
                title="📉 Controle de Faltas",
                description=f"{sinal} **{abs(quantidade)}** falta(s) na disciplina `{disciplina}`.\n\n**Total atual de faltas:** {novas_faltas}",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Use /frequencia_risco para ver se você está próximo do limite.")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Erro ao registrar falta: {e}", exc_info=True)
            await interaction.followup.send("Houve um erro ao registrar a falta.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(GestaoPessoal(bot))

